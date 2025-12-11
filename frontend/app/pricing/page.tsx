import Link from 'next/link';
import { CheckCircle2 } from 'lucide-react';

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-dark-950 text-white py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-dark-300">Choose the plan that fits your needs</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <PricingCard
            name="Free"
            price="$0"
            features={['3 blogs per month', 'Basic research', 'Markdown export', 'Email notifications']}
            cta="Get Started"
            ctaLink="/register"
          />
          <PricingCard
            name="Starter"
            price="$29"
            features={['20 blogs per month', 'Standard research', 'Markdown & PDF export', 'Email notifications', 'Priority support']}
            cta="Upgrade"
            ctaLink="/settings"
            highlighted
          />
          <PricingCard
            name="Pro"
            price="$99"
            features={['Unlimited blogs', 'Deep research', 'All export formats', 'Priority support', 'Custom branding']}
            cta="Upgrade"
            ctaLink="/settings"
          />
        </div>
      </div>
    </div>
  );
}

function PricingCard({ name, price, features, cta, ctaLink, highlighted = false }: any) {
  return (
    <div className={`bg-dark-900 p-8 rounded-2xl border ${highlighted ? 'border-primary-500' : 'border-dark-800'}`}>
      {highlighted && <div className="text-primary-500 text-sm font-semibold mb-4">MOST POPULAR</div>}
      <h3 className="text-2xl font-bold mb-2">{name}</h3>
      <div className="text-4xl font-bold mb-6">
        {price}<span className="text-lg text-dark-400">/mo</span>
      </div>
      <ul className="space-y-3 mb-8">
        {features.map((feature: string, i: number) => (
          <li key={i} className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-primary-500 shrink-0" />
            <span className="text-dark-200">{feature}</span>
          </li>
        ))}
      </ul>
      <Link
        href={ctaLink}
        className={`block text-center px-6 py-3 rounded-lg font-semibold transition ${
          highlighted ? 'gradient-primary hover:opacity-90' : 'bg-dark-800 hover:bg-dark-700'
        }`}
      >
        {cta}
      </Link>
    </div>
  );
}
