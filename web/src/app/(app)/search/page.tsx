"use client";
import { FormEvent, useState } from "react";
import RecommendationResults from "@/components/RecommendationResults";
import { apiRequest, SearchResponse } from "@/lib/api";

const EXAMPLES = ["Rugged edge vision gateway for production-line defect inspection", "Wireless vibration monitoring for CNC machines and rotating equipment", "Connect PLC and historian data into our analytics platform"];
export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function search(event?: FormEvent<HTMLFormElement>) {
    event?.preventDefault(); if (query.trim().length < 3) return;
    setLoading(true);setError("");setResult(null);
    try { setResult(await apiRequest<SearchResponse>("suggestions", { method: "POST", body: JSON.stringify({ query: query.trim() }) })); }
    catch (e) { setError(e instanceof Error ? e.message : "AI temporarily unavailable"); }
    finally { setLoading(false); }
  }
  return <div className="page-wrap">
    <div className="page-header"><div><div className="eyebrow">AI-assisted discovery</div><h1>Find the right product</h1><p className="muted">Describe your customer&apos;s challenge. We&apos;ll match it with products from your catalog.</p></div></div>
    <section className="search-hero"><div className="hero-label">Customer requirements</div>
      <form onSubmit={search} className="query-form"><label htmlFor="needs">What is your customer looking for?</label><textarea id="needs" rows={5} minLength={3} maxLength={1500} value={query} onChange={e=>setQuery(e.target.value)} placeholder="e.g. We need predictive maintenance for motors and pumps at our Rayong plant…" required />
        <div className="actions end"><span className="muted">Describe requirements in your own words</span><button className="primary" type="submit" disabled={loading || query.trim().length < 3}>{loading ? "Analyzing…" : "Find products"}</button></div>
      </form>
    </section>
    <div className="examples"><span className="muted">Try an example:</span>{EXAMPLES.map(example=><button key={example} className="example" onClick={()=>setQuery(example)} type="button">{example}</button>)}</div>
    {error && <section className="content-card error-block" role="alert"><strong>AI recommendations unavailable</strong><p>{error}</p><button className="secondary" type="button" onClick={()=>void search()}>Retry</button><p className="muted">You can still manage the catalog while AI is offline.</p></section>}
    {loading && <section aria-live="polite" className="content-card">Analyzing catalog candidates with OpenRouter…</section>}
    {result && <section className="results-section" aria-live="polite"><div className="section-heading"><h2>Recommended products</h2><span className="muted">{result.suggestions.length} result(s) · Catalog verified</span></div>
      {result.notice && <p className="notice">{result.notice}</p>}<RecommendationResults items={result.suggestions}/>
    </section>}
  </div>;
}
