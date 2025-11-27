export default function HomePage() {
  return (
    <div className="py-20 text-center">
      <h1 className="text-5xl font-bold mb-6">PaperScout</h1>
      <p className="text-xl text-gray-600">
        A research search engine powered by embeddings.
      </p>

      <div className="mt-10">
        <a
          href="/search"
          className="bg-black text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-gray-800"
        >
          Start Searching →
        </a>
      </div>
    </div>
  );
}
