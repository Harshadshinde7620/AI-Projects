const XLSX = require('xlsx');
const path = require('path');

const resultsDir = path.join(__dirname, 'Orange HRM Results');
const filePath = path.join(resultsDir, 'Orange_HRM_Login_Test_Cases.xlsx');

const data = [
    ["TC ID", "Title", "Preconditions", "Steps", "Expected Result", "Priority", "Category"],
    ["TC-01", "Valid Login Attempt", "Browser is open at Login page", "1. Enter 'Admin' in Username\n2. Enter 'admin123' in Password\n3. Click Login", "User is redirected to Dashboard", "High", "Smoke"],
    ["TC-02", "Invalid Password", "Browser is open at Login page", "1. Enter 'Admin' in Username\n2. Enter 'wrong123' in Password\n3. Click Login", "Error message 'Invalid credentials' is displayed", "High", "Negative"],
    ["TC-03", "Invalid Username", "Browser is open at Login page", "1. Enter 'NotAdmin' in Username\n2. Enter 'admin123' in Password\n3. Click Login", "Error message 'Invalid credentials' is displayed", "Medium", "Negative"],
    ["TC-04", "Empty Fields", "Browser is open at Login page", "1. Leave Username empty\n2. Leave Password empty\n3. Click Login", "'Required' validation messages appear under fields", "Medium", "Negative"],
    ["TC-05", "SQL Injection Attempt", "Browser is open at Login page", "1. Enter \"' OR '1'='1\" in Username\n2. Enter any password\n3. Click Login", "Error message 'Invalid credentials' is displayed (Safe handling)", "Low", "Edge Case"]
];

const workbook = XLSX.utils.book_new();
const worksheet = XLSX.utils.aoa_to_sheet(data);

// Apply column widths
const wscols = [
    {wch: 10}, // TC ID
    {wch: 25}, // Title
    {wch: 35}, // Preconditions
    {wch: 50}, // Steps
    {wch: 45}, // Expected Result
    {wch: 10}, // Priority
    {wch: 15}  // Category
];
worksheet['!cols'] = wscols;

XLSX.utils.book_append_sheet(workbook, worksheet, "Test Cases");
XLSX.writeFile(workbook, filePath);

console.log(`Excel file created at: ${filePath}`);
