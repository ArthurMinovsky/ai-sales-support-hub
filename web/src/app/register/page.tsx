"use client";
import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    setPending(true);
    try {
      const response = await fetch("/api/auth/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ username, password, confirm_password: confirmPassword }) });
      const data = await response.json();
      if (!response.ok) {
        const message = typeof data.detail === "string" ? data.detail : "Please check your registration information";
        throw new Error(message);
      }
      router.push("/login?registered=1");
    } catch (e) { setError(e instanceof Error ? e.message : "Unable to register"); }
    finally { setPending(false); }
  }
  return <main className="auth-bg"><div className="auth-card">
    <div className="eyebrow"><svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M8 1.5 14 4.9v6.2L8 14.5 2 11.1V4.9L8 1.5Z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"/></svg> Sales Support Hub</div>
    <h1>Create your account</h1><p className="muted sub">Get started with your product workspace.</p>
    <form onSubmit={submit} className="form-grid">
      <label>Username<input autoComplete="username" minLength={3} value={username} onChange={e=>setUsername(e.target.value)} required /></label>
      <label>Password<input aria-label="Password" aria-describedby="password-help" type="password" autoComplete="new-password" minLength={10} maxLength={128} value={password} onChange={e=>setPassword(e.target.value)} required /><small id="password-help" className="muted">At least 10 characters.</small></label>
      <label>Confirm password<input type="password" autoComplete="new-password" minLength={10} maxLength={128} value={confirmPassword} onChange={e=>setConfirmPassword(e.target.value)} required /></label>
      {error && <p role="alert" className="error">{error}</p>}
      <button className="primary" disabled={pending}>{pending ? "Creating…" : "Register"}</button>
    </form><p className="muted lower">Already have an account? <Link href="/login">Sign in</Link></p>
  </div></main>;
}
