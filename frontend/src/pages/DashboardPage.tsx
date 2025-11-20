import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { jobsAPI, blogsAPI } from '@/services/api';
import toast from 'react-hot-toast';
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
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    sector: '',
    location: '',
    additional_keywords: '',
    tone: 'professional',
  });

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

  // Create job mutation
  const createJobMutation = useMutation({
    mutationFn: jobsAPI.create,
    onSuccess: () => {
      toast.success('Blog generation started! You\'ll be notified when it\'s ready.');
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      setShowCreateModal(false);
      setFormData({ sector: '', location: '', additional_keywords: '', tone: 'professional' });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create job');
    },
  });

  const handleCreateJob = (e: React.FormEvent) => {
    e.preventDefault();
    createJobMutation.mutate(formData);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const canCreateBlog = user && (user.blog_limit === -1 || user.blogs_created_this_month < user.blog_limit);

  return (
    <div className="min-h-screen bg-dark-950 text-white">
      {/* Navigation */}
      <nav className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <Link to="/dashboard" className="flex items-center space-x-2">
                <Sparkles className="w-8 h-8 text-primary-500" />
                <span className="text-xl font-bold">Content Scout</span>
              </Link>
              <Link
                to="/blogs"
                className="text-dark-300 hover:text-white transition flex items-center space-x-2"
              >
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
                to="/settings"
                className="p-2 hover:bg-dark-800 rounded-lg transition"
              >
                <Settings className="w-5 h-5" />
              </Link>
              <button
                onClick={handleLogout}
                className="p-2 hover:bg-dark-800 rounded-lg transition"
              >
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
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.full_name}!</h1>
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
            value={`${statsData?.blogs_this_month || 0} / ${statsData?.blog_limit === -1 ? '∞' : statsData?.blog_limit || 0}`}
          />
          <StatCard
            icon={<FileText className="w-8 h-8 text-purple-500" />}
            title="Total Words"
            value={statsData?.total_word_count?.toLocaleString() || 0}
          />
        </div>

        {/* Create Button */}
        <div className="mb-8">
          <button
            onClick={() => setShowCreateModal(true)}
            disabled={!canCreateBlog}
            className="w-full md:w-auto gradient-primary px-8 py-4 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>Create New Blog</span>
          </button>
          {!canCreateBlog && (
            <p className="text-red-400 text-sm mt-2">
              You've reached your monthly limit. <Link to="/settings" className="underline">Upgrade your plan</Link>.
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
              <p className="text-dark-300">No jobs yet. Create your first blog!</p>
            </div>
          )}
        </div>
      </div>

      {/* Create Job Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-dark-900 rounded-2xl border border-dark-800 max-w-2xl w-full p-8">
            <h2 className="text-2xl font-bold mb-6">Create New Blog</h2>
            <form onSubmit={handleCreateJob} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Industry Sector *</label>
                  <input
                    type="text"
                    required
                    value={formData.sector}
                    onChange={(e) => setFormData({ ...formData, sector: e.target.value })}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., Real Estate, Healthcare"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Location *</label>
                  <input
                    type="text"
                    required
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., Ghana, Lagos"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Additional Keywords (optional)</label>
                <input
                  type="text"
                  value={formData.additional_keywords}
                  onChange={(e) => setFormData({ ...formData, additional_keywords: e.target.value })}
                  className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                  placeholder="e.g., luxury homes, investment"
                />
                <p className="text-xs text-dark-400 mt-1">Comma-separated keywords to refine your research</p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Tone</label>
                <select
                  value={formData.tone}
                  onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                  className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                >
                  <option value="professional">Professional</option>
                  <option value="casual">Casual</option>
                  <option value="technical">Technical</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-6 py-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createJobMutation.isPending}
                  className="gradient-primary px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50"
                >
                  {createJobMutation.isPending ? 'Creating...' : 'Create Blog'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ icon, title, value }: { icon: React.ReactNode; title: string; value: string | number }) {
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
        return <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />;
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
            <span className="text-sm capitalize">{getStatusText()}</span>
          </div>
        </div>
        {job.status === 'completed' && job.blog && (
          <Link
            to={`/blogs/${job.blog.id}`}
            className="gradient-primary px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 transition"
          >
            View Blog
          </Link>
        )}
      </div>
    </div>
  );
}
