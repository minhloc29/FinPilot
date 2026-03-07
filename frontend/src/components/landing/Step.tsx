interface Props {
  number: string
  title: string
  desc: string
}

export function Step({ number, title, desc }: Props) {
  return (
    <div>

      <div className="text-3xl font-bold text-purple-600 mb-2">
        {number}
      </div>

      <h3 className="font-semibold mb-2">
        {title}
      </h3>

      <p className="text-sm text-gray-500">
        {desc}
      </p>

    </div>
  )
}