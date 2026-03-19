# Test Plan: Orange HRM Login Page

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Antigravity AI |
| **Date** | 2026-03-19 |
| **Environment** | Demo / Public Staging |
| **Browser** | Chromium (Playwright) |

---

## 1. Introduction

This test plan describes the testing approach for the **Orange HRM Login Page**. It outlines the scope, test strategy, resources, schedule, and deliverables for the testing effort focused on the main authentication gateway of the OrangeHRM Open Source platform.

## 2. Objectives

- Verify core login functionality works as expected with valid credentials.
- Identify defects in error handling for invalid or missing inputs.
- Ensure user flows for login and password recovery are complete and error-free.
- Validate UI elements (logo, branding, labels) and navigation.

## 3. Scope

### In Scope
- Verification of positive login flow (`Admin` / `admin123`).
- Verification of negative login flows (invalid credentials, empty fields).
- Validation of UI components: Username field, Password field, Login button, Forgot Password link.
- Branding verification (OrangeHRM logo presence).

### Out of Scope
- Load and performance testing of the authentication API.
- Security penetration testing.
- Database integrity checks beyond session creation.
- Testing on legacy browsers (IE11).

## 4. Test Strategy

### Test Approach
- **Automation Tool:** Playwright with `@playwright/test`
- **Test Type:** End-to-end functional testing
- **Browser:** Chromium
- **Environment:** Demo / Public Staging

### Test Levels
- Smoke Testing: Verified valid login flow.
- Functional Testing: Verified field validations and branding.
- Negative Testing: Verified error messages for incorrect inputs.

## 5. Test Environment

| Component | Details |
|-----------|---------|
| Application URL | https://opensource-demo.orangehrmlive.com/web/index.php/auth/login |
| Browser | Chromium |
| OS | Windows (as per user environment) |
| Framework | Playwright v1.58+ |
| Reporter | HTML + JSON |

## 6. Entry Criteria

- Application is deployed and accessible via the demo URL.
- Test environment (Node.js, Playwright) is configured.
- Valid test data (`Admin` / `admin123`) is available.
- Test scenarios are defined.

## 7. Exit Criteria

- All planned test cases executed against the dashboard and login page.
- All critical/high priority defects (e.g., login failure) resolved.
- Test report generated and reviewed.
- No open blockers preventing user login.

## 8. Test Cases Summary

| TC ID | Test Case Description | Expected Result |
|-------|-----------------------|-----------------|
| TC01 | Valid Login Attempt | User is redirected to the Dashboard page. |
| TC02 | Invalid Password | Error message "Invalid credentials" is displayed. |
| TC03 | Empty Credentials | "Required" validation message appears under fields. |
| TC04 | Forgot Password Link | User is navigated to the Reset Password page. |
| TC05 | Dashboard Branding | OrangeHRM logo is visible after successful login. |

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Application downtime | High | Use stable demo environment; verify connectivity before runs. |
| Flaky tests | Medium | Implement proper waits for AJAX calls and page loads. |
| Environment differences | Medium | Use consistent Playwright browser versions. |

## 10. Schedule

| Phase | Duration |
|-------|----------|
| Test Planning | 0.5 days |
| Test Case Design | 0.5 days |
| Test Execution | 0.5 days |
| Defect Reporting | Ongoing |
| Test Closure | 0.5 days |

## 11. Deliverables

- [x] Test Plan (this document)
- [ ] Test Cases Document
- [x] Dashboard Screenshot
- [ ] Test Summary Report
