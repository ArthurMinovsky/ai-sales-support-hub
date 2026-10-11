import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const nonce = btoa(crypto.randomUUID());
  const development = process.env.NODE_ENV === "development";
  const policy = [
    "default-src 'self'",
    "script-src 'self' 'nonce-" + nonce + "' 'strict-dynamic'" + (development ? " 'unsafe-eval'" : ""),
    "style-src 'self' " + (development ? "'unsafe-inline'" : "'nonce-" + nonce + "'"),
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self'" + (development ? " ws: wss:" : ""),
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'self'",
    "frame-src 'none'",
    "frame-ancestors 'none'",
  ].join("; ");
  const headers = new Headers(request.headers);
  // Overwrite untrusted incoming policy/nonce before Next renders its scripts.
  headers.set("x-nonce", nonce);
  headers.set("Content-Security-Policy", policy);
  // No session is possible without a Cookie header. Return the same public
  // login destination without Next's large streamed redirect body.
  const publicRoot = request.nextUrl.pathname === "/" && !request.headers.has("cookie");
  const response = publicRoot
    ? NextResponse.redirect(new URL("/login", request.url))
    : NextResponse.next({ request: { headers } });
  response.headers.set("Content-Security-Policy", policy);
  if (publicRoot) response.headers.set("Cache-Control", "private, no-store");
  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};

