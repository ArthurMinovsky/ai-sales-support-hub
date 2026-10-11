"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Recommendation } from "@/lib/api";

export default function RecommendationResults({ items }: { items: Recommendation[] }) {
  if (!items.length) return <div className="empty">No matching catalog products were returned. Try describing the need in different words.</div>;
  return <div className="cards-grid" role="region" aria-label="Recommended products">
    {items.map((item, index) => <article className="result-card" key={item.product_id}>
      <div className="result-top"><span className="rank">{index + 1}</span><span className="pill">{item.product.category}</span><span className="brand-chip"><span className="dot" />{item.product.brand}</span></div>
      <h3>{item.product.name}</h3><p className="muted">#{item.product_id} · {item.product.type} · {item.product.subtype}</p>
      <p className="desc">{item.product.description}</p><div className="reason"><strong>Why it matches</strong><p>{item.reason}</p></div>
    </article>)}
  </div>;
}

export function LogoutButton() {
  const [pending, setPending] = useState(false);
  const router = useRouter();
  async function logout() {
    setPending(true);
    try { await fetch("/api/auth/logout", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" }); }
    finally { router.push("/login"); router.refresh(); setPending(false); }
  }
  return <button className="signout" type="button" disabled={pending} onClick={logout}>
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true" style={{ marginRight: 6, verticalAlign: "-2px" }}><path d="M6 2H3.5A1.5 1.5 0 0 0 2 3.5v9A1.5 1.5 0 0 0 3.5 14H6" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/><path d="M10.5 11 14 8l-3.5-3M14 8H6" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/></svg>Sign out
  </button>;
}
