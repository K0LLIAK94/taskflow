import { DndContext, DragEndEvent } from "@dnd-kit/core"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { getBoard, moveCard } from "../api/client"
import type { Board } from "../types"
import { ColumnView } from "./ColumnView"

export function BoardView({ boardId }: { boardId: number }) {
  const qc = useQueryClient()
  const { data: board, isLoading } = useQuery<Board>({
    queryKey: ["board", boardId],
    queryFn: () => getBoard(boardId),
  })

  const move = useMutation({
    mutationFn: ({ cardId, columnId }: { cardId: number; columnId: number }) =>
      moveCard(cardId, columnId, Date.now()),
    // оптимистичное обновление
    onMutate: async ({ cardId, columnId }) => {
      await qc.cancelQueries({ queryKey: ["board", boardId] })
      const prev = qc.getQueryData<Board>(["board", boardId])
      if (prev) {
        const next: Board = structuredClone(prev)
        for (const col of next.columns) {
          const idx = col.cards.findIndex((c) => c.id === cardId)
          if (idx !== -1) {
            const [card] = col.cards.splice(idx, 1)
            card.column_id = columnId
            next.columns.find((c) => c.id === columnId)?.cards.push(card)
            break
          }
        }
        qc.setQueryData(["board", boardId], next)
      }
      return { prev }
    },
    onError: (_e, _v, ctx) => {
      if (ctx?.prev) qc.setQueryData(["board", boardId], ctx.prev)
    },
    onSettled: () => qc.invalidateQueries({ queryKey: ["board", boardId] }),
  })

  if (isLoading || !board) return <p>Загрузка…</p>

  function onDragEnd(e: DragEndEvent) {
    const cardId = Number(e.active.id)
    const columnId = e.over ? Number(e.over.id) : null
    if (columnId) move.mutate({ cardId, columnId })
  }

  return (
    <DndContext onDragEnd={onDragEnd}>
      <h1>{board.title}</h1>
      <div className="board">
        {board.columns
          .slice()
          .sort((a, b) => a.position - b.position)
          .map((col) => (
            <ColumnView key={col.id} column={col} />
          ))}
      </div>
    </DndContext>
  )
}
