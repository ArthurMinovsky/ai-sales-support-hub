import { redirect } from "next/navigation";
import Link from "next/link";
import { isVerifiedSession } from "@/lib/session";
import { LogoutButton } from "@/components/RecommendationResults";

export default async function ProtectedLayout({ children }: { children: React.ReactNode }) {
  if (!(await isVerifiedSession())) redirect("/login");
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand-mark">✦ <strong>Sales Support</strong><small>AI WORKSPACE</small></div>
      <nav aria-label="Main navigation" className="nav-stack">
        <Link href="/search">✧ &nbsp; Product Search</Link>
        <Link href="/products">▦ &nbsp; Manage Products</Link>
      </nav>
      <div className="sidebar-foot"><span className="demo-chip">DEMO CATALOG</span><LogoutButton /></div>
    </aside>
    <main className="main-panel">{children}</main>
  </div>;
}
