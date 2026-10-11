import { NextRequest, NextResponse } from "next/server";
import { getSessionToken, internalBackendUrl, isAllowedOrigin } from "@/lib/session";

interface Context { params: Promise<{ segments: string[] }> }

async function proxy(request: NextRequest, context: Context) {
  const method = request.method.toUpperCase();
  if (!["GET", "POST", "PUT", "DELETE"].includes(method)) return NextResponse.json({ detail: "Method not allowed" }, { status: 405 });
  if (method !== "GET" && !isAllowedOrigin(request)) return NextResponse.json({ detail: "Origin not allowed" }, { status: 403 });
  const token = await getSessionToken();
  if (!token) return NextResponse.json({ detail: "Authentication required" }, { status: 401 });
  const { segments } = await context.params;
  const [first, second, ...extra] = segments;
  const products = first === "products" && !extra.length && (!second || /^\d+$/.test(second));
  const suggestions = first === "suggestions" && !second && (method === "POST");
  if (!products && !suggestions) return NextResponse.json({ detail: "Unknown API path" }, { status: 404 });
  if (products && first === "products" && second && method === "POST") return NextResponse.json({ detail: "Method not allowed" }, { status: 405 });
  if (products && !second && ["PUT", "DELETE"].includes(method)) return NextResponse.json({ detail: "Method not allowed" }, { status: 405 });
  const apiPath = segments.map(encodeURIComponent).join("/");
  const url = new URL(`${internalBackendUrl()}/api/${apiPath}`);
  for (const [key, value] of request.nextUrl.searchParams) url.searchParams.append(key, value);
  try {
    const hasBody = ["POST", "PUT"].includes(method);
    const body = hasBody ? await request.text() : undefined;
    if (body && body.length > 20000) return NextResponse.json({ detail: "Payload too large" }, { status: 413 });
    const upstream = await fetch(url, {
      method,
      headers: { Authorization: `Bearer ${token}`, ...(hasBody ? { "Content-Type": "application/json" } : {}) },
      body, cache: "no-store", signal: AbortSignal.timeout(25000),
    });
    if (upstream.status === 204) return new NextResponse(null, { status: 204 });
    const text = await upstream.text();
    return new NextResponse(text, { status: upstream.status, headers: { "Content-Type": upstream.headers.get("content-type") || "application/json", "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json({ code: "UPSTREAM_UNAVAILABLE", message: "Service temporarily unavailable" }, { status: 503 });
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const DELETE = proxy;
