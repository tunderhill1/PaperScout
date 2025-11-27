"use client";

import { useState } from "react";
import PaperCard from "@/components/PaperCard";

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

  async function handleSearch() {
    if (!query.trim()) return;

    setLoading(true);
    setResults([]);

    try {
      const res = await fetch(
        `http://localhost:8000/papers/search/hybrid?query=${encodeURIComponent(
          query
        )}`
      );

      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Search Papers</h1>

      <div className="flex gap-3 mb-8">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. transformer models"
          className="flex-1 border px-4 py-2 rounded-lg"
        />
        <button
          onClick={handleSearch}
          className="bg-black text-white px-6 py-2 rounded-lg"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-600">Searching…</p>}

      <div className="space-y-6">
        {results.map((paper) => (
          <PaperCard key={paper.id} {...paper} />
        ))}
      </div>
    </div>
  );
}
