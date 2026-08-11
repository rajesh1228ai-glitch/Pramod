| **Test ID** | **Description** | **Pre-conditions** | **Steps** | **Expected Result** | **Priority** |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Verify successful login | User registered with valid email & password | 1. Open vwo.com login page<br>2. Enter ``testuser@valid.mail``<br>3. Enter ``password123``<br>4. Click Login | Redirected to main dashboard | P0 |
| TC-02 | Verify incorrect email format | User has invalid email format | 1. Open login page<br>2. Enter ``testuser@invalid.mail``<br>3. Enter ``password123``<br>4. Click Login | Error: "Invalid Email Format" | P1 |
| TC-03 | Blank fields ignored due to account expiry | Account expired | 1. Open login page<br>2. Leave email blank<br>3. Enter valid password<br>4. Click Login | Redirected to dashboard | P0 |
| TC-04 | Attempt login without initial password | No password provided | 1. Open login page<br>2. Leave email blank<br>3. Enter invalid password<br>4. Click Login | Error: "Invalid Credentials" | P2 |
| TC-05 | Verify Remember Me option | Remember Me enabled | 1. Open login page<br>2. Enable Remember Me<br>3. Enter credentials<br>4. Click Login | Login successful | P0 |
| TC-06 | Handle login for already authenticated user | User already logged in | 1. Open login page<br>2. Enter valid credentials<br>3. Submit | Redirect to dashboard or message “Already logged in” | P1 |
| TC-07 | Error messaging for invalid credentials | User enters wrong password | 1. Open login page<br>2. Enter incorrect password<br>3. Submit | Error: "Invalid Credentials" | P0 |
| TC-08 | Password field character limit | Password length validation required | 1. Open login page<br>2. Enter ``password1``<br>3. Submit | Minimum requirements enforced | P1 |
| TC-09 | Test email format input | Email field empty | 1. Open login page<br>2. Leave email blank<br>3. Enter valid email<br>4. Click Login | Error displayed | P1 |
| TC-010 | Missing email | Profile not linked | 1. Open login page<br>2. Fill new email<br>3. Attempt login | Error message displayed | P0 |
| TC-011 | Password strength indication | Password meets strength criteria | 1. Open login page<br>2. Enter strong password<br>3. Click Login | Strong password logo displayed | P0 |
| TC-012 | Password visibility toggle | Password field available | 1. Open login page<br>2. Leave password blank<br>3. Submit | Option to toggle visibility present | P0 |
| TC-013 | SSO/SAML integration | SSO configured | 1. Open login page<br>2. Enter credentials<br>3. Press Sign In | SSO successful/failed | P0 |
| TC-014 | Rate limiting after failed login | Multiple failed attempts | 1. Login with invalid creds<br>2. Retry | Alert to admin | P2 |
| TC-015 | Session timeout after failed login | Invalid credentials entered | 1. Open login page<br>2. Enter wrong username<br>3. Try valid password<br>4. Initiate password change | Timeout or password change | P2 |
| TC-016 | HTTPS enforcement | HTTPS enabled | 1. Open login page<br>2. Enter valid email<br>3. Enter password<br>4. Confirm login | Login via HTTPS | P0 |
| TC-017 | Loading state on submit | Submission initiated | 1. Open login page<br>2. Click submit<br>3. Input details | Validation completes | P0 |
| TC-018 | Auto focus on field | Login form active | 1. Open login page<br>2. Enter key character<br>3. Click Submit | Auto focus applied | P0 |
| TC-019 | Keyboard navigation | Tab key navigation | 1. Open login page<br>2. Navigate with Tab<br>3. Submit | Navigation works | P0 |
| TC-020 | High contrast mode | Accessibility enabled | 1. Open login page<br>2. Enable high contrast<br>3. Enter credentials | Login successful | P0 |
| TC-021 | Responsive mobile layout | Mobile device used | 1. Launch app<br>2. Click Sign In<br>3. Verify navigation | Login form responsive | P0 |
| TC-022 | Register link | Registration available | 1. Open login page<br>2. Click Register link<br>3. Navigate menu | Registration link works | P0 |
| TC-023 | Error message clarity | Error messages enabled | 1. Open login page<br>2. Enter valid credentials<br>3. Click Login | Clear error content | P0 |
| TC-024 | Password toggle disable/enable | Password toggle available | 1. Open login page<br>2. Enter incorrect credentials<br>3. Click Cancel<br>4. Change setting<br>5. Attempt login | Toggle works correctly | P0 |
| TC-025 | Loading state after first login | Valid credentials entered | 1. Open login page<br>2. Enter valid email<br>3. Enter password<br>4. Press Login | Loading completes successfully | P0 |