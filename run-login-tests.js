const { chromium } = require('playwright-core');
const XLSX = require('xlsx');
const path = require('path');

const resultsDir = path.join(__dirname, 'Orange HRM Results');
const reportPath = path.join(resultsDir, 'Orange_HRM_Login_Test_Report.xlsx');
const baseURL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login';

async function runTests() {
    const browser = await chromium.launch({ headless: true });
    const results = [
        ["TC ID", "Title", "Status", "Execution Time", "Error/Notes"]
    ];

    const testScenarios = [
        {
            id: 'TC-01',
            title: 'Valid Login Attempt',
            run: async (page) => {
                await page.goto(baseURL);
                await page.fill('input[name="username"]', 'Admin');
                await page.fill('input[name="password"]', 'admin123');
                await page.click('button[type="submit"]');
                await page.waitForURL('**/dashboard/index');
                return true;
            }
        },
        {
            id: 'TC-02',
            title: 'Invalid Password',
            run: async (page) => {
                await page.goto(baseURL);
                await page.fill('input[name="username"]', 'Admin');
                await page.fill('input[name="password"]', 'wrong123');
                await page.click('button[type="submit"]');
                const error = await page.waitForSelector('.oxd-alert-content-text');
                return (await error.textContent()).includes('Invalid credentials');
            }
        },
        {
            id: 'TC-03',
            title: 'Invalid Username',
            run: async (page) => {
                await page.goto(baseURL);
                await page.fill('input[name="username"]', 'NotAdmin');
                await page.fill('input[name="password"]', 'admin123');
                await page.click('button[type="submit"]');
                const error = await page.waitForSelector('.oxd-alert-content-text');
                return (await error.textContent()).includes('Invalid credentials');
            }
        },
        {
            id: 'TC-04',
            title: 'Empty Fields',
            run: async (page) => {
                await page.goto(baseURL);
                await page.fill('input[name="username"]', '');
                await page.fill('input[name="password"]', '');
                await page.click('button[type="submit"]');
                const error = await page.waitForSelector('.oxd-input-group__message');
                return (await error.textContent()).includes('Required');
            }
        },
        {
            id: 'TC-05',
            title: 'SQL Injection Attempt',
            run: async (page) => {
                await page.goto(baseURL);
                await page.fill('input[name="username"]', "' OR '1'='1");
                await page.fill('input[name="password"]', 'anything');
                await page.click('button[type="submit"]');
                const error = await page.waitForSelector('.oxd-alert-content-text');
                return (await error.textContent()).includes('Invalid credentials');
            }
        }
    ];

    for (const test of testScenarios) {
        console.log(`Running ${test.id}: ${test.title}`);
        const context = await browser.newContext();
        const page = await context.newPage();
        const startTime = Date.now();
        let status = 'FAIL';
        let errorMsg = '';

        try {
            const success = await test.run(page);
            status = success ? 'PASS' : 'FAIL';
        } catch (e) {
            errorMsg = e.message;
            console.error(`Error in ${test.id}: ${e.message}`);
        }

        const duration = ((Date.now() - startTime) / 1000).toFixed(2) + 's';
        results.push([test.id, test.title, status, duration, errorMsg]);
        await context.close();
    }

    await browser.close();

    // Create Report Excel
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.aoa_to_sheet(results);
    const wscols = [
        {wch: 10}, // TC ID
        {wch: 30}, // Title
        {wch: 10}, // Status
        {wch: 20}, // Execution Time
        {wch: 50}  // Notes
    ];
    worksheet['!cols'] = wscols;
    XLSX.utils.book_append_sheet(workbook, worksheet, "Execution Results");
    XLSX.writeFile(workbook, reportPath);

    console.log(`Test Report created at: ${reportPath}`);
}

runTests().catch(console.error);
