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
  await page.route("http://localhost:8000/metrics", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        {
          time_stamp: "2024-01-01T12:00:00",
          cpu_pct: 10,
          ram_pct: 20,
          disk_pct: 30,
          ram_used: 1,
          ram_total: 8,
        },
      ]),
    });
  });

  await page.goto("http://localhost:5173/");
  await expect(
    page.getByText("live, updates every 60s", { exact: true }),
  ).toBeVisible();
});

test("has health test results", async ({ page }) => {
  await page.route(
    "http://localhost:8000/metrics/status/test_results",
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          time_stamp: "2024-01-01T12:00:00",
          http: 404,
          mtls_no_cert: 0,
          mtls_cert: 404,
        }),
      });
    },
  );

  await page.goto("http://localhost:5173/");
  await expect(page.getByText("HTTP: 404")).toBeVisible();
  await expect(page.getByText("mTLS no cert: 000")).toBeVisible();
  await expect(page.getByText("mTLS with cert: 404")).toBeVisible();
});
