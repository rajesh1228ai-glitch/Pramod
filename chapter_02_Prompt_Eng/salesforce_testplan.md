# Salesforce Test Plan

## Overview

This document contains a concise test plan and 10 industry-level test cases for a Salesforce-like CRM implementation. It covers authentication, core CRM CRUD flows, lead conversion, opportunity workflows, RBAC, integrations, bulk import, duplicate detection, sharing, and reports.

## Scope
- Authentication & MFA
- Accounts/Contacts CRUD
- Leads conversion to Opportunities
- Opportunity stage/workflow
- Role-Based Access Control (RBAC)
- API integrations (REST)
- Bulk data import (CSV)
- Duplicate detection & validation
- Data sharing and reports

## Objectives
- Validate functional correctness of core CRM features
- Ensure data integrity and auditability
- Verify security and RBAC enforcement
- Confirm integration endpoints and bulk operations behave as expected

## Assumptions
- Test sandbox environment available
- Test users and API credentials provisioned
- Test data can be reset between runs

## Entry Criteria
- Test environment up and reachable
- Test users and roles created
- Integration endpoints reachable with test credentials

## Exit Criteria
- All high/critical tests pass or have accepted defects
- No remaining critical regressions

---

# Test Cases (10)

## TC01 — Login / Multi-factor Auth
- Objective: Verify user can log in with valid credentials and MFA; block invalid attempts.
- Preconditions: Test user exists with MFA enabled.
- Steps:
  1. Navigate to login screen.
  2. Enter valid username/password.
  3. Complete MFA (OTP) flow.
  4. Attempt invalid password 5 times.
- Expected: Successful login and dashboard load; account locked or CAPTCHA after repeated failures.
- Priority: High; Type: Functional/Security

## TC02 — Create Account & Contact (CRUD)
- Objective: Create Account and related Contact; verify persistence and UI display.
- Preconditions: Authenticated user with create rights.
- Steps:
  1. Create an Account with required fields.
  2. Create a Contact linked to the Account.
  3. Refresh and verify records appear in list and detail views.
- Expected: Records stored and visible; audit fields populated.
- Priority: High; Type: Functional

## TC03 — Lead Conversion to Opportunity
- Objective: Convert a Lead into Account/Contact/Opportunity and validate data mapping.
- Preconditions: Lead record exists with complete contact info.
- Steps:
  1. Open Lead record.
  2. Execute Convert action and map fields.
  3. Verify Account/Contact/Opportunity are created and Lead marked converted.
- Expected: No data loss; relationships preserved.
- Priority: High; Type: Functional/Integration

## TC04 — Opportunity Sales Stage Workflow
- Objective: Validate Opportunity stage transitions and required field enforcement.
- Preconditions: Opportunity exists; user has edit rights.
- Steps:
  1. Transition Opportunity through defined stages.
  2. Attempt to bypass required fields for a stage.
  3. Mark as Closed Won and Closed Lost and verify behavior.
- Expected: Transitions enforce business rules and required fields; closed states locked.
- Priority: High; Type: Functional/Business Rule

## TC05 — Role-Based Access Control (RBAC)
- Objective: Verify object/field-level and record-level access for different roles.
- Preconditions: Users with Sales Rep, Sales Manager, and Read-Only roles exist.
- Steps:
  1. Login as Sales Rep and edit own Opportunity.
  2. Login as Read-Only and attempt an edit.
  3. Login as Manager and view team records.
- Expected: Permissions enforced per role; unauthorized actions blocked.
- Priority: High; Type: Security

## TC06 — Duplicate Detection & Validation Rules
- Objective: Ensure duplicate detection rules and validation rules prevent bad data.
- Preconditions: Duplicate and validation rules configured.
- Steps:
  1. Attempt to create duplicate Account/Contact.
  2. Create a record that violates a validation rule.
- Expected: Duplicates blocked or flagged; validation error messages displayed and logged.
- Priority: Medium; Type: Negative/Validation

## TC07 — API Integration: Create Contact via REST
- Objective: Verify external system can create Contact via API and triggers workflows.
- Preconditions: API credentials and endpoint available.
- Steps:
  1. POST Contact payload to the REST API.
  2. Verify HTTP 201 and response body.
  3. Confirm Contact exists and automation (assignment/workflow) executed.
- Expected: API success; data persisted; downstream automation triggered.
- Priority: High; Type: Integration/API

## TC08 — Bulk Data Import (CSV)
- Objective: Validate bulk import handles valid and invalid rows, producing actionable errors.
- Preconditions: CSV import tool configured.
- Steps:
  1. Prepare CSV containing valid and invalid rows.
  2. Upload, map fields, and execute import.
  3. Review import report for successes/failures.
- Expected: Valid rows imported; invalid rows rejected with clear reasons; no partial corrupt state.
- Priority: Medium; Type: Bulk/Negative

## TC09 — Data Sharing & Record Visibility (Sharing Rules)
- Objective: Verify sharing rules and manual sharing expose records appropriately.
- Preconditions: Records owned by User A; sharing rules configured.
- Steps:
  1. As User B (outside team), verify visibility of User A's record.
  2. Apply manual share to grant access and verify.
  3. Revoke share and confirm access removed.
- Expected: Visibility follows sharing rules; manual share works and can be revoked.
- Priority: Medium; Type: Security/Functional

## TC10 — Reports & Dashboard Accuracy
- Objective: Validate reports aggregate data correctly and dashboards refresh.
- Preconditions: Sample transactional data present.
- Steps:
  1. Create transactions that affect report metrics.
  2. Run report filters and compare against source data.
  3. Verify dashboard tiles reflect the changes after refresh.
- Expected: Report values accurate; dashboard displays updated figures.
- Priority: Medium; Type: Functional/Regression

---

If you want, I can also generate automation snippets (Selenium/Playwright or REST scripts) for the high-priority tests (TC01–TC04, TC07).
