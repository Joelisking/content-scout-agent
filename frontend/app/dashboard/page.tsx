'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  useQuery,
  useMutation,
  useQueryClient,
} from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { jobsAPI, blogsAPI } from '@/lib/api';
import { toast } from 'sonner';
import {
  Sparkles,
  Plus,
  FileText,
  Settings,
  LogOut,
  TrendingUp,
  Clock,
  CheckCircle2,
  XCircle,
  Loader2,
} from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  // Fetch recent jobs
  const { data: jobsData, isLoading: jobsLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: () => jobsAPI.list({ page: 1, page_size: 10 }),
  });

  // Fetch blog stats
  const { data: statsData } = useQuery({
    queryKey: ['blog-stats'],
    queryFn: () => blogsAPI.getStats(),
  });

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const canCreateBlog =
    user &&
    (user.blog_limit === -1 ||
      user.blogs_created_this_month < user.blog_limit);

  return (
    <div className="min-h-screen bg-dark-950 text-white">
      {/* Navigation */}
      <nav className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <Link
                href="/dashboard"
                className="flex items-center space-x-2">
                <Sparkles className="w-8 h-8 text-primary-500" />
                <span className="text-xl font-bold">
                  Content Scout
                </span>
              </Link>
              <Link
                href="/blogs"
                className="text-dark-300 hover:text-white transition flex items-center space-x-2">
                <FileText className="w-5 h-5" />
                <span>Blogs</span>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-dark-300">
                {user?.subscription_tier && (
                  <span className="px-3 py-1 bg-primary-500/20 text-primary-400 rounded-full capitalize">
                    {user.subscription_tier}
                  </span>
                )}
              </div>
              <Link
                href="/settings"
                className="p-2 hover:bg-dark-800 rounded-lg transition">
                <Settings className="w-5 h-5" />
              </Link>
              <button
                onClick={handleLogout}
                className="p-2 hover:bg-dark-800 rounded-lg transition">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-dark-300">
            Generate AI-powered blog content for your business
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon={<FileText className="w-8 h-8 text-primary-500" />}
            title="Total Blogs"
            value={statsData?.total_blogs || 0}
          />
          <StatCard
            icon={<TrendingUp className="w-8 h-8 text-green-500" />}
            title="This Month"
            value={`${statsData?.blogs_this_month || 0} / ${
              statsData?.blog_limit === -1
                ? '∞'
                : statsData?.blog_limit || 0
            }`}
          />
          <StatCard
            icon={<FileText className="w-8 h-8 text-purple-500" />}
            title="Total Words"
            value={statsData?.total_word_count?.toLocaleString() || 0}
          />
        </div>

        {/* Create Button */}
        <div className="mb-8">
          <Link
            href={canCreateBlog ? '/create-blog' : '#'}
            onClick={(e) => {
              if (!canCreateBlog) {
                e.preventDefault();
                toast.error('You have reached your monthly blog limit');
              }
            }}
            className={`w-full md:w-auto gradient-primary px-8 py-4 rounded-xl font-semibold hover:opacity-90 transition flex items-center justify-center space-x-2 ${
              !canCreateBlog ? 'opacity-50 cursor-not-allowed' : ''
            }`}>
            <Plus className="w-5 h-5" />
            <span>Create New Blog</span>
          </Link>
          {!canCreateBlog && (
            <p className="text-red-400 text-sm mt-2">
              You&apos;ve reached your monthly limit.{' '}
              <Link href="/settings" className="underline">
                Upgrade your plan
              </Link>
              .
            </p>
          )}
        </div>

        {/* Recent Jobs */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Recent Jobs</h2>
          {jobsLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
            </div>
          ) : jobsData?.jobs?.length > 0 ? (
            <div className="space-y-4">
              {jobsData.jobs.map((job: any) => (
                <JobCard key={job.id} job={job} />
              ))}
            </div>
          ) : (
            <div className="bg-dark-900 p-12 rounded-2xl border border-dark-800 text-center">
              <FileText className="w-16 h-16 text-dark-600 mx-auto mb-4" />
              <p className="text-dark-300">
                No jobs yet. Create your first blog!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({
  icon,
  title,
  value,
}: {
  icon: React.ReactNode;
  title: string;
  value: string | number;
}) {
  return (
    <div className="bg-dark-900 p-6 rounded-2xl border border-dark-800">
      <div className="flex items-center justify-between mb-4">
        {icon}
      </div>
      <p className="text-dark-300 text-sm mb-1">{title}</p>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}

function JobCard({ job }: { job: any }) {
  const getStatusIcon = () => {
    switch (job.status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'pending':
      case 'researching':
      case 'generating':
        return (
          <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />
        );
      default:
        return <Clock className="w-5 h-5 text-dark-500" />;
    }
  };

  const getStatusText = () => {
    switch (job.status) {
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      case 'researching':
        return 'Researching...';
      case 'generating':
        return 'Generating...';
      default:
        return 'Pending';
    }
  };

  return (
    <div className="bg-dark-900 p-6 rounded-xl border border-dark-800 hover:border-dark-700 transition">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold mb-2">
            {job.sector} in {job.location}
          </h3>
          <p className="text-dark-400 text-sm mb-3">
            Created {new Date(job.created_at).toLocaleDateString()}
          </p>
          <div className="flex items-center space-x-2">
            {getStatusIcon()}
            <span className="text-sm capitalize">
              {getStatusText()}
            </span>
          </div>
        </div>
        {job.status === 'completed' && job.blog && (
          <Link
            href={`/blogs/${job.blog.id}`}
            className="gradient-primary px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 transition">
            View Blog
          </Link>
        )}
      </div>
    </div>
  );
}
