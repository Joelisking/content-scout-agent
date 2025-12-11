'use client';

import Link from 'next/link';
import { useAuthStore } from '@/stores/authStore';
import { ArrowLeft, CreditCard } from 'lucide-react';

export default function SettingsPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="min-h-screen bg-dark-950 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link href="/dashboard" className="inline-flex items-center space-x-2 text-dark-300 hover:text-white mb-6">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </Link>

        <h1 className="text-3xl font-bold mb-8">Settings</h1>

        <div className="space-y-6">
          <div className="bg-dark-900 p-6 rounded-xl border border-dark-800">
            <h2 className="text-xl font-semibold mb-4">Account Information</h2>
            <div className="space-y-3 text-dark-300">
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Name:</strong> {user?.full_name}</p>
              <p><strong>Country:</strong> {user?.country}</p>
              <p><strong>Plan:</strong> <span className="capitalize">{user?.subscription_tier}</span></p>
            </div>
          </div>

          <div className="bg-dark-900 p-6 rounded-xl border border-dark-800">
            <h2 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <CreditCard className="w-6 h-6" />
              <span>Subscription</span>
            </h2>
            <p className="text-dark-300 mb-4">
              You are currently on the <span className="capitalize font-semibold">{user?.subscription_tier}</span> plan.
            </p>
            <Link
              href="/pricing"
              className="gradient-primary px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition inline-block"
            >
              Upgrade Plan
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
