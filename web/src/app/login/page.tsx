"use client";
import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setPending(true); setError("");
    try {
      const response = await fetch("/api/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username, password }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Login failed");
      router.push("/search"); router.refresh();
    } catch (e) { setError(e instanceof Error ? e.message : "Unable to log in"); }
    finally { setPending(false); }
  }
  return <main className="auth-bg"><div className="auth-card">
    <div className="eyebrow">Sales Support Hub · project DEMO</div>
    <h1>Welcome back<span className="period">.</span></h1>
    <p className="muted">Sign in to find the right solution for your customers.</p>
    <form onSubmit={submit} className="form-grid">
      <label>Username<input autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} required /></label>
      <label>Password<input type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} required /></label>
      {error && <p role="alert" className="error">{error}</p>}
      <button type="submit" className="primary" disabled={pending}>{pending ? "Signing in…" : "Sign in →"}</button>
    </form><p className="muted lower">New here? <Link href="/register">Create an account</Link></p>
  </div></main>;
}
