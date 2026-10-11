"use client";
import { FormEvent, useEffect, useState } from "react";
import { Product, ProductInput } from "@/lib/api";

const blank: ProductInput = { name: "", brand: "", description: "", image_url: null, category: "", type: "", subtype: "" };
export default function ProductForm({ product, onSubmit, onCancel, pending }: {
  product: Product | null;
  onSubmit: (input: ProductInput) => Promise<void>;
  onCancel: () => void;
  pending: boolean;
}) {
  const [form, setForm] = useState<ProductInput>(blank);
  const [error, setError] = useState("");
  useEffect(() => { setForm(product ? { name: product.name, brand: product.brand, description: product.description, image_url: product.image_url, category: product.category, type: product.type, subtype: product.subtype } : blank); setError(""); }, [product]);
  function field(key: keyof ProductInput, label: string, required = true) {
    return <label key={key}>{label}<input value={form[key] || ""} onChange={e => setForm(old => ({ ...old, [key]: e.target.value }))} required={required} /></label>;
  }
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    if (form.description.trim().length < 10) { setError("Description must contain at least 10 characters."); return; }
    try { await onSubmit({ ...form, image_url: form.image_url?.trim() || null }); }
    catch (e) { setError(e instanceof Error ? e.message : "Unable to save product"); }
  }
  return <section className="form-panel" aria-label={product ? "Edit product" : "Add product"}>
    <h2>{product ? "Edit product" : "Add product"}</h2>
    <form className="form-grid" onSubmit={submit}>
      <div className="form-row">{field("name", "Product name")}{field("brand", "Brand")}</div>
      <label>Description<textarea rows={4} minLength={10} value={form.description} onChange={e=>setForm(old=>({...old, description:e.target.value}))} required /></label>
      <div className="form-row">{field("category", "Category")}{field("type", "Type")}</div>
      <div className="form-row">{field("subtype", "Subtype")}{field("image_url", "HTTPS image URL (optional)", false)}</div>
      {error && <p className="error" role="alert">{error}</p>}
      <div className="actions"><button className="primary" type="submit" disabled={pending}>{pending ? "Saving…" : "Save product"}</button><button className="secondary" type="button" onClick={onCancel}>Cancel</button></div>
    </form>
  </section>;
}
