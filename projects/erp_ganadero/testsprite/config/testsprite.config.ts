import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: '../scenarios',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: [['html', { outputFolder: '../reports' }], ['list']],
    use: {
        baseURL: 'http://localhost:3001',
        trace: 'on-first-retry',
        screenshot: 'on',
        video: 'retain-on-failure',
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
});
