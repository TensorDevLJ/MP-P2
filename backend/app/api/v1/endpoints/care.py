"""
Healthcare provider discovery endpoints using Google Places API
"""
from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import structlog
import googlemaps
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.provider import HealthcareProvider, UserProviderBookmark
from app.schemas.care import ProviderSearchRequest, ProviderResponse, BookmarkRequest

logger = structlog.get_logger(__name__)
router = APIRouter()

# Initialize Google Maps client
gmaps = None
if settings.GOOGLE_MAPS_API_KEY:
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

@router.get("/nearby", response_model=List[ProviderResponse])
async def find_nearby_providers(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    specialty: str = Query(default="mental health", description="Provider specialty"),
    radius: int = Query(default=10000, description="Search radius in meters"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Find nearby mental health providers using Google Places API"""
    
    if not gmaps:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Location services are not configured"
        )
    
    logger.info("Searching for nearby providers",
               user_id=str(current_user.id),
               lat=lat, lng=lng, specialty=specialty)
    
    try:
        # Check cache first
        cached_providers = await _get_cached_providers(db, lat, lng, specialty, radius)
        if cached_providers:
            logger.info("Returning cached providers", count=len(cached_providers))
            return cached_providers
        
        # Search Google Places API
        search_query = f"{specialty} near me"
        if specialty == "mental health":
            search_query = "psychiatrist psychologist therapist counselor"
        
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=radius,
            keyword=search_query,
            type="health"
        )
        
        providers = []
        
        for place in places_result.get('results', []):
            # Get detailed information
            place_details = gmaps.place(
                place_id=place['place_id'],
                fields=[
                    'name', 'formatted_address', 'formatted_phone_number',
                    'website', 'rating', 'user_ratings_total', 'opening_hours',
                    'photos', 'price_level', 'types'
                ]
            )
            
            detail = place_details.get('result', {})
            
            # Determine specialty from types and name
            determined_specialty = _determine_specialty(place.get('types', []), place.get('name', ''))
            
            provider_data = {
                'google_place_id': place['place_id'],
                'name': detail.get('name', ''),
                'specialty': determined_specialty,
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'address': detail.get('formatted_address', ''),
                'phone': detail.get('formatted_phone_number'),
                'website': detail.get('website'),
                'rating': detail.get('rating'),
                'user_ratings_total': detail.get('user_ratings_total'),
                'price_level': detail.get('price_level'),
                'opening_hours': detail.get('opening_hours', {}).get('weekday_text'),
            }
            
            # Calculate distance
            distance_km = _calculate_distance(lat, lng, provider_data['latitude'], provider_data['longitude'])
            provider_data['distance_km'] = distance_km
            
            # Check if currently open
            provider_data['open_now'] = detail.get('opening_hours', {}).get('open_now', False)
            
            providers.append(ProviderResponse(**provider_data))
            
            # Cache in database
            await _cache_provider(db, provider_data)
        
        # Sort by distance and rating
        providers.sort(key=lambda p: (p.distance_km, -p.rating if p.rating else 0))
        
        logger.info("Found nearby providers", count=len(providers))
        return providers[:20]  # Limit to top 20 results
        
    except Exception as e:
        logger.error("Provider search failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search for providers"
        )

@router.post("/bookmark")
async def bookmark_provider(
    request: BookmarkRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Bookmark a healthcare provider"""
    
    # Check if already bookmarked
    existing = db.query(UserProviderBookmark).filter(
        UserProviderBookmark.user_id == current_user.id,
        UserProviderBookmark.provider_id == request.provider_id
    ).first()
    
    if existing:
        # Update existing bookmark
        existing.notes = request.notes
        existing.updated_at = datetime.utcnow()
    else:
        # Create new bookmark
        bookmark = UserProviderBookmark(
            user_id=current_user.id,
            provider_id=request.provider_id,
            notes=request.notes
        )
        db.add(bookmark)
    
    db.commit()
    
    logger.info("Provider bookmarked", 
               user_id=str(current_user.id),
               provider_id=request.provider_id)
    
    return {"message": "Provider bookmarked successfully"}

@router.get("/bookmarks")
async def get_user_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Get user's bookmarked providers"""
    
    bookmarks = db.query(UserProviderBookmark).filter(
        UserProviderBookmark.user_id == current_user.id
    ).order_by(UserProviderBookmark.created_at.desc()).all()
    
    providers = []
    for bookmark in bookmarks:
        provider = db.query(HealthcareProvider).filter(
            HealthcareProvider.id == bookmark.provider_id
        ).first()
        
        if provider:
            provider_data = {
                'id': str(provider.id),
                'name': provider.name,
                'specialty': provider.specialty,
                'phone': provider.phone,
                'address': provider.address,
                'rating': provider.rating,
                'bookmarked_at': bookmark.created_at,
                'notes': bookmark.notes
            }
            providers.append(provider_data)
    
    return {"bookmarks": providers}

async def _get_cached_providers(
    db: Session, 
    lat: float, 
    lng: float, 
    specialty: str, 
    radius: int
) -> List[ProviderResponse]:
    """Get cached providers within radius"""
    
    # Simple radius check (in production, use PostGIS for better geo queries)
    cache_expiry = datetime.utcnow() - timedelta(hours=24)  # 24 hour cache
    
    providers = db.query(HealthcareProvider).filter(
        HealthcareProvider.specialty == specialty,
        HealthcareProvider.cached_at > cache_expiry
    ).all()
    
    # Filter by distance
    nearby_providers = []
    for provider in providers:
        distance = _calculate_distance(lat, lng, provider.latitude, provider.longitude)
        if distance * 1000 <= radius:  # Convert km to meters
            provider_response = ProviderResponse(
                id=str(provider.id),
                google_place_id=provider.google_place_id,
                name=provider.name,
                specialty=provider.specialty,
                latitude=provider.latitude,
                longitude=provider.longitude,
                address=provider.address,
                phone=provider.phone,
                website=provider.website,
                rating=provider.rating,
                user_ratings_total=provider.user_ratings_total,
                price_level=provider.price_level,
                opening_hours=provider.opening_hours,
                distance_km=distance,
                open_now=False  # Would need real-time check
            )
            nearby_providers.append(provider_response)
    
    return nearby_providers if len(nearby_providers) >= 5 else []

async def _cache_provider(db: Session, provider_data: Dict[str, Any]):
    """Cache provider in database"""
    
    try:
        existing = db.query(HealthcareProvider).filter(
            HealthcareProvider.google_place_id == provider_data['google_place_id']
        ).first()
        
        if existing:
            # Update existing record
            for key, value in provider_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.cached_at = datetime.utcnow()
        else:
            # Create new record
            provider = HealthcareProvider(**provider_data)
            db.add(provider)
        
        db.commit()
        
    except Exception as e:
        logger.error("Provider caching failed", error=str(e))
        db.rollback()

def _determine_specialty(types: List[str], name: str) -> str:
    """Determine provider specialty from Google Places types and name"""
    
    name_lower = name.lower()
    
    # Check name for specific specialties
    if any(word in name_lower for word in ['psychiatrist', 'psychiatric']):
        return 'psychiatrist'
    elif any(word in name_lower for word in ['psychologist', 'psychology']):
        return 'psychologist'
    elif any(word in name_lower for word in ['therapist', 'therapy', 'counselor', 'counseling']):
        return 'therapist'
    elif any(word in name_lower for word in ['neurologist', 'neurology']):
        return 'neurologist'
    
    # Check types
    if 'hospital' in types:
        return 'psychiatrist'  # Assume psychiatrist for hospitals
    elif 'health' in types:
        return 'mental health provider'
    
    return 'mental health provider'

def _calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    
    from math import radians, cos, sin, asin, sqrt
    
    # Convert to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in kilometers
    r = 6371
    
    return c * r