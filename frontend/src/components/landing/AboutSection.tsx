import { BarChart3, ShieldCheck, TrendingUp, Wallet } from "lucide-react";

export function AboutSection() {
  return (
    <section className="w-full max-w-6xl mx-auto py-24 grid md:grid-cols-2 gap-16 items-center">

      {/* LEFT SIDE IMAGES */}
      <div className="relative flex justify-center">

        <img
          src="public/finance3.jpg"
          className="rounded-xl shadow-xl w-[420px]"
        />

        <img
          src="public/finance2.jpg"
          className="absolute -left-12 top-10 w-[200px] rounded-xl shadow-lg"
        />

        <img
          src="public/finance1.jpg"
          className="absolute right-0 bottom-[-20px] w-[180px] rounded-xl shadow-lg"
        />

      </div>

      {/* RIGHT SIDE CONTENT */}
      <div>

        <p className="text-purple-600 font-semibold mb-2 uppercase text-sm">
          Giải pháp
        </p>

        <h2 className="text-4xl font-bold text-gray-900 mb-8">
          Công cụ AI giúp đầu tư thông minh hơn
        </h2>

        <div className="space-y-8">

          <Feature
            icon={<BarChart3 />}
            title="Phân tích danh mục đầu tư"
            desc="Hiểu rõ mức độ đa dạng hóa, phân bổ theo ngành và hiệu suất danh mục của bạn ngay lập tức."
          />

          <Feature
            icon={<TrendingUp />}
            title="Insight thị trường"
            desc="Đặt câu hỏi về cổ phiếu, xu hướng thị trường và các tín hiệu kinh tế vĩ mô để nhận phân tích từ AI."
          />

          <Feature
            icon={<ShieldCheck />}
            title="Đánh giá rủi ro"
            desc="Phân tích độ biến động, rủi ro tập trung và các khả năng sụt giảm của danh mục đầu tư."
          />

          <Feature
            icon={<Wallet />}
            title="Tái cân bằng thông minh"
            desc="AI đề xuất điều chỉnh danh mục nhằm tối ưu hóa hiệu quả và tăng trưởng dài hạn."
          />

        </div>

      </div>
    </section>
  );
}

function Feature({
  icon,
  title,
  desc,
}: {
  icon: React.ReactNode;
  title: string;
  desc: string;
}) {
  return (
    <div className="flex gap-4">

      <div className="bg-purple-100 text-purple-600 p-3 rounded-lg">
        {icon}
      </div>

      <div>
        <h4 className="font-semibold text-lg">{title}</h4>
        <p className="text-gray-500 text-sm">{desc}</p>
      </div>

    </div>
  );
}