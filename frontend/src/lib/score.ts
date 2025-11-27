export function scoreToTen(raw: number): number {
  // raw is ~0.0 to ~1.5 (sometimes higher for old/high-citation papers)
  // We clamp and scale to 0–10 for readability.
  const clamped = Math.max(0, Math.min(raw, 1)); // clamp 0–1
  const scaled = 10 - (clamped * 10);
  return scaled;
}