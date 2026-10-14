import { test, expect, Page } from "@playwright/test";

async function signedIn(page: Page) {
  const name = `catalog_${Date.now()}`;
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

test("authorized product create edit refresh and delete", async ({ page }) => {
  await signedIn(page);
  await page.goto("/products");
  await page.getByRole("button", { name: /Add Product/ }).click();
  await page.getByLabel("Product name").fill("VisionScan FG-120 Vision Gateway");
  await page.getByLabel("Brand").fill("Demo Sensors");
  await page.getByLabel("Description").fill("Compact GigE Vision gateway with onboard defect detection for assembly lines.");
  await page.getByLabel("Category").fill("Industrial AI");
  await page.getByLabel("Type", { exact: true }).fill("Edge Gateway");
  await page.getByLabel("Subtype").fill("Machine Vision");
  await page.getByRole("button", { name: "Save product" }).click();
  await expect(page.getByText("VisionScan FG-120 Vision Gateway")).toBeVisible();
  await page.reload();
  await expect(page.getByText("VisionScan FG-120 Vision Gateway")).toBeVisible();
  const row = page.getByRole("row").filter({ hasText: "VisionScan FG-120 Vision Gateway" });
  await row.getByRole("button", { name: "Edit" }).click();
  await page.getByLabel("Product name").fill("VisionScan FG-121 Vision Gateway");
  await page.getByRole("button", { name: "Save product" }).click();
  const updated = page.getByRole("row").filter({ hasText: "VisionScan FG-121 Vision Gateway" });
  await expect(updated).toBeVisible();
  await page.reload();
  await expect(updated).toBeVisible();
  page.once("dialog", dialog => dialog.accept());
  await updated.getByRole("button", { name: "Delete" }).click();
  await expect(page.getByRole("row").filter({ hasText: "VisionScan FG-121 Vision Gateway" })).toHaveCount(0);
});
