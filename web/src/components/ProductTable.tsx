"use client";
import { Product } from "@/lib/api";

export default function ProductTable({ products, onEdit, onDelete, busy }: { products: Product[]; onEdit: (product: Product) => void; onDelete: (product: Product) => void; busy: boolean; }) {
  if (!products.length) return <div className="empty">No products found. Add the first product to begin.</div>;
  return <div className="table-scroller"><table><thead><tr><th>Product</th><th>Category</th><th>Type</th><th>Brand</th><th>Actions</th></tr></thead><tbody>
    {products.map(product => <tr key={product.id}><td><strong>{product.name}</strong><span className="table-desc">{product.description}</span></td><td>{product.category}</td><td>{product.type} / {product.subtype}</td><td>{product.brand}</td><td><div className="actions"><button type="button" className="text-button" onClick={()=>onEdit(product)} disabled={busy}>Edit</button><button type="button" className="text-button danger" onClick={()=>onDelete(product)} disabled={busy}>Delete</button></div></td></tr>)}
  </tbody></table></div>;
}
