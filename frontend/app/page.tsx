'use client';

import { useState } from 'react';
import HeaderNav from '@/components/HeaderNav';

export default function Page() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const res = await fetch('http://localhost:8000/query-laws', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inquiry: query }),
      });

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      const data = await res.json();
      // Adjust this if your API response shape is different
      setAnswer(data.answer ?? JSON.stringify(data, null, 2));
    } catch (err: any) {
      setError(err.message ?? 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <HeaderNav signOut={() => {}} />
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-4 py-10">
        <h1 className="text-2xl font-semibold text-gray-900">
          Query Laws
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <label className="text-sm font-medium text-gray-700">
            Enter your legal question
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. What happens if I steal?"
            className="rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="mt-1 inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
          >
            {loading ? 'Querying…' : 'Submit'}
          </button>
        </form>

        {error && (
          <p className="text-sm text-red-600">
            {error}
          </p>
        )}

        {answer && (
          <section className="rounded-md border border-gray-200 bg-white p-4 text-sm shadow-sm">
            <h2 className="mb-2 text-base font-semibold text-gray-900">
              Answer
            </h2>
            <pre className="whitespace-pre-wrap break-words text-gray-800">
              {answer}
            </pre>
          </section>
        )}
      </main>
    </div>
  );
}
