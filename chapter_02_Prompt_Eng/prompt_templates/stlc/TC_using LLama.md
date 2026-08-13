┌─────────┬────────────────────────────────────────┬────────────────────────────────────────┬────────────────────────────────────────┬────────────────────────────────────────┬──────────┐
  │ Test ID │ Description                            │ Pre-conditions                         │ Steps                                  │ Expected Result                        │ Priority │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-01   │ Verify successful login with valid     │ User is registered with valid email    │ 1. Open app.vwo.com login page 2.      │ User is redirected to the main         │ P0       │
  │         │ credentials                            │ and password                           │ Enter valid registered email 3. Enter  │ dashboard                              │          │
  │         │                                        │                                        │ correct password 4. Click Login        │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-02   │ Verify email format validation for     │ User has not entered a valid email     │ 1. Open app.vwo.com login page 2.      │ Error message "Invalid Email Format"   │ P1       │
  │         │ invalid email                          │ format                                 │ Enter 'testuser@invalid' in the email  │ is displayed and login is blocked      │          │
  │         │                                        │                                        │ field 3. Enter password 4. Click Login │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-03   │ Verify blank email field handling      │ No value entered in email field        │ 1. Open app.vwo.com login page 2.      │ Error message "Email is required" is   │ P1       │
  │         │                                        │                                        │ Leave email field blank 3. Enter valid │ displayed; no redirect occurs          │          │
  │         │                                        │                                        │ password 4. Click Login                │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-04   │ Verify blank password field handling   │ No value entered in password field     │ 1. Open app.vwo.com login page 2.      │ Error message "Password is required"   │ P1       │
  │         │                                        │                                        │ Enter valid email 3. Leave password    │ is displayed; no redirect occurs       │          │
  │         │                                        │                                        │ field blank 4. Click Login             │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-05   │ Verify login with incorrect password   │ User has valid registered email and    │ 1. Open app.vwo.com login page 2.      │ Error message "Invalid Credentials" is │ P0       │
  │         │                                        │ wrong password                         │ Enter valid email 3. Enter incorrect   │ displayed; user stays on login page    │          │
  │         │                                        │                                        │ password 4. Click Login                │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-06   │ Verify error message clarity for       │ User enters wrong credentials          │ 1. Open app.vwo.com login page 2.      │ Error message is clear and actionable, │ P0       │
  │         │ failed login                           │                                        │ Enter invalid email/password 3. Submit │ e.g., "Invalid email or password"      │          │
  │         │                                        │                                        │ 4. Read error message                  │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-07   │ Verify Remember Me checkbox persists   │ User has a valid account and selects   │ 1. Open login page 2. Check the        │ User session persists; user is not     │ P1       │
  │         │ session                                │ Remember Me                            │ Remember Me checkbox 3. Enter valid    │ required to re-login                   │          │
  │         │                                        │                                        │ credentials 4. Click Login 5. Close    │                                        │          │
  │         │                                        │                                        │ browser and reopen                     │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-08   │ Verify session expires without         │ User logged in without Remember Me     │ 1. Login without Remember Me 2. Wait   │ Session expires; user is redirected to │ P1       │
  │         │ Remember Me                            │                                        │ for configured session timeout 3.      │ login page                             │          │
  │         │                                        │                                        │ Attempt to access dashboard            │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-09   │ Verify password strength indicator     │ User types a password of low and high  │ 1. Open login page 2. Type weak        │ Weak password shows low strength;      │ P2       │
  │         │                                        │ strength                               │ password '1234' 3. Observe indicator   │ strong password shows high strength    │          │
  │         │                                        │                                        │ 4. Type strong password                │ with visual feedback                   │          │
  │         │                                        │                                        │ 'Vwo@2026#Pass' 5. Observe indicator   │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-10   │ Verify password visibility toggle      │ Password field is present on login     │ 1. Open login page 2. Enter a password │ Password characters are shown when     │ P2       │
  │         │                                        │ page                                   │ 3. Click the eye/toggle icon 4.        │ toggled on and masked when toggled off │          │
  │         │                                        │                                        │ Observe field 5. Click toggle again    │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-11   │ Verify Forgot Password flow            │ User has a registered email address    │ 1. Open login page 2. Click "Forgot    │ Reset email is sent with secure token; │ P1       │
  │         │                                        │                                        │ Password" link 3. Enter registered     │ user can set a new password and login  │          │
  │         │                                        │                                        │ email 4. Submit 5. Check email for     │                                        │          │
  │         │                                        │                                        │ reset link 6. Click reset link and set │                                        │          │
  │         │                                        │                                        │ new password                           │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-12   │ Verify 2FA login with valid OTP        │ 2FA is enabled for the user account    │ 1. Open login page 2. Enter valid      │ User is authenticated and redirected   │ P0       │
  │         │                                        │                                        │ credentials 3. Click Login 4. Enter    │ to dashboard                           │          │
  │         │                                        │                                        │ valid OTP from authenticator app       │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-13   │ Verify 2FA login with invalid OTP      │ 2FA is enabled; user enters wrong OTP  │ 1. Open login page 2. Enter valid      │ Error message "Invalid verification    │ P1       │
  │         │                                        │                                        │ credentials 3. Click Login 4. Enter    │ code" is displayed; access is denied   │          │
  │         │                                        │                                        │ incorrect OTP                          │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-14   │ Verify SSO/SAML login for enterprise   │ Enterprise account configured with SSO │ 1. Open login page 2. Click "Sign in   │ User is authenticated via IdP and      │ P1       │
  │         │ user                                   │                                        │ with SSO" 3. Enter corporate email 4.  │ redirected to dashboard                │          │
  │         │                                        │                                        │ Complete IdP authentication            │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-15   │ Verify rate limiting after multiple    │ No prior failed attempts on the        │ 1. Open login page 2. Attempt login    │ Account is temporarily locked or       │ P1       │
  │         │ failed attempts                        │ account                                │ with wrong password 5 times 3. Attempt │ throttled with message to retry later  │          │
  │         │                                        │                                        │ 6th login                              │                                        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-16   │ Verify HTTPS enforcement               │ Login page URL accessed                │ 1. Open login page 2. Check URL        │ Page loads only over HTTPS; HTTP       │ P0       │
  │         │                                        │                                        │ protocol 3. Attempt to access via HTTP │ requests redirect to HTTPS with valid  │          │
  │         │                                        │                                        │                                        │ certificate                            │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-17   │ Verify loading state on login submit   │ Valid credentials entered              │ 1. Open login page 2. Enter valid      │ Loading spinner/disabled button shown  │ P2       │
  │         │                                        │                                        │ credentials 3. Click Login 4. Observe  │ until authentication completes; no     │          │
  │         │                                        │                                        │ button and page during processing      │ double submit                          │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-18   │ Verify auto-focus on email field       │ Login page is opened fresh             │ 1. Open app.vwo.com login page 2.      │ Cursor is auto-focused on the email    │ P3       │
  │         │                                        │                                        │ Observe initial focus                  │ input field without user action        │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-19   │ Verify keyboard navigation             │ Login page is loaded                   │ 1. Open login page 2. Press Tab        │ All interactive elements (fields,      │ P2       │
  │         │                                        │                                        │ repeatedly 3. Attempt to activate      │ checkbox, buttons, links) are          │          │
  │         │                                        │                                        │ Login and Remember Me via Enter/Space  │ reachable and operable via keyboard    │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-20   │ Verify screen reader / ARIA labels     │ Screen reader enabled on login page    │ 1. Open login page with screen reader  │ ARIA labels are announced correctly    │ P2       │
  │         │                                        │                                        │ 2. Navigate fields and controls        │ for email, password, Remember Me, and  │          │
  │         │                                        │                                        │                                        │ Login button                           │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-21   │ Verify high contrast mode              │ High contrast accessibility option     │ 1. Open login page 2. Enable high      │ Text and controls remain readable with │ P2       │
  │         │                                        │ available                              │ contrast mode 3. Observe text and      │ sufficient contrast in high contrast   │          │
  │         │                                        │                                        │ controls                               │ mode                                   │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-22   │ Verify Dark Mode toggle                │ Announcement banner with Light/Dark    │ 1. Open login page 2. Click Dark Mode  │ Page theme switches to dark mode with  │ P3       │
  │         │                                        │ Mode options present                   │ option 3. Observe page appearance      │ all elements clearly visible;          │          │
  │         │                                        │                                        │                                        │ preference persists                    │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-23   │ Verify responsive layout on mobile     │ Login page opened on mobile device     │ 1. Open login page on mobile phone 2.  │ Layout adapts to screen size; fields   │ P1       │
  │         │                                        │                                        │ Enter credentials 3. Submit            │ and buttons are touch-friendly with no │          │
  │         │                                        │                                        │                                        │ overflow                               │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-24   │ Verify registration link redirects to  │ Login page is loaded                   │ 1. Open login page 2. Click "Start     │ User is redirected to the free trial   │ P2       │
  │         │ signup                                 │                                        │ Free Trial"/registration link          │ signup page                            │          │
  ├─────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼────────────────────────────────────────┼──────────┤
  │ TC-25   │ Verify login page load time under 2    │ Standard network connection and        │ 1. Open login page 2. Measure page     │ Login page loads within 2 seconds on a │ P1       │
  │         │ seconds                                │ browser                                │ load time using DevTools/Performance   │ standard connection                    │          │
  │         │                                        │                                        │ tool                                   │                                        │          │
  └─────────┴────────────────────────────────────────┴────────────────────────────────────────┴────────────────────────────────────────┴────────────────────────────────────────┴──────────┘
