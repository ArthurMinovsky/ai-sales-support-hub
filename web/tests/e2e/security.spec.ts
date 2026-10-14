import { test, expect } from "@playwright/test";

test("security headers and per-response nonces cover pages and assets", async ({ request }) => {
  const first = await request.get("/login");
  expect(first.ok()).toBe(true);
  const headers = first.headers();
  const policy = headers["content-security-policy"] ?? "";
  expect(policy).toContain("frame-ancestors 'none'");
  expect(policy).toContain("object-src 'none'");
  expect(policy).toContain("connect-src 'self'");
  expect(policy).not.toMatch(/unsafe-inline|unsafe-eval/);
  const nonce = policy.match(/'nonce-([^']+)'/)?.[1];
  expect(nonce).toBeTruthy();
  expect(headers["x-frame-options"]).toBe("DENY");
  expect(headers["x-content-type-options"]).toBe("nosniff");
  expect(headers["cross-origin-opener-policy"]).toBe("same-origin");
  expect(headers["cross-origin-embedder-policy"]).toBe("credentialless");
  expect(headers["cross-origin-resource-policy"]).toBe("same-origin");
  expect(headers["permissions-policy"]).toContain("camera=()");
  expect(headers["cache-control"]).toContain("no-store");
  const html = await first.text();
  const scripts = html.match(/<script\b[^>]*>/g) ?? [];
  expect(scripts.length).toBeGreaterThan(0);
  for (const script of scripts) expect(script).toContain('nonce="' + nonce + '"');
  const second = await request.get("/login");
  expect(second.headers()["content-security-policy"]).not.toBe(policy);
  const asset = html.match(/<script\b[^>]*src="([^"]+)"/)?.[1];
  expect(asset).toBeTruthy();
  const staticResponse = await request.get(asset!);
  expect(staticResponse.ok()).toBe(true);
  expect(staticResponse.headers()["x-content-type-options"]).toBe("nosniff");
  expect(staticResponse.headers()["cross-origin-resource-policy"]).toBe("same-origin");
  const root = await request.get("/", { maxRedirects: 0 });
  expect(root.status()).toBe(307);
  expect(root.headers()["location"]).toMatch(/\/login$/);
  expect(new URL(root.headers()["location"], first.url()).origin).toBe(new URL(first.url()).origin);
  expect((await root.body()).length).toBeLessThan(100);
});

test("strict CSP permits hydration and blocks an untrusted inline script", async ({ page }) => {
  const violations: string[] = [];
  await page.exposeFunction("recordPolicyViolation", (directive: string) => violations.push(directive));
  await page.addInitScript(() => {
    document.addEventListener("securitypolicyviolation", (event) => {
      void (window as unknown as { recordPolicyViolation: (value: string) => Promise<void> })
        .recordPolicyViolation(event.effectiveDirective);
    });
  });
  await page.goto("/login");
  await page.getByLabel("Username").fill("csp_probe_nonexistent");
  await page.getByLabel("Password", { exact: true }).fill("not-a-real-password");
  await page.getByRole("button", { name: /Sign in/ }).click();
  await expect(page.getByText("Incorrect username or password", { exact: true })).toBeVisible();
  expect(violations).toEqual([]);
  // Inject through the HTML parser. Debugger-evaluated DOM insertion is trusted
  // by Chromium and does not represent an untrusted response/XSS payload.
  await page.route(page.url(), async (route) => {
    const response = await route.fetch();
    const body = (await response.text()).replace("</head>", "<script>window.__untrustedInlineExecuted = true</script></head>");
    await route.fulfill({ response, body });
  });
  await page.reload();
  await expect.poll(() => violations).toContain("script-src-elem");
  expect(await page.evaluate(() => (window as unknown as { __untrustedInlineExecuted?: boolean }).__untrustedInlineExecuted)).toBeUndefined();
});

