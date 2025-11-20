import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { blogsAPI } from '@/services/api';
import toast from 'react-hot-toast';
import { Download, ArrowLeft } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function BlogDetailPage() {
  const { id } = useParams();
  const { data: blog, isLoading } = useQuery({
    queryKey: ['blog', id],
    queryFn: () => blogsAPI.get(Number(id)),
  });

  const handleDownload = async (format: 'markdown' | 'pdf') => {
    try {
      const blob = format === 'markdown'
        ? await blogsAPI.downloadMarkdown(Number(id))
        : await blogsAPI.downloadPDF(Number(id));

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${blog?.title}.${format === 'markdown' ? 'md' : 'pdf'}`;
      a.click();
      toast.success(`Downloaded as ${format.toUpperCase()}`);
    } catch (error) {
      toast.error('Download failed');
    }
  };

  if (isLoading) return <div className="min-h-screen bg-dark-950 text-white p-8">Loading...</div>;
  if (!blog) return <div className="min-h-screen bg-dark-950 text-white p-8">Blog not found</div>;

  return (
    <div className="min-h-screen bg-dark-950 text-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Link to="/blogs" className="inline-flex items-center space-x-2 text-dark-300 hover:text-white mb-6">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Blogs</span>
        </Link>

        <div className="bg-dark-900 rounded-2xl border border-dark-800 p-8">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">{blog.title}</h1>
              <p className="text-dark-400">
                {blog.word_count} words · {blog.reading_time_minutes} min read
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleDownload('markdown')}
                className="p-2 bg-dark-800 hover:bg-dark-700 rounded-lg transition"
                title="Download Markdown"
              >
                <Download className="w-5 h-5" />
              </button>
              <button
                onClick={() => handleDownload('pdf')}
                className="p-2 bg-dark-800 hover:bg-dark-700 rounded-lg transition"
                title="Download PDF"
              >
                <Download className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="prose prose-invert prose-lg max-w-none">
            <ReactMarkdown>{blog.content}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
