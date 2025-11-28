"use client";

import { useState } from "react";
import PaperCard from "@/components/PaperCard";
import PaperSkeletonCard from "@/components/PaperSkeletonCard";
import type { PaperResult, SearchResponse } from "@/lib/api";
import { searchPapers, triggerIngestionAndWait } from "@/lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<PaperResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState("final_score"); // Default sorting option

  async function handleSearch(performIngestion: boolean = true, sortOption: string = sortBy) {
    if (!query.trim() || loading) return;

    setLoading(true);
    setError(null);
    if (performIngestion) setResults([]);

    try {
      if (performIngestion) {
        // 1) ingest exactly 1 page for this query
        await triggerIngestionAndWait(query, 1);
      }

      // 2) run hybrid search with sorting
      const data: SearchResponse = await searchPapers(query, sortOption);
      setResults(data.results || []);
    } catch (err: any) {
      console.error("Search/ingestion error:", err);
      setError(err.message ?? "Search failed");
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
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          placeholder="e.g. transformer models"
          className="flex-1 border px-4 py-2 rounded-lg"
          autoFocus
        />
        <button
          onClick={() => handleSearch()}
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-300 cursor-pointer"
        >
          Search
        </button>
      </div>

      {/* Sorting Dropdown */}
      <div className="mb-4">
        <label htmlFor="sort" className="mr-2 text-sm font-medium">
          Sort by:
        </label>
        <select
          id="sort"
          value={sortBy}
          onChange={(e) => {
            const newSortBy = e.target.value;
            setSortBy(newSortBy);
            handleSearch(false, newSortBy); // Pass the new sort option directly
          }}
          className="border px-2 py-1 rounded-lg text-sm"
        >
          <option value="published_year">Publication Year</option>
          <option value="citation_count">Citation Count</option>
          <option value="distance">Relevancy</option>
          <option value="final_score">Total Score</option>
        </select>
      </div>

      {loading && <p className="text-gray-600">Searching…</p>}
      {loading && (
        <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-gray-300 mx-auto"></div>
      )}
      <div className="space-y-6">
        {results.map((paper) => (
          <PaperCard key={paper.id} {...paper} />
        ))}
      </div>
    </div>
  );
}
