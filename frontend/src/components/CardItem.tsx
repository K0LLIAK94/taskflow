import type { CSSProperties } from "react"
import { useDraggable } from "@dnd-kit/core"

import type { Card } from "../types"

export function CardItem({ card }: { card: Card }) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: card.id,
  })
  const style: CSSProperties = {
    transform: transform
      ? `translate(${transform.x}px, ${transform.y}px)`
      : undefined,
  }
  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="card"
    >
      <strong>{card.title}</strong>
      {card.description && <p>{card.description}</p>}
      <div className="labels">
        {card.labels.map((l) => {
          const labelStyle: CSSProperties = { backgroundColor: l.color }
          return (
            <span key={l.id} style={labelStyle} className="label">
              {l.name}
            </span>
          )
        })}
      </div>
    </div>
  )
}
