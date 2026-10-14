import { redirect } from "next/navigation";
import Link from "next/link";
import { isVerifiedSession } from "@/lib/session";
import { LogoutButton } from "@/components/RecommendationResults";

function SearchIcon() {
  return <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="6.75" cy="6.75" r="5" stroke="currentColor" strokeWidth="1.6"/><path d="m10.5 10.5 3 3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/></svg>;
}
function GridIcon() {
  return <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.6"/><rect x="9" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.6"/><rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.6"/><rect x="9" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.6"/></svg>;
}

export default async function ProtectedLayout({ children }: { children: React.ReactNode }) {
  if (!(await isVerifiedSession())) redirect("/login");
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand-mark">
        <span className="logo" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 16 16" fill="none"><path d="M8 1.5 14 4.9v6.2L8 14.5 2 11.1V4.9L8 1.5Z" stroke="#fff" strokeWidth="1.4" strokeLinejoin="round"/><path d="M8 5.2 11 7v3.4L8 12.1 5 10.4V7l3-1.8Z" fill="#fff"/></svg>
        </span>
        <span><strong>Sales Support Hub</strong><small>PRODUCT WORKSPACE</small></span>
      </div>
      <nav aria-label="Main navigation" className="nav-stack">
        <Link href="/search"><SearchIcon /> Product Search</Link>
        <Link href="/products"><GridIcon /> Manage Products</Link>
      </nav>
      <div className="sidebar-foot"><LogoutButton /></div>
    </aside>
    <main className="main-panel">{children}</main>
  </div>;
}
