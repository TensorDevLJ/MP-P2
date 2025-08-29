import * as yup from 'yup';

export const loginSchema = yup.object({
  email: yup
    .string()
    .email('Please enter a valid email address')
    .required('Email is required'),
  password: yup
    .string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
});

export const signupSchema = yup.object({
  email: yup
    .string()
    .email('Please enter a valid email address')
    .required('Email is required'),
  password: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .matches(/[a-z]/, 'Password must contain at least one lowercase letter')
    .matches(/\d/, 'Password must contain at least one number')
    .required('Password is required'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
  displayName: yup
    .string()
    .min(2, 'Display name must be at least 2 characters')
    .required('Display name is required'),
  timezone: yup.string().required('Timezone is required'),
});

export const textAnalysisSchema = yup.object({
  text: yup
    .string()
    .min(10, 'Please provide at least 10 characters for meaningful analysis')
    .max(5000, 'Text must be less than 5000 characters')
    .required('Text is required for analysis'),
});