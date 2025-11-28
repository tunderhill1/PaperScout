"use client";

import { useState, useEffect } from "react";
import { triggerIngestion, getIngestionLogs } from "@/lib/api";

export default function IngestionPage() {
  const [query, setQuery] = useState("");
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [logs, setLogs] = useState<any[]>([]);

  async function runIngestion() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await triggerIngestion(query, pages);
      setResult(res);
      loadLogs();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadLogs() {
    try {
      const data = await getIngestionLogs();
      setLogs(data);
    } catch (err) {}
  }

  useEffect(() => {
    loadLogs();
  }, []);

  return (
    <div className="max-w-3xl mx-auto space-y-10">
      <h1 className="text-3xl font-bold">Ingestion Console</h1>

      {/* FORM */}
      <div className="bg-white/5 border border-white/10 p-6 rounded-xl">
        <h2 className="text-xl font-semibold mb-4">Run Ingestion to speed up searches</h2>

        <div className="space-y-4">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search term (e.g. transformer models)"
            className="w-full border px-4 py-2 rounded-lg bg-black/20 text-white"
          />
          <input
            type="number"
            value={pages}
            min={1}
            max={10}
            onChange={(e) => setPages(Number(e.target.value))}
            className="w-32 border px-4 py-2 rounded-lg bg-black/20 text-white"
          />

          <button
            onClick={runIngestion}
            disabled={!query || loading}
            className={`px-5 py-2 rounded-lg text-white font-medium ${
              loading || !query
                ? "bg-gray-600 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {loading ? "Ingesting..." : "Start Ingestion"}
          </button>

          {error && (
            <p className="text-red-400 mt-2">{error}</p>
          )}

          {result && (
            <div className="mt-4 text-green-400">
              ✅ Added {result.added} papers (processed {result.pages_processed} pages)
            </div>
          )}
        </div>
      </div>

      {/* LOGS */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Last 20 Ingestion Logs</h2>

        <div className="overflow-x-auto">
          <table className="min-w-full bg-black/20 border border-white/10 rounded-xl">
            <thead>
              <tr className="text-left bg-white/5">
                <th className="px-4 py-2">ID</th>
                <th className="px-4 py-2">Query</th>
                <th className="px-4 py-2">Pages</th>
                <th className="px-4 py-2">Num Added</th>
                <th className="px-4 py-2">Timestamp</th>
              </tr>
            </thead>

            <tbody>
              {logs.map((log) => (
                <tr
                  key={log.id}
                  className="border-t border-white/10 hover:bg-white/5 transition"
                >
                  <td className="px-4 py-2 text-sm">{log.id}</td>
                  <td className="px-4 py-2 text-sm">{log.query}</td>
                  <td className="px-4 py-2 text-sm">{log.pages}</td>
                  <td className="px-4 py-2 text-sm">{log.added}</td>
                  <td className="px-4 py-2 text-sm">
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}

              {logs.length === 0 && (
                <tr>
                  <td className="px-4 py-4 text-gray-400" colSpan={5}>
                    No logs found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}