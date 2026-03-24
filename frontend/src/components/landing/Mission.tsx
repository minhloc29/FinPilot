export function MissionVision() {
  return (
    <section className="w-full py-24 bg-background">
      <div className="max-w-6xl mx-auto px-4 space-y-16">

        {/* ================= IMAGE COLLAGE ================= */}
        <div className="relative h-[300px] flex justify-center items-center">

  <img src="/public/finance4.jpg"
    className="absolute w-56 h-72 object-cover rounded-xl shadow-xl z-10" />

  <img src="/public/finance1.jpg"
    className="absolute left-0 top-20 w-40 h-28 rounded-xl shadow-md" />

  <img src="/public/finance3.jpg"
    className="absolute right-0 top-20 w-40 h-28 rounded-xl shadow-md" />

  <img src="/public/finance5.jpg"
    className="absolute right-10 bottom-0 w-44 h-32 rounded-xl shadow-md" />

</div>
        {/* ================= TEXT SECTION ================= */}
        <div className="grid md:grid-cols-2 gap-12">

          {/* Mission */}
          <div>
            <p className="text-sm font-semibold text-primary uppercase tracking-wide mb-2">
              Sứ mệnh
            </p>

            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Xây dựng trợ lý tài chính AI cá nhân hóa
            </h2>

            <p className="text-muted-foreground leading-relaxed">
              Chúng tôi giúp mọi người đưa ra quyết định tài chính tốt hơn bằng cách
              cung cấp các chiến lược đầu tư được cá nhân hóa dựa trên dữ liệu thực tế.
              FinAssist không chỉ phân tích danh mục đầu tư, mà còn tối ưu hóa
              chiến lược theo mục tiêu và mức độ chấp nhận rủi ro của từng người dùng.
            </p>
          </div>

          {/* Vision */}
          <div>
            <p className="text-sm font-semibold text-primary uppercase tracking-wide mb-2">
              Tầm nhìn
            </p>

            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Trở thành nền tảng AI tài chính hàng đầu
            </h2>

            <p className="text-muted-foreground leading-relaxed">
              Chúng tôi hướng tới việc xây dựng một hệ sinh thái nơi AI có thể hỗ trợ
              mọi người quản lý tài sản, tối ưu danh mục đầu tư và ra quyết định tài chính
              một cách thông minh, minh bạch và dễ tiếp cận cho tất cả mọi người.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}