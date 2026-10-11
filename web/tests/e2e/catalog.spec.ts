import { test, expect, Page } from "@playwright/test";

async function signedIn(page: Page) {
  const name = `catalog_${Date.now()}`;
  await page.goto("/register");
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Email").fill(`${name}@example.test`);
  await page.getByLabel("Password").fill("testing-password-123");
  await page.getByRole("button", { name: "Register" }).click();
  await expect(page).toHaveURL(/\/login\?registered=1/);
  await page.getByLabel("Username").fill(name);
  await page.getByLabel("Password").fill("testing-password-123");
  await page.getByRole("button", { name: /Sign in/ }).click();
  await expect(page).toHaveURL(/\/search/);
}

test("authorized product create edit refresh and delete", async ({ page }) => {
  await signedIn(page);
  await page.goto("/products");
  await page.getByRole("button", { name: /Add Product/ }).click();
  await page.getByLabel("Product name").fill("Test E2E Controller");
  await page.getByLabel("Brand").fill("Test Brand");
  await page.getByLabel("Description").fill("A testing controller with excellent resilience and safe integration.");
  await page.getByLabel("Category").fill("Industrial");
  await page.getByLabel("Type", { exact: true }).fill("Device");
  await page.getByLabel("Subtype").fill("Control");
  await page.getByRole("button", { name: "Save product" }).click();
  await expect(page.getByText("Test E2E Controller")).toBeVisible();
  await page.reload();
  await expect(page.getByText("Test E2E Controller")).toBeVisible();
  const row = page.getByRole("row").filter({ hasText: "Test E2E Controller" });
  await row.getByRole("button", { name: "Edit" }).click();
  await page.getByLabel("Product name").fill("Updated E2E Controller");
  await page.getByRole("button", { name: "Save product" }).click();
  const updated = page.getByRole("row").filter({ hasText: "Updated E2E Controller" });
  page.once("dialog", dialog => dialog.accept());
  await updated.getByRole("button", { name: "Delete" }).click();
  await expect(page.getByRole("row").filter({ hasText: "Updated E2E Controller" })).toHaveCount(0);
});
