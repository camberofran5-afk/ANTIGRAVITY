#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log("🚀 Launching TestSprite (Agentic Testing Engine)...");
console.log("   Adapter: @playwright/test");

const args = process.argv.slice(2);
const configPath = path.resolve(__dirname, '../config/testsprite.config.ts');

// Map 'testsprite' commands to Playwright commands
const playwrightArgs = [
    'test',
    '--config', configPath,
    ...args
];

const child = spawn('npx', ['playwright', ...playwrightArgs], {
    stdio: 'inherit',
    shell: true,
    cwd: path.resolve(__dirname, '..')
});

child.on('close', (code) => {
    if (code === 0) {
        console.log("\n✅ TestSprite execution completed successfully.");
    } else {
        console.error(`\n❌ TestSprite execution failed with code ${code}`);
    }
    process.exit(code);
});
