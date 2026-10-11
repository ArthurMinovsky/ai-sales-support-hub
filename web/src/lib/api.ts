export interface Product {
  id: number;
  name: string;
  brand: string;
  description: string;
  image_url: string | null;
  category: string;
  type: string;
  subtype: string;
  created_at: string;
  updated_at: string;
}
export type ProductInput = Pick<Product, "name" | "brand" | "description" | "image_url" | "category" | "type" | "subtype">;
export interface Recommendation { product_id: number; product: Product; reason: string }
export interface SearchResponse { suggestions: Recommendation[]; notice?: string | null }

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) { super(message); }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api/backend/${path}`, {
    ...init, cache: "no-store", headers: { "Content-Type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    if (response.status === 401 && typeof window !== "undefined") window.location.assign("/login");
    throw new ApiError(response.status, error.message || (typeof error.detail === "string" && error.detail) || `Request failed (${response.status})`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
