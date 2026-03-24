import { Search, Brain, Sparkles } from "lucide-react";

const STEPS = [
  {
    icon: Search,
    title: "Nhập thông tin tài chính của bạn",
    description:
      "Cung cấp thu nhập, mục tiêu và danh mục đầu tư hiện tại để bắt đầu.",
    color: "bg-orange-500",
  },
  {
    icon: Brain,
    title: "AI phân tích dữ liệu của bạn",
    description:
      "Hệ thống AI đánh giá mức độ rủi ro, danh mục và điều kiện thị trường.",
    color: "bg-indigo-500",
  },
  {
    icon: Sparkles,
    title: "Nhận đề xuất đầu tư thông minh",
    description:
      "Nhận chiến lược đầu tư cá nhân hóa và các gợi ý hành động cụ thể.",
    color: "bg-yellow-500",
  },
];

export function HowItWorks() {
  return (
    <section className="relative w-full py-24 bg-gradient-to-b from-background to-muted/30 overflow-hidden">
      <div className="max-w-6xl mx-auto px-4 text-center">

        {/* Header */}
        <p className="text-sm font-semibold text-primary uppercase tracking-wide mb-2">
          What we offer
        </p>

        <h2 className="text-3xl md:text-4xl font-bold mb-16">
          How AlphaLens Works
        </h2>

        {/* Steps container */}
        <div className="relative grid md:grid-cols-3 gap-12 items-start">

          {/* SVG Arrows */}
          <svg
            className="hidden md:block absolute top-8 left-0 w-full pointer-events-none"
            height="120"
            viewBox="0 0 1200 120"
          >
            {/* Arrow 1 */}
            <path
              d="M250,60 C350,10 450,110 550,60"
              stroke="#c7d2fe"
              strokeWidth="2"
              fill="transparent"
              markerEnd="url(#arrowhead)"
            />

            {/* Arrow 2 */}
            <path
              d="M650,60 C750,10 850,110 950,60"
              stroke="#c7d2fe"
              strokeWidth="2"
              fill="transparent"
              markerEnd="url(#arrowhead)"
            />

            {/* Arrowhead */}
            <defs>
              <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="10"
                refY="3.5"
                orient="auto"
              >
                <polygon points="0 0, 10 3.5, 0 7" fill="#c7d2fe" />
              </marker>
            </defs>
          </svg>

          {/* Steps */}
          {STEPS.map((step, i) => {
            const Icon = step.icon;

            return (
              <div
                key={i}
                className="flex flex-col items-center text-center space-y-4 relative z-10"
              >
                {/* Icon */}
                <div
                  className={`w-16 h-16 rounded-full flex items-center justify-center text-white shadow-lg ${step.color}`}
                >
                  <Icon className="w-7 h-7" />
                </div>

                {/* Title */}
                <h3 className="text-lg font-semibold">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-sm text-muted-foreground max-w-xs">
                  {step.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}