import { test, expect } from "@playwright/test";

test("has header", async ({ page }) => {
  await page.goto("http://localhost:5173");
  await expect(page.getByRole("heading", { name: "Monitoring" })).toBeVisible();
});

test("has stat cards", async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await expect(page.getByText("CPU", { exact: true })).toBeVisible();
  await expect(page.getByText("RAM", { exact: true })).toBeVisible();
  await expect(page.getByText("Disk", { exact: true })).toBeVisible();
  await expect(page.getByText("Uptime", { exact: true })).toBeVisible();
});

test("has canvas charts", async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await expect(page.locator("canvas")).toBeVisible();
});

test("has connection indicator", async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await expect(
    page.getByText("live, updates every 60s", { exact: true }),
  ).toBeVisible();
});

test("has health test results", async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await expect(page.getByText("HTTP: 200")).toBeVisible();
  await expect(page.getByText("mTLS no cert: 0")).toBeVisible();
  await expect(page.getByText("mTLS with cert: 404")).toBeVisible();
});
