import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:5000',
    screenshot: 'on',
    viewport: { width: 1366, height: 768 },
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1366, height: 768 } } },
    { name: 'mobile', use: { viewport: { width: 375, height: 667 } } },
  ],
  reporter: [['html', { open: 'never' }]],
});
