// src/lib/api.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not set in .env.local");
}

// -------- generic helpers --------

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error(`API GET ${path} failed: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export async function apiPost<T>(path: string, body?: any): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    throw new Error(`API POST ${path} failed: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

// -------- types --------

export interface PaperResult {
  id: number;
  title: string;
  abstract: string | null;
  url: string | null;
  published_year: number | null;
  citation_count: number;
  distance: number;
  recency_score: number;
  popularity_score: number;
  final_score: number;
  authors?: { name: string }[];
  fields?: { name: string }[];
}

export interface SearchResponse {
  query: string;
  results: PaperResult[];
}

export interface IngestionResult {
  added: number;
  pages_processed: number;
  log_id: number;
}

// -------- endpoint helpers --------

// run hybrid search
export async function searchPapers(query: string, sortBy: string): Promise<SearchResponse> {
  return apiGet(
    `/papers/search/hybrid?query=${encodeURIComponent(query)}&sort_by=${encodeURIComponent(sortBy)}`
  );
}

// trigger ingestion for given query and pages
export async function triggerIngestion(
  query: string,
  pages: number = 1
): Promise<IngestionResult> {
  return apiPost(
    `/papers/ingest?query=${encodeURIComponent(query)}&pages=${pages}`
  );
}

export async function triggerIngestionAndWait(
  query: string,
  pages: number = 1
) {
  return apiPost(
    `/papers/ingest_and_wait?query=${encodeURIComponent(query)}&pages=${pages}`
  );
}

// --- logs ---
export async function getIngestionLogs() {
  const res = await fetch(`${API_URL}/ingestion/logs`);

  if (!res.ok) throw new Error("Failed to fetch logs");

  return res.json();
}