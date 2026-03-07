interface Props {
  title: string
  desc: string
}

export function FeatureCard({ title, desc }: Props) {
  return (
    <div className="rounded-2xl bg-white/70 backdrop-blur-md 
    shadow-lg p-6 text-center">

      <h3 className="font-semibold text-lg mb-2">
        {title}
      </h3>

      <p className="text-sm text-gray-500">
        {desc}
      </p>

    </div>
  )
}