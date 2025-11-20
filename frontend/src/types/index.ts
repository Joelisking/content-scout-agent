export interface User {
  id: number;
  email: string;
  full_name: string;
  company_name?: string;
  country: string;
  is_active: boolean;
  is_verified: boolean;
  subscription_tier: 'free' | 'starter' | 'pro';
  payment_provider?: 'stripe' | 'paystack';
  blogs_created_this_month: number;
  blog_limit: number;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  company_name?: string;
  country: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface ResearchJob {
  id: number;
  user_id: number;
  sector: string;
  location: string;
  additional_keywords?: string;
  tone: string;
  status: 'pending' | 'researching' | 'generating' | 'completed' | 'failed';
  error_message?: string;
  research_data?: any;
  keywords_found?: string[];
  created_at: string;
  started_at?: string;
  completed_at?: string;
  celery_task_id?: string;
}

export interface CreateJobData {
  sector: string;
  location: string;
  additional_keywords?: string;
  tone?: string;
}

export interface Blog {
  id: number;
  user_id: number;
  research_job_id: number;
  title: string;
  content: string;
  summary?: string;
  keywords?: string;
  word_count?: number;
  reading_time_minutes?: number;
  markdown_file_path?: string;
  pdf_file_path?: string;
  html_file_path?: string;
  created_at: string;
}

export interface PricingTier {
  tier: 'free' | 'starter' | 'pro';
  price: number;
  currency: string;
  blogs_per_month: number;
  features: string[];
}

export interface Subscription {
  tier: 'free' | 'starter' | 'pro';
  payment_provider?: 'stripe' | 'paystack';
  status?: string;
  current_period_end?: string;
  blogs_created_this_month: number;
  blog_limit: number;
}
