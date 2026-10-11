"use client";
import { useCallback, useEffect, useState } from "react";
import ProductForm from "@/components/ProductForm";
import ProductTable from "@/components/ProductTable";
import { apiRequest, Product, ProductInput } from "@/lib/api";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [query, setQuery] = useState("");
  const [editing, setEditing] = useState<Product | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const load = useCallback(async () => { setLoading(true); try { setProducts(await apiRequest<Product[]>("products")); setError(""); } catch(e) { setError(e instanceof Error ? e.message : "Could not load catalog"); } finally { setLoading(false); } }, []);
  useEffect(() => { void load(); }, [load]);
  async function save(input: ProductInput) {
    setBusy(true);
    try {
      await apiRequest<Product>(editing ? `products/${editing.id}` : "products", { method: editing ? "PUT" : "POST", body: JSON.stringify(input) });
      setFormOpen(false); setEditing(null); setNotice(editing ? "Product updated" : "Product created"); await load();
    } finally { setBusy(false); }
  }
  async function remove(product: Product) {
    if (!window.confirm(`Delete ${product.name}? This cannot be undone.`)) return;
    setBusy(true); setError("");
    try { await apiRequest<void>(`products/${product.id}`, { method: "DELETE" }); setNotice("Product deleted"); await load(); }
    catch(e) { setError(e instanceof Error ? e.message : "Delete failed"); }
    finally { setBusy(false); }
  }
  const filtered = products.filter(p => `${p.name} ${p.brand} ${p.category}`.toLowerCase().includes(query.toLowerCase()));
  return <div className="page-wrap">
    <div className="page-header"><div><div className="eyebrow">CATALOG MANAGEMENT</div><h1>Manage Products</h1><p className="muted">Keep your product knowledge up to date.</p></div><button className="primary" onClick={()=>{setEditing(null); setFormOpen(true);}}>+ Add Product</button></div>
    {error && <p className="error" role="alert">{error}</p>}
    {notice && <p className="notice" role="status">{notice}</p>}
    {formOpen && <ProductForm product={editing} onSubmit={save} onCancel={()=>{setFormOpen(false);setEditing(null);}} pending={busy}/>}
    <section className="content-card"><div className="toolbar"><h2>Product catalog <span className="counter">{products.length}</span></h2><label className="search-control"><span className="sr-only">Filter products</span><input placeholder="Filter by product, brand or category" value={query} onChange={e=>setQuery(e.target.value)}/></label></div>
      {loading ? <p className="muted">Loading catalog…</p> : <ProductTable products={filtered} busy={busy} onEdit={p=>{setEditing(p);setFormOpen(true);}} onDelete={remove}/>}
    </section>
  </div>;
}
