import { request } from "./client";

export interface Holding {
  id: number
  ticker: string
  shares: number
  average_cost?: number
  current_value?: number
}

export interface Portfolio {
  id: string
  user_id: string
  name: string
  holdings: {
    symbol: string
    shares: number
    average_cost?: number
  }[]
  created_at: string
  total_value?: number
}

export async function createPortfolio(
  data: {
    name: string
    description?: string
    holdings: {
      symbol: string
      shares: number
      average_cost?: number
    }[]
  },
  token: string
) {
  return request<Portfolio>("/api/v1/portfolio", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  })
}

export async function getPortfolios(token: string) {
  return request<Portfolio[]>("/api/v1/portfolios", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export async function getPortfolio(id: number, token: string) {
  return request<Portfolio>(`/api/v1/portfolio/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export async function addHolding(
  portfolioId: number,
  holding: {
    symbol: string
    shares: number
    average_cost?: number
  },
  token: string
) {
  return request<Holding>(
    `/api/v1/portfolio/${portfolioId}/holdings`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(holding)
    }
  )
}

export async function deleteHolding(
  holdingId: number,
  token: string
) {
  return request<void>(`/api/v1/holdings/${holdingId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}