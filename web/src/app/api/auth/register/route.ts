import { NextResponse } from "next/server";
import { internalBackendUrl, isAllowedOrigin } from "@/lib/session";

export async function POST(request: Request) {
  if (!isAllowedOrigin(request)) return NextResponse.json({ detail: "Origin not allowed" }, { status: 403 });
  try {
    const body = await request.json();
    const res = await fetch(`${internalBackendUrl()}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
      signal: AbortSignal.timeout(10000),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ detail: "Unable to register. Please try again." }, { status: 503 });
  }
}
