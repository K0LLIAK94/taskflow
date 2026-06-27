import { useDroppable } from "@dnd-kit/core"

import type { Column } from "../types"
import { CardItem } from "./CardItem"

export function ColumnView({ column }: { column: Column }) {
  const { setNodeRef, isOver } = useDroppable({ id: column.id })
  return (
    <div
      ref={setNodeRef}
      className="column"
      style= outline: isOver ? "2px solid #4c9aff" : "none" 
    >
      <h3>{column.title}</h3>
      <div className="cards">
        {column.cards
          .slice()
          .sort((a, b) => a.position - b.position)
          .map((card) => (
            <CardItem key={card.id} card={card} />
          ))}
      </div>
    </div>
  )
}
