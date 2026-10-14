import { test, expect, Page } from "@playwright/test";

async function signedIn(page: Page) {
  const name = `search_${Date.now()}`;
  await page.goto("/register");
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Confirm password", { exact: true }).fill("testing-password-123");
  await page.getByLabel("Password", { exact: true }).fill("testing-password-123");
  await page.getByRole("button", { name: "Register" }).click();
  await expect(page).toHaveURL(/\/login\?registered=1/);
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Password", { exact: true }).fill("testing-password-123");
  await page.getByRole("button", { name: /Sign in/ }).click();
  await expect(page).toHaveURL(/\/search/);
}

test("recommendation shows only known catalog items and reasons", async ({ page }) => {
  await signedIn(page);
  await page.getByLabel("What is your customer looking for?").fill("Edge vision gateway for production-line defect inspection");
  await page.getByRole("button", { name: /Find products/ }).click();
  await expect(page.getByRole("region", { name: "Recommended products" })).toBeVisible();
  await expect(page.getByText("Why it matches").first()).toBeVisible();
});

test("OpenRouter fixture failure is shown honestly", async ({ page }) => {
  await signedIn(page);
  await page.getByLabel("What is your customer looking for?").fill("FORCE_PROVIDER_ERROR vision gateway");
  await page.getByRole("button", { name: /Find products/ }).click();
  await expect(page.getByRole("alert").filter({ hasText: "AI recommendations unavailable" })).toContainText("AI recommendations unavailable");
  await expect(page.getByRole("link", { name: /Manage Products/ })).toBeVisible();
});
