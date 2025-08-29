import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const useAPIQuery = (queryKey, queryFn, options = {}) => {
  return useQuery({
    queryKey,
    queryFn,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    ...options,
  });
};

export const useAPIMutation = (mutationFn, options = {}) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn,
    onSuccess: () => {
      if (options.invalidateQueries) {
        queryClient.invalidateQueries(options.invalidateQueries);
      }
    },
    ...options,
  });
};

export const usePolling = (queryKey, queryFn, interval = 2000, enabled = true) => {
  return useQuery({
    queryKey,
    queryFn,
    refetchInterval: enabled ? interval : false,
    refetchIntervalInBackground: false,
    enabled,
  });
};

export const useFileUpload = (uploadFn) => {
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);

  const upload = async (file, onProgress) => {
    setUploading(true);
    setProgress(0);

    try {
      const result = await uploadFn(file, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percentCompleted);
        onProgress?.(percentCompleted);
      });

      setUploading(false);
      setProgress(100);
      return result;
    } catch (error) {
      setUploading(false);
      setProgress(0);
      throw error;
    }
  };

  return { upload, progress, uploading };
};