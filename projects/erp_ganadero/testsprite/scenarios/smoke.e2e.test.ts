import { test, expect } from '@playwright/test';

test('TestSprite: Smoke Test - Load Dashboard', async ({ page }) => {
    console.log('🤖 TestSprite Agent: Navigating to Dashboard...');

    // Navigate to app
    await page.goto('/');

    // Check title
    await expect(page).toHaveTitle(/ERP Ganadero/);

    // Check main content presence
    const root = page.locator('#root');
    await expect(root).toBeVisible();

    console.log('✅ TestSprite: Dashboard loaded successfully!');
});
