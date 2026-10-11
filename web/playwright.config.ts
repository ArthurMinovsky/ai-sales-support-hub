import { defineConfig, devices } from "@playwright/test";
import { execFileSync } from "node:child_process";
import { resolve } from "node:path";

function webBaseUrl(): string {
  if (process.env.PLAYWRIGHT_BASE_URL) return process.env.PLAYWRIGHT_BASE_URL;
  try {
    const published = execFileSync("docker", ["compose", "port", "--index", "1", "web", "3000"], {
      cwd: resolve(__dirname, ".."), encoding: "utf8", stdio: ["ignore", "pipe", "pipe"],
    }).trim().split("\n")[0];
    const port = published.split(":").pop();
    if (!port || !/^\d+$/.test(port) || Number(port) === 0) throw new Error("Web port is unavailable");
    return `http://localhost:${port}`;
  } catch {
    throw new Error("Start the Compose test stack and set COMPOSE_PROJECT_NAME, or set PLAYWRIGHT_BASE_URL to the running Web URL.");
  }
}

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  timeout: 30_000,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { outputFolder: "../evidence/frontend/playwright-report", open: "never" }]],
  use: { baseURL: webBaseUrl(), trace: "retain-on-failure", screenshot: "only-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
