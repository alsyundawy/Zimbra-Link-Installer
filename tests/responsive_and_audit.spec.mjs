import { test, expect } from "@playwright/test";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const indexPath = path.join(__dirname, "..", "index.html");
const fileUrl = `file://${indexPath}`;

test.describe("Zimbra Link Installer & Telemetry Suite - Audit & Verification", () => {
  test("Pillar 1 & 2: SEO Meta Tags & 2026 Standards Verification", async ({
    page,
  }) => {
    await page.goto(fileUrl);

    // Title tag
    const title = await page.title();
    expect(title).toContain("Zimbra Link Installer");

    // Viewport-fit=cover
    const viewportMeta = await page
      .locator('meta[name="viewport"]')
      .getAttribute("content");
    expect(viewportMeta).toContain("viewport-fit=cover");

    // Theme color
    const themeColor = await page
      .locator('meta[name="theme-color"]')
      .first()
      .getAttribute("content");
    expect(themeColor).toBe("#0a0f1d");

    // OpenGraph dimensions & type
    const ogImageWidth = await page
      .locator('meta[property="og:image:width"]')
      .getAttribute("content");
    const ogImageHeight = await page
      .locator('meta[property="og:image:height"]')
      .getAttribute("content");
    expect(ogImageWidth).toBe("1200");
    expect(ogImageHeight).toBe("630");

    // JSON-LD structured data schema
    const jsonLdContent = await page
      .locator('script[type="application/ld+json"]')
      .textContent();
    const jsonLd = JSON.parse(jsonLdContent);
    expect(jsonLd["@context"]).toBe("https://schema.org");

    // Check dateModified per today (2026-10-26)
    const techArticle = jsonLd["@graph"].find(
      (item) => item["@type"] === "TechArticle",
    );
    expect(techArticle).toBeDefined();
    expect(techArticle.dateModified).toContain("2026-10-26");
  });

  test("Pillar 3 & 4: WCAG 2.2 Accessibility & Color Standards", async ({
    page,
  }) => {
    await page.goto(fileUrl);

    // Skip to content link
    const skipLink = page.locator(".skip-to-content");
    await expect(skipLink).toHaveAttribute("href", "#main-content");

    // Color scheme dark
    const colorScheme = await page
      .locator('meta[name="color-scheme"]')
      .getAttribute("content");
    expect(colorScheme).toBe("dark");

    // ARIA controls & labels
    const mobileBtn = page.locator("#mobileMenuBtn");
    await expect(mobileBtn).toHaveAttribute("aria-label");
    await expect(mobileBtn).toHaveAttribute("aria-expanded");

    const backToTopBtn = page.locator("#backToTopBtn");
    await expect(backToTopBtn).toHaveAttribute("aria-label");
  });

  test("Pillar 5, 6, 7: Interactive Features (i18n Switcher, Filter, Drawer, Copy)", async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(fileUrl);

    // Test Language Switcher to English
    const btnLangEn = page.locator("#btnLangEn");
    await btnLangEn.click();
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
    await expect(btnLangEn).toHaveClass(/active/);

    // Test Language Switcher to Indonesian
    const btnLangId = page.locator("#btnLangId");
    await btnLangId.click();
    await expect(page.locator("html")).toHaveAttribute("lang", "id");
    await expect(btnLangId).toHaveClass(/active/);

    // Test Table Search Filter
    const filterInput = page.locator(".table-filter").first();
    if ((await filterInput.count()) > 0) {
      await filterInput.fill("10.1.0");
      await page.waitForTimeout(300); // Debounce wait
      const targetTableId = await filterInput.getAttribute("data-target");
      const table = page.locator(`#${targetTableId}`);
      if ((await table.count()) > 0) {
        const visibleRows = table.locator("tbody tr:visible");
        expect(await visibleRows.count()).toBeGreaterThan(0);
      }
      await filterInput.fill("");
      await page.waitForTimeout(300);
    }

    // Test Copy Button Feedback
    const copyBtn = page.locator(".copy-btn").first();
    if ((await copyBtn.count()) > 0) {
      await copyBtn.click();
      await expect(copyBtn).toContainText(/Tersalin|Copied/i);
    }
  });

  const devices = [
    { name: "VGA Portrait", width: 480, height: 640 },
    { name: "VGA Landscape", width: 640, height: 480 },
    { name: "iPhone SE (Ultra-compact)", width: 320, height: 568 },
    {
      name: "Xiaomi Redmi 9A / POCO C (MIUI/HyperOS)",
      width: 360,
      height: 800,
    },
    { name: "iPhone 14/15/16", width: 390, height: 844 },
    {
      name: "Xiaomi Redmi Note 12/13/14 (MIUI/HyperOS)",
      width: 392,
      height: 873,
    },
    { name: "POCO F5/F6 / X6 Pro (MIUI/HyperOS)", width: 393, height: 873 },
    { name: "Samsung Galaxy S24", width: 412, height: 915 },
    {
      name: "Xiaomi Redmi / POCO Landscape (with notch)",
      width: 873,
      height: 392,
    },
    { name: "iPad Mini (Tablet)", width: 768, height: 1024 },
    { name: "iPad Pro (Large Tablet)", width: 1024, height: 1366 },
    { name: "MacBook / Laptop", width: 1440, height: 900 },
    { name: "Desktop Full HD (1080p)", width: 1920, height: 1080 },
    { name: "2K QHD Desktop Monitor", width: 2560, height: 1440 },
  ];

  for (const device of devices) {
    test(`Pillar 8-13: Responsive & Zero-Cutoff on ${device.name} (${device.width}x${device.height})`, async ({
      page,
    }) => {
      await page.setViewportSize({
        width: device.width,
        height: device.height,
      });
      await page.goto(fileUrl);
      await page.waitForLoadState("domcontentloaded");

      // Verify ZERO horizontal blowout/overflow
      const hasHorizontalOverflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > window.innerWidth;
      });
      expect(hasHorizontalOverflow).toBe(false);

      // Verify top-navbar is rendered and inside viewport
      const navbar = page.locator(".top-navbar");
      await expect(navbar).toBeVisible();

      // On mobile viewports (<= 1024px), verify hamburger button works
      if (device.width <= 1024) {
        const mobileMenuBtn = page.locator("#mobileMenuBtn");
        await expect(mobileMenuBtn).toBeVisible();

        const sidebar = page.locator("#sidebarNav");
        expect(
          await sidebar.evaluate((el) => el.classList.contains("open")),
        ).toBe(false);

        // Open offcanvas drawer
        await mobileMenuBtn.click();
        expect(
          await sidebar.evaluate((el) => el.classList.contains("open")),
        ).toBe(true);

        // Close via backdrop click
        const backdrop = page.locator("#sidebarBackdrop");
        await backdrop.click({ force: true });
        expect(
          await sidebar.evaluate((el) => el.classList.contains("open")),
        ).toBe(false);
      }
    });
  }
});
