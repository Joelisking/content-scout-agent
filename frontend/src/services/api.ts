import axios from 'axios';
import type {
  AuthResponse,
  RegisterData,
  LoginData,
  User,
  ResearchJob,
  CreateJobData,
  Blog,
  PricingTier,
  Subscription,
} from '@/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Research Jobs API
export const jobsAPI = {
  create: async (data: CreateJobData): Promise<ResearchJob> => {
    const response = await api.post('/jobs', data);
    return response.data;
  },

  list: async (params?: { page?: number; page_size?: number; status?: string }) => {
    const response = await api.get('/jobs', { params });
    return response.data;
  },

  get: async (id: number): Promise<ResearchJob> => {
    const response = await api.get(`/jobs/${id}`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/jobs/${id}`);
  },
};

// Blogs API
export const blogsAPI = {
  list: async (params?: { page?: number; page_size?: number }) => {
    const response = await api.get('/blogs', { params });
    return response.data;
  },

  get: async (id: number): Promise<Blog> => {
    const response = await api.get(`/blogs/${id}`);
    return response.data;
  },

  downloadMarkdown: async (id: number): Promise<Blob> => {
    const response = await api.get(`/blogs/${id}/download/markdown`, {
      responseType: 'blob',
    });
    return response.data;
  },

  downloadPDF: async (id: number): Promise<Blob> => {
    const response = await api.get(`/blogs/${id}/download/pdf`, {
      responseType: 'blob',
    });
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/blogs/${id}`);
  },

  getStats: async () => {
    const response = await api.get('/blogs/stats/summary');
    return response.data;
  },
};

// Subscriptions API
export const subscriptionsAPI = {
  getPricing: async (): Promise<PricingTier[]> => {
    const response = await api.get('/subscriptions/pricing');
    return response.data;
  },

  getPaymentMethod: async () => {
    const response = await api.get('/subscriptions/payment-method');
    return response.data;
  },

  getCurrent: async (): Promise<Subscription> => {
    const response = await api.get('/subscriptions/current');
    return response.data;
  },

  create: async (data: { tier: string; payment_method_id?: string }) => {
    const response = await api.post('/subscriptions/create', data);
    return response.data;
  },

  cancel: async () => {
    const response = await api.post('/subscriptions/cancel');
    return response.data;
  },

  verifyPaystack: async (reference: string) => {
    const response = await api.get(`/subscriptions/verify/paystack/${reference}`);
    return response.data;
  },
};

export default api;
