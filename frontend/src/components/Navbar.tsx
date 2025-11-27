"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full border-b bg-white/70 backdrop-blur py-3">
      <div className="max-w-5xl mx-auto px-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold">
          PaperScout
        </Link>
        <div className="space-x-6 text-sm">
          <Link href="/search" className="hover:underline">
            Search
          </Link>
          <Link href="/ingest" className="hover:underline">
            Ingestion
          </Link>
        </div>
      </div>
    </nav>
  );
}
