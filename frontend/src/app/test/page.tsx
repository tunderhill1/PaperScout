// src/app/test/page.tsx
"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function TestPage() {
  const [response, setResponse] = useState<any>(null);

  useEffect(() => {
    apiGet("/health")
      .then(setResponse)
      .catch((err) => setResponse({ error: err.message }));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">API connection test</h1>
      <pre className="bg-gray-900 text-white p-4 rounded">
        {JSON.stringify(response, null, 2)}
      </pre>
    </div>
  );
}
