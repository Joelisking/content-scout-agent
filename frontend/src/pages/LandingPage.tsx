import { Link } from 'react-router-dom';
import { Sparkles, Target, Zap, Globe, CheckCircle2 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-dark-950 text-white">
      {/* Navigation */}
      <nav className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-xl fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-8 h-8 text-primary-500" />
              <span className="text-xl font-bold">Content Scout</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/pricing"
                className="text-dark-300 hover:text-white transition"
              >
                Pricing
              </Link>
              <Link
                to="/login"
                className="text-dark-300 hover:text-white transition"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="gradient-primary px-6 py-2 rounded-lg font-semibold hover:opacity-90 transition"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-black mb-6 bg-gradient-to-r from-primary-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            AI-Powered Content
            <br />
            That Converts
          </h1>
          <p className="text-xl md:text-2xl text-dark-300 mb-8 max-w-3xl mx-auto">
            Automatically research trending topics and generate SEO-optimized blog posts
            for any industry and location with the power of AI.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center gradient-primary px-8 py-4 rounded-xl text-lg font-semibold hover:opacity-90 transition shadow-lg shadow-primary-500/50"
          >
            Start Creating for Free
            <Zap className="ml-2 w-5 h-5" />
          </Link>
          <p className="text-dark-400 mt-4">No credit card required. 3 blogs free.</p>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 bg-dark-900/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Target className="w-12 h-12 text-primary-500" />}
              title="1. Choose Your Topic"
              description="Select your industry sector and target location. Add custom keywords to refine your research."
            />
            <FeatureCard
              icon={<Sparkles className="w-12 h-12 text-purple-500" />}
              title="2. AI Research"
              description="Our AI scouts the web for trending topics, popular keywords, and industry insights specific to your niche."
            />
            <FeatureCard
              icon={<Globe className="w-12 h-12 text-pink-500" />}
              title="3. Get Your Blog"
              description="Receive a fully-written, SEO-optimized blog post in minutes. Download as Markdown or PDF."
            />
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">
                Built for Growing Businesses
              </h2>
              <div className="space-y-4">
                <Benefit text="Save 10+ hours per blog post" />
                <Benefit text="Always trending and relevant content" />
                <Benefit text="SEO-optimized for better rankings" />
                <Benefit text="Export to Markdown, PDF, or HTML" />
                <Benefit text="Email notifications when ready" />
                <Benefit text="Multi-currency payment support" />
              </div>
            </div>
            <div className="bg-gradient-to-br from-primary-600 to-purple-600 rounded-2xl p-8 shadow-2xl">
              <div className="text-center">
                <h3 className="text-2xl font-bold mb-4">Perfect for:</h3>
                <div className="space-y-3 text-left">
                  <Industry>Real Estate Agencies</Industry>
                  <Industry>Marketing Agencies</Industry>
                  <Industry>SaaS Companies</Industry>
                  <Industry>E-commerce Brands</Industry>
                  <Industry>Consulting Firms</Industry>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4 bg-gradient-to-br from-primary-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Scale Your Content?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join businesses already using Content Scout to dominate their niche.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center bg-white text-primary-600 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-dark-50 transition shadow-xl"
          >
            Get Started Now
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-dark-800">
        <div className="max-w-7xl mx-auto text-center text-dark-400">
          <p>&copy; 2024 Content Scout. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-dark-800/50 p-8 rounded-2xl border border-dark-700 hover:border-primary-500 transition">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-dark-300">{description}</p>
    </div>
  );
}

function Benefit({ text }: { text: string }) {
  return (
    <div className="flex items-center space-x-3">
      <CheckCircle2 className="w-6 h-6 text-primary-500 flex-shrink-0" />
      <span className="text-dark-200">{text}</span>
    </div>
  );
}

function Industry({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center space-x-2">
      <div className="w-2 h-2 bg-white rounded-full"></div>
      <span>{children}</span>
    </div>
  );
}
