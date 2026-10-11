import { NextResponse } from "next/server";
import { internalBackendUrl, isAllowedOrigin, secureCookieOptions, SESSION_COOKIE } from "@/lib/session";

export async function POST(request: Request) {
  if (!isAllowedOrigin(request)) return NextResponse.json({ detail: "Origin not allowed" }, { status: 403 });
  try {
    const body = await request.json();
    const res = await fetch(`${internalBackendUrl()}/api/auth/login`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body), cache: "no-store", signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      return NextResponse.json({ detail: err.detail || "Incorrect credentials" }, { status: res.status });
    }
    const data = await res.json();
    const response = NextResponse.json({ authenticated: true, expires_in: 3600 });
    response.cookies.set(SESSION_COOKIE, data.access_token, secureCookieOptions(request));
    return response;
  } catch {
    return NextResponse.json({ detail: "Login temporarily unavailable" }, { status: 503 });
  }
}
