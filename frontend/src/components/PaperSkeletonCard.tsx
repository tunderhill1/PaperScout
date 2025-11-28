import Skeleton from "./Skeleton";

export default function PaperSkeletonCard() {
  return (
    <div className="p-4 bg-white border rounded-lg shadow-sm space-y-3">
      <Skeleton className="h-6 w-3/4" />

      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />

      <div className="space-y-1 pt-2">
        <Skeleton className="h-3 w-1/4" />
        <Skeleton className="h-3 w-1/3" />
      </div>

      <div className="space-y-1 pt-2">
        <Skeleton className="h-3 w-1/5" />
        <Skeleton className="h-3 w-1/5" />
        <Skeleton className="h-3 w-1/5" />
      </div>

      <Skeleton className="h-4 w-20 mt-3" />
    </div>
  );
}