'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { jobsAPI } from '@/lib/api';
import { toast } from 'sonner';
import {
  Sparkles,
  ArrowLeft,
  ChevronDown,
  ChevronUp,
  Loader2,
} from 'lucide-react';

export default function CreateBlogPage() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [formData, setFormData] = useState({
    sector: '',
    location: '',
    custom_title: '',
    target_word_count: '',
    additional_keywords: '',
    tone: 'professional',
    writing_style: '',
    target_audience: '',
    content_depth: 'moderate',
    seo_focus: 'medium',
    include_sections: [] as string[],
    custom_instructions: '',
  });

  // Create job mutation
  const createJobMutation = useMutation({
    mutationFn: jobsAPI.create,
    onSuccess: () => {
      toast.success(
        "Blog generation started! You'll be notified when it's ready."
      );
      router.push('/dashboard');
    },
    onError: (error: any) => {
      toast.error(
        error.response?.data?.detail || 'Failed to create job'
      );
    },
  });

  const handleCreateJob = (e: React.FormEvent) => {
    e.preventDefault();
    createJobMutation.mutate(formData);
  };

  const canCreateBlog =
    user &&
    (user.blog_limit === -1 ||
      user.blogs_created_this_month < user.blog_limit);

  if (!canCreateBlog) {
    return (
      <div className="min-h-screen bg-dark-950 text-white flex items-center justify-center p-4">
        <div className="max-w-md text-center">
          <h1 className="text-2xl font-bold mb-4">Limit Reached</h1>
          <p className="text-dark-300 mb-6">
            You&apos;ve reached your monthly blog limit.{' '}
            <Link href="/settings" className="text-primary-500 hover:underline">
              Upgrade your plan
            </Link>{' '}
            to create more blogs.
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center space-x-2 text-dark-300 hover:text-white transition">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-950 text-white">
      {/* Navigation */}
      <nav className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-xl sticky top-0 z-40">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link
              href="/dashboard"
              className="flex items-center space-x-2 text-dark-300 hover:text-white transition">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Dashboard</span>
            </Link>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-6 h-6 text-primary-500" />
              <span className="text-lg font-semibold">Create New Blog</span>
            </div>
            <div className="w-32" /> {/* Spacer for centering */}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleCreateJob} className="space-y-8">
          {/* Basic Settings Section */}
          <div className="bg-dark-900 rounded-2xl border border-dark-800 p-6 md:p-8">
            <h2 className="text-xl font-bold mb-6">Basic Settings</h2>

            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Industry Sector *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.sector}
                    onChange={(e) =>
                      setFormData({ ...formData, sector: e.target.value })
                    }
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., Real Estate, Healthcare"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Location *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.location}
                    onChange={(e) =>
                      setFormData({ ...formData, location: e.target.value })
                    }
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., Ghana, Lagos"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Custom Title (optional)
                </label>
                <input
                  type="text"
                  value={formData.custom_title}
                  onChange={(e) =>
                    setFormData({ ...formData, custom_title: e.target.value })
                  }
                  className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                  placeholder="Leave blank for AI to generate"
                />
                <p className="text-xs text-dark-400 mt-1">
                  Provide a custom title or let AI create one based on your content
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Target Word Count (optional)
                  </label>
                  <select
                    value={formData.target_word_count}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        target_word_count: e.target.value,
                      })
                    }
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition">
                    <option value="">Default (1200-1800)</option>
                    <option value="800-1000">Short (800-1000)</option>
                    <option value="1200-1800">Medium (1200-1800)</option>
                    <option value="2000-2500">Long (2000-2500)</option>
                    <option value="2500-3000">Very Long (2500-3000)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Additional Keywords (optional)
                  </label>
                  <input
                    type="text"
                    value={formData.additional_keywords}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        additional_keywords: e.target.value,
                      })
                    }
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., luxury, investment"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Advanced Settings Section */}
          <div className="bg-dark-900 rounded-2xl border border-dark-800 overflow-hidden">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="w-full flex items-center justify-between p-6 md:p-8 hover:bg-dark-800/30 transition">
              <h2 className="text-xl font-bold">Advanced Settings</h2>
              {showAdvanced ? (
                <ChevronUp className="w-6 h-6" />
              ) : (
                <ChevronDown className="w-6 h-6" />
              )}
            </button>

            {showAdvanced && (
              <div className="px-6 md:px-8 pb-6 md:pb-8 space-y-6 border-t border-dark-800 pt-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Tone
                    </label>
                    <select
                      value={formData.tone}
                      onChange={(e) =>
                        setFormData({ ...formData, tone: e.target.value })
                      }
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition">
                      <option value="professional">Professional</option>
                      <option value="casual">Casual</option>
                      <option value="technical">Technical</option>
                    </select>
                    <p className="text-xs text-dark-400 mt-1">
                      The overall tone and formality of the writing
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Writing Style
                    </label>
                    <select
                      value={formData.writing_style}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          writing_style: e.target.value,
                        })
                      }
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition">
                      <option value="">Auto</option>
                      <option value="informative">Informative</option>
                      <option value="storytelling">Storytelling</option>
                      <option value="how-to">How-To Guide</option>
                      <option value="listicle">Listicle</option>
                      <option value="opinion">Opinion/Editorial</option>
                    </select>
                    <p className="text-xs text-dark-400 mt-1">
                      The structure and narrative approach
                    </p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Target Audience
                  </label>
                  <input
                    type="text"
                    value={formData.target_audience}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        target_audience: e.target.value,
                      })
                    }
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition"
                    placeholder="e.g., business professionals, general consumers"
                  />
                  <p className="text-xs text-dark-400 mt-1">
                    Who should this content be written for?
                  </p>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Content Depth
                    </label>
                    <select
                      value={formData.content_depth}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          content_depth: e.target.value,
                        })
                      }
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition">
                      <option value="overview">Overview</option>
                      <option value="moderate">Moderate</option>
                      <option value="comprehensive">Comprehensive</option>
                    </select>
                    <p className="text-xs text-dark-400 mt-1">
                      How detailed should the content be?
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      SEO Focus Level
                    </label>
                    <select
                      value={formData.seo_focus}
                      onChange={(e) =>
                        setFormData({ ...formData, seo_focus: e.target.value })
                      }
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                    <p className="text-xs text-dark-400 mt-1">
                      Balance between SEO and natural readability
                    </p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-3">
                    Include Sections
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {[
                      { value: 'case_studies', label: 'Case Studies' },
                      { value: 'statistics', label: 'Statistics' },
                      { value: 'expert_quotes', label: 'Expert Quotes' },
                      { value: 'faqs', label: 'FAQs' },
                      { value: 'call_to_action', label: 'Call to Action' },
                    ].map((section) => (
                      <label
                        key={section.value}
                        className="flex items-center space-x-3 p-3 bg-dark-800/50 rounded-lg cursor-pointer hover:bg-dark-800 transition">
                        <input
                          type="checkbox"
                          checked={formData.include_sections.includes(
                            section.value
                          )}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setFormData({
                                ...formData,
                                include_sections: [
                                  ...formData.include_sections,
                                  section.value,
                                ],
                              });
                            } else {
                              setFormData({
                                ...formData,
                                include_sections:
                                  formData.include_sections.filter(
                                    (s) => s !== section.value
                                  ),
                              });
                            }
                          }}
                          className="w-5 h-5 text-primary-500 bg-dark-800 border-dark-700 rounded focus:ring-primary-500"
                        />
                        <span className="text-sm font-medium">
                          {section.label}
                        </span>
                      </label>
                    ))}
                  </div>
                  <p className="text-xs text-dark-400 mt-2">
                    Select specific sections to include in your blog
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Custom Instructions
                  </label>
                  <textarea
                    value={formData.custom_instructions}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        custom_instructions: e.target.value,
                      })
                    }
                    rows={4}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg focus:outline-none focus:border-primary-500 transition resize-none"
                    placeholder="Any specific requirements or guidelines for the blog..."
                  />
                  <p className="text-xs text-dark-400 mt-1">
                    Provide any additional context or specific requirements
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end space-x-4 pb-8">
            <Link
              href="/dashboard"
              className="px-6 py-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition font-medium">
              Cancel
            </Link>
            <button
              type="submit"
              disabled={createJobMutation.isPending}
              className="gradient-primary px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition disabled:opacity-50 flex items-center space-x-2">
              {createJobMutation.isPending ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Creating...</span>
                </>
              ) : (
                <span>Create Blog</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
