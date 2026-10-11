import { test, expect } from "@playwright/test";
import { isAllowedOrigin, secureCookieOptions } from "../../src/lib/session";

test.describe("Origin policy", () => {
  const previousOrigin = process.env.APP_ORIGIN;
  test.afterEach(() => {
    if (previousOrigin === undefined) delete process.env.APP_ORIGIN;
    else process.env.APP_ORIGIN = previousOrigin;
  });

  test("accepts the actual host and dynamic port", () => {
    process.env.APP_ORIGIN = "";
    const request = new Request("http://web:3000/api/auth/login", {
      headers: { host: "localhost:45123", origin: "http://localhost:45123" },
    });
    expect(isAllowedOrigin(request)).toBe(true);
    expect(secureCookieOptions(request).secure).toBe(false);
  });

  for (const origin of ["http://attacker.example", "http://localhost:45124", "https://localhost:45123", "null", ""]) {
    test(`rejects mismatched or absent origin: ${origin || "missing"}`, () => {
      process.env.APP_ORIGIN = "";
      const request = new Request("http://web:3000/api/auth/login", {
        headers: { host: "localhost:45123", ...(origin ? { origin } : {}) },
      });
      expect(isAllowedOrigin(request)).toBe(false);
    });
  }

  test("does not trust a forged forwarded host", () => {
    process.env.APP_ORIGIN = "";
    const request = new Request("http://web:3000/api/auth/login", {
      headers: { host: "localhost:45123", origin: "http://attacker.example", "x-forwarded-host": "attacker.example" },
    });
    expect(isAllowedOrigin(request)).toBe(false);
  });

  test("rejects requests without a host", () => {
    process.env.APP_ORIGIN = "";
    expect(isAllowedOrigin(new Request("http://web:3000/api/auth/login", {
      headers: { origin: "http://web:3000" },
    }))).toBe(false);
  });

  test("requires a configured origin for HTTPS forwarded metadata", () => {
    process.env.APP_ORIGIN = "";
    expect(isAllowedOrigin(new Request("https://web:3000/api/auth/login", {
      headers: { host: "localhost:45123", origin: "https://localhost:45123", "x-forwarded-proto": "https" },
    }))).toBe(false);
  });

  test("keeps a configured HTTPS origin strict and cookies secure", () => {
    process.env.APP_ORIGIN = "https://sales.example";
    const request = new Request("http://web:3000/api/auth/login", {
      headers: { host: "localhost:45123", origin: "https://sales.example" },
    });
    expect(isAllowedOrigin(request)).toBe(true);
    expect(secureCookieOptions(request).secure).toBe(true);
    expect(isAllowedOrigin(new Request(request, { headers: { host: "localhost:45123", origin: "http://localhost:45123" } }))).toBe(false);
  });
});

test("BFF rejects cross-origin mutations on the published web port", async ({ request, baseURL }) => {
  const sameOrigin = new URL(baseURL!).origin;
  const deniedOrigins = ["http://attacker.example", "null", `${sameOrigin.replace(/:\d+$/, "")}:1`];
  for (const origin of deniedOrigins) {
    for (const path of ["/api/auth/register", "/api/auth/login", "/api/auth/logout", "/api/backend/products", "/api/backend/suggestions"]) {
      const response = await request.post(path, { headers: { Origin: origin, "X-Forwarded-Host": new URL(sameOrigin).host }, data: {} });
      expect(response.status(), `${path} Origin=${origin}`).toBe(403);
    }
    for (const method of ["put", "delete"] as const) {
      const response = await request[method]("/api/backend/products/1", { headers: { Origin: origin } });
      expect(response.status()).toBe(403);
    }
  }
  const absent = await request.post("/api/auth/logout");
  expect(absent.status()).toBe(403);
  const forgedScheme = await request.post("/api/auth/logout", {
    headers: { Origin: sameOrigin.replace("http:", "https:"), "X-Forwarded-Proto": "https" },
  });
  expect(forgedScheme.status()).toBe(403);
  const allowed = await request.post("/api/auth/logout", { headers: { Origin: sameOrigin } });
  expect(allowed.status()).toBe(200);
});

test("register, login, reject wrong credentials, and logout", async ({ page }) => {
  const name = `person_${Date.now()}`;
  await page.goto("/register");
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Email").fill(`${name}@example.test`);
  await page.getByLabel("Password").fill("testing-password-123");
  await page.getByRole("button", { name: "Register" }).click();
  await expect(page).toHaveURL(/\/login/);
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Password").fill("wrong-password");
  await page.getByRole("button", { name: /Sign in/ }).click();
  await expect(page.getByText("Incorrect username or password", { exact: true })).toBeVisible();
  await page.getByLabel("Password").fill("testing-password-123");
  await page.getByRole("button", { name: /Sign in/ }).click();
  await expect(page).toHaveURL(/\/search/);
  await page.getByRole("button", { name: /Sign out/ }).click();
  await expect(page).toHaveURL(/\/login/);
  await page.goto("/products");
  await expect(page).toHaveURL(/\/login/);
});
