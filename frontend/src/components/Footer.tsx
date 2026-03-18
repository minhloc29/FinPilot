import { Facebook, Linkedin, Twitter, Mail, MapPin } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-[#1e1b3a] text-white mt-24">
      <div className="max-w-7xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-4 gap-10">

        {/* Logo + Description */}
        <div>
          <h3 className="text-2xl font-bold">AlphaLens</h3>

          <p className="text-sm text-gray-300 mt-4 leading-relaxed">
            AlphaLens is an AI-powered investment assistant that helps you
            analyze portfolios, assess risks, and discover market opportunities.
          </p>

          {/* Social icons */}
          <div className="flex gap-4 mt-6">
            <div className="bg-white/10 p-2 rounded-md">
              <Facebook size={18} />
            </div>
            <div className="bg-white/10 p-2 rounded-md">
              <Linkedin size={18} />
            </div>
            <div className="bg-white/10 p-2 rounded-md">
              <Twitter size={18} />
            </div>
          </div>
        </div>

        {/* Product */}
        <div>
          <h4 className="text-lg font-semibold mb-4">Product</h4>

          <ul className="space-y-3 text-gray-300 text-sm">
            <li>Portfolio Analysis</li>
            <li>Market Insights</li>
            <li>Risk Assessment</li>
            <li>Rebalancing</li>
          </ul>
        </div>

        {/* Resources */}
        <div>
          <h4 className="text-lg font-semibold mb-4">Resources</h4>

          <ul className="space-y-3 text-gray-300 text-sm">
            <li>Documentation</li>
            <li>Blog</li>
            <li>Pricing</li>
            <li>Terms & Conditions</li>
          </ul>
        </div>

        {/* Contact */}
        <div>
          <h4 className="text-lg font-semibold mb-4">Contact</h4>

          <div className="space-y-3 text-gray-300 text-sm">

            <div className="flex items-center gap-2">
              <MapPin size={16} />
              Ha Noi, Vietnam
            </div>

            <div className="flex items-center gap-2">
              <Mail size={16} />
              contact@alphalens.ai
            </div>

          </div>
        </div>
      </div>

      {/* Bottom */}
      <div className="border-t border-white/10 text-center text-sm py-6 text-gray-400">
        © 2026 AlphaLens. All Rights Reserved
      </div>
    </footer>
  )
}