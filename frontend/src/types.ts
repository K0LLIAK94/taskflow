export interface Label {
  id: number
  name: string
  color: string
}

export interface Card {
  id: number
  title: string
  description: string
  position: number
  column_id: number
  labels: Label[]
}

export interface Column {
  id: number
  title: string
  position: number
  cards: Card[]
}

export interface Board {
  id: number
  title: string
  columns: Column[]
}
