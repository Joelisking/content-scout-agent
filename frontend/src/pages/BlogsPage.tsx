import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { blogsAPI } from '@/services/api';
import { FileText, Download, Calendar } from 'lucide-react';

export default function BlogsPage() {
  const { data: blogsData, isLoading } = useQuery({
    queryKey: ['blogs'],
    queryFn: () => blogsAPI.list({ page: 1, page_size: 20 }),
  });

  return (
    <div className="min-h-screen bg-dark-950 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Your Blogs</h1>

        {isLoading ? (
          <p>Loading...</p>
        ) : blogsData?.blogs?.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {blogsData.blogs.map((blog: any) => (
              <Link
                key={blog.id}
                to={`/blogs/${blog.id}`}
                className="bg-dark-900 p-6 rounded-xl border border-dark-800 hover:border-primary-500 transition"
              >
                <h3 className="text-xl font-semibold mb-3">{blog.title}</h3>
                <p className="text-dark-400 text-sm mb-4 line-clamp-2">{blog.summary}</p>
                <div className="flex items-center justify-between text-sm text-dark-500">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-4 h-4" />
                    <span>{new Date(blog.created_at).toLocaleDateString()}</span>
                  </div>
                  <div>{blog.word_count} words</div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-dark-600 mx-auto mb-4" />
            <p className="text-dark-300">No blogs yet</p>
          </div>
        )}
      </div>
    </div>
  );
}
