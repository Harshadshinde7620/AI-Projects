# Test Cases: Orange HRM Login Page

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Antigravity AI |
| **Date** | 2026-03-19 |
| **Total Test Cases** | 5 |

---

## Test Cases

| TC ID | Title | Preconditions | Steps | Expected Result | Priority | Category | Spec File |
|-------|-------|---------------|-------|-----------------|----------|----------|-----------|
| TC-01 | Valid Login Attempt | Browser is open at Login page | 1. Enter "Admin" in Username<br>2. Enter "admin123" in Password<br>3. Click Login | User is redirected to Dashboard | High | Smoke | `login.spec.ts` |
| TC-02 | Invalid Password | Browser is open at Login page | 1. Enter "Admin" in Username<br>2. Enter "wrong123" in Password<br>3. Click Login | Error: "Invalid credentials" | High | Negative | `login.spec.ts` |
| TC-03 | Invalid Username | Browser is open at Login page | 1. Enter "NotAdmin" in Username<br>2. Enter "admin123" in Password<br>3. Click Login | Error: "Invalid credentials" | Medium | Negative | `login.spec.ts` |
| TC-04 | Empty Fields | Browser is open at Login page | 1. Leave Username empty<br>2. Leave Password empty<br>3. Click Login | "Required" messages appear | Medium | Negative | `login.spec.ts` |
| TC-05 | SQL Injection Attempt | Browser is open at Login page | 1. Enter `' OR '1'='1` in Username<br>2. Enter anything in Password<br>3. Click Login | Error: "Invalid credentials" (Safe handling) | Low | Edge Case | `login.spec.ts` |

---

## Summary

| Priority | Count |
|----------|-------|
| High | 2 |
| Medium | 2 |
| Low | 1 |
| **Total** | **5** |

| Category | Count |
|----------|-------|
| Smoke | 1 |
| Functional | 0 |
| Negative | 4 (incl Edge Case) |
