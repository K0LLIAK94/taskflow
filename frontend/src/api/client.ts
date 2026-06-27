import axios from "axios"

import type { Board, Card } from "../types"

const api = axios.create({ baseURL: "/api" })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export async function login(email: string, password: string): Promise<string> {
  const form = new URLSearchParams()
  form.set("username", email)
  form.set("password", password)
  const { data } = await api.post("/auth/login", form)
  localStorage.setItem("token", data.access_token)
  return data.access_token
}

export async function getBoard(id: number): Promise<Board> {
  const { data } = await api.get(`/boards/${id}`)
  return data
}

export async function moveCard(
  cardId: number,
  columnId: number,
  position: number,
): Promise<Card> {
  const { data } = await api.patch(`/cards/${cardId}/move`, {
    column_id: columnId,
    position,
  })
  return data
}
