import { BoardView } from "./components/BoardView"

export default function App() {
  // Для демо используется доска с id = 1.
  return (
    <div className="app">
      <BoardView boardId={1} />
    </div>
  )
}
