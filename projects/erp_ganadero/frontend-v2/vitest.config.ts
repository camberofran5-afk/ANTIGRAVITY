/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
    test: {
        environment: 'jsdom',
        setupFiles: ['./tests/setup.ts'],
        globals: true, // Allow describe, test, expect without imports
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});
