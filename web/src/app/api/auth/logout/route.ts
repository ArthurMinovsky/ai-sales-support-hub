import { NextResponse } from "next/server";
import { isAllowedOrigin, secureCookieOptions, SESSION_COOKIE } from "@/lib/session";

export async function POST(request: Request) {
  if (!isAllowedOrigin(request)) return NextResponse.json({ detail: "Origin not allowed" }, { status: 403 });
  const response = NextResponse.json({ authenticated: false });
  response.cookies.set(SESSION_COOKIE, "", { ...secureCookieOptions(request), maxAge: 0 });
  return response;
}
