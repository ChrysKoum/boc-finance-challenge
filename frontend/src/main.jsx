import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "";

function createCorrelationId() {
  if (crypto.randomUUID) {
    return crypto.randomUUID();
  }

  return `demo-${Date.now()}`;
}

function App() {
  const [question, setQuestion] = useState("How do I save money?");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const endpoint = useMemo(() => {
    return `${apiBaseUrl}/api/v1/finance/ask`;
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) {
      setError("Please enter a question.");
      setResponse(null);
      return;
    }

    const correlationId = createCorrelationId();

    setIsLoading(true);
    setError("");

    try {
      const apiResponse = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          correlationId,
          question: trimmedQuestion,
        }),
      });

      if (!apiResponse.ok) {
        throw new Error(`Request failed with status ${apiResponse.status}`);
      }

      setResponse(await apiResponse.json());
    } catch (requestError) {
      setError(requestError.message || "Request failed.");
      setResponse(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <section className="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center px-5 py-10">
        <div className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">
            Optional live demo
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-normal text-slate-950 sm:text-4xl">
            Finance guidance API
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
            A small frontend for manually testing the FastAPI challenge service.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
        >
          <label htmlFor="question" className="block text-sm font-medium text-slate-800">
            Question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows="4"
            className="mt-2 block w-full resize-none rounded-md border border-slate-300 px-3 py-2 text-base leading-6 outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
            placeholder="Ask a simple financial question"
          />

          <div className="mt-4 flex items-center justify-between gap-3">
            <span className="text-sm text-slate-500">
              POST /api/v1/finance/ask
            </span>
            <button
              type="submit"
              disabled={isLoading}
              className="min-w-28 rounded-md bg-emerald-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            >
              {isLoading ? "Sending" : "Submit"}
            </button>
          </div>
        </form>

        {(response || error) && (
          <section className="mt-5 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-base font-semibold text-slate-950">Response</h2>

            {error && <p className="mt-3 text-sm leading-6 text-red-700">{error}</p>}

            {response && (
              <dl className="mt-4 grid gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    blocked
                  </dt>
                  <dd className="mt-1 text-lg font-semibold text-slate-950">
                    {String(response.blocked)}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    correlationId
                  </dt>
                  <dd className="mt-1 break-all text-sm font-medium text-slate-800">
                    {response.correlationId}
                  </dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    answer
                  </dt>
                  <dd className="mt-1 text-base leading-7 text-slate-800">
                    {response.answer}
                  </dd>
                </div>
              </dl>
            )}
          </section>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
