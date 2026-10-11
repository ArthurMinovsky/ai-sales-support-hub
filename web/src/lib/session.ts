import { cookies } from "next/headers";

export const SESSION_COOKIE = "sales_hub_session";
export const SESSION_MAX_AGE = 3600;

export async function getSessionToken(): Promise<string | undefined> {
  return (await cookies()).get(SESSION_COOKIE)?.value;
}

export function secureCookieOptions(request: Request) {
  return {
    httpOnly: true as const,
    sameSite: "lax" as const,
    secure: (process.env.APP_ORIGIN || request.url).startsWith("https://"),
    path: "/",
    maxAge: SESSION_MAX_AGE,
  };
}

export function isAllowedOrigin(request: Request): boolean {
  const origin = request.headers.get("origin");
  if (!origin || origin === "null") return false;
  if (process.env.APP_ORIGIN) return origin === process.env.APP_ORIGIN;

  // Docker's direct Node listener is HTTP and keeps the public Host/port.
  // Next may derive request.url's scheme from forwarded headers, so an HTTPS
  // proxy must use an explicit APP_ORIGIN instead of trusting that metadata.
  const host = request.headers.get("host");
  if (!host) return false;
  try {
    const protocol = new URL(request.url).protocol;
    if (protocol !== "http:") return false;
    const allowed = new URL(`${protocol}//${host}`);
    if (allowed.host !== host.toLowerCase() || allowed.username || allowed.password) return false;
    return origin === allowed.origin;
  } catch {
    return false;
  }
}

export function internalBackendUrl(): string {
  return process.env.BACKEND_INTERNAL_URL || "http://localhost:8000";
}

export async function isVerifiedSession(): Promise<boolean> {
  const token = await getSessionToken();
  if (!token) return false;
  try {
    const res = await fetch(`${internalBackendUrl()}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
      signal: AbortSignal.timeout(5000),
    });
    return res.ok;
  } catch {
    return false;
  }
}
