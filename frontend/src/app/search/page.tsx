"use client";

import { useState } from "react";
import PaperCard from "@/components/PaperCard";
import PaperSkeletonCard from "@/components/PaperSkeletonCard";

interface PaperResult {
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
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<PaperResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (!query.trim() || loading) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const res = await fetch(
        `http://localhost:8000/papers/search/hybrid?query=${encodeURIComponent(
          query
        )}`
      );

      if (!res.ok) throw new Error(`Backend error: ${res.status}`);

      const data = await res.json();
      setResults(data.results || []);
    } catch (err: any) {
      console.error("Search error:", err);
      setError(err.message || "Search failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Search Papers</h1>

      {/* Search bar */}
      <div className="flex gap-3 mb-8">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          placeholder="e.g. transformer models"
          className="flex-1 border px-4 py-2 rounded-lg"
          autoFocus
        />

        <button
          onClick={handleSearch}
          disabled={!query.trim() || loading}
          className={`px-6 py-2 rounded-lg text-white ${
            !query.trim() || loading
              ? "bg-gray-400"
              : "bg-black hover:bg-gray-800"
          }`}
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </div>

      {/* Error box */}
      {error && (
        <div className="p-3 mb-6 bg-red-100 text-red-700 border rounded">
          {error}
        </div>
      )}

      {/* Loading skeletons */}
      {loading && (
        <div className="space-y-6">
          {Array.from({ length: 5 }).map((_, i) => (
            <PaperSkeletonCard key={i} />
          ))}
        </div>
      )}

      {/* No results */}
      {!loading && !error && results.length === 0 && query.trim() && (
        <div className="text-gray-500 mt-6">No papers found.</div>
      )}

      {/* Results */}
      {!loading && !error && results.length > 0 && (
        <div className="space-y-6 animate-fadeIn">
          {results.map((paper) => (
            <PaperCard key={paper.id} {...paper} />
          ))}
        </div>
      )}
    </div>
  );
}