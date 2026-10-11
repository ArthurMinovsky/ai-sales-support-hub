"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Recommendation } from "@/lib/api";

export default function RecommendationResults({ items }: { items: Recommendation[] }) {
  if (!items.length) return <div className="empty">No matching catalog products were returned.</div>;
  return <div className="cards-grid" role="region" aria-label="Recommended products">
    {items.map((item, index) => <article className="result-card" key={item.product_id}>
      <div className="result-top"><span className="rank">0{index+1}</span><span className="pill">{item.product.category}</span></div>
      <h3>{item.product.name}</h3><p className="muted">{item.product.brand} · {item.product.type} / {item.product.subtype}</p>
      <p>{item.product.description}</p><div className="reason"><strong>Why it matches</strong><p>{item.reason}</p></div>
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
  return <button className="signout" type="button" disabled={pending} onClick={logout}>↩ &nbsp;Sign out</button>;
}
