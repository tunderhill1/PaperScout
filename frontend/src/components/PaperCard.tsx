import Link from "next/link";
import { scoreToTen } from "@/lib/score";

interface PaperCardProps {
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
  fields?: { name: string }[]; // optional, future expansion
  authors?: { name: string }[];
}

export default function PaperCard({
  title,
  abstract,
  url,
  published_year,
  citation_count,
  distance,
  final_score,
  fields = [],
  authors = [],
}: PaperCardProps) {
  return (
    <div className="border rounded-xl p-6 bg-white shadow-sm hover:shadow-md transition">
        {/* TITLE */}
        <h2 className="text-xl font-semibold leading-snug text-gray-900 group-hover:text-black">
          {title}
        </h2>

      {/* AUTHORS */}
      {authors.length > 0 && (
        <p className="text-sm text-gray-500 mt-1">
          {authors.slice(0, 4).map((a) => a.name).join(", ")}
          {authors.length > 4 ? " et al." : ""}
        </p>
      )}

      {/* FIELDS */}
      <div className="flex flex-wrap gap-2 mt-3">
        {fields.map((field) => (
          <span
            key={field.name}
            className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-md"
          >
            {field.name}
          </span>
        ))}
      </div>

      {/* ABSTRACT */}
      {abstract && (
        <p className="text-gray-700 mt-3 line-clamp-3">{abstract}</p>
      )}

      {/* METRICS */}
      <div className="flex gap-4 text-sm text-gray-600 mt-4">
        <span>📅 {published_year ?? "N/A"}</span>
        <span>📈 {citation_count} citations</span>
        <span>🔍 relevancy: {scoreToTen(distance).toFixed(2)} / 10</span>
        <span>⭐ total score: {scoreToTen(final_score).toFixed(1)} / 10</span>
      </div>

      {/* LINK */}
      {url && (
        <Link
          href={url}
          target="_blank"
          className="mt-4 inline-block text-sm text-indigo-600 underline"
        >
          View paper →
        </Link>
      )}
    </div>
  );
}
