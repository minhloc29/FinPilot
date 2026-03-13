const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {

  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export { request };