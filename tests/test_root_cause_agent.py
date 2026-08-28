from agents.root_cause_agent import analyze_root_cause


# =========================================================
# CURRENT BUG
# =========================================================

bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button.

The login request reaches the server, but the application
terminates before the dashboard is displayed.

The issue occurs consistently during login.
"""


# =========================================================
# TRIAGE FINDINGS
# =========================================================

triage = """
DEFECT CATEGORY:
Application Crash / Functional Defect

AFFECTED AREA:
User Authentication / Login Flow / Post-Login Initialization

SEVERITY:
High

PRIORITY:
P2

REPRODUCIBILITY:
Consistent

MISSING INFORMATION:
Application version, environment details, stack trace,
and server logs were initially unavailable.
"""


# =========================================================
# LOG FINDINGS
# =========================================================

logs = """
LOG ANALYSIS SUMMARY:

A java.lang.NullPointerException occurs during login.

ERROR MESSAGE:
Cannot invoke "UserSession.setToken(String)"
because "session" is null.

FAILURE LOCATION:
com.example.auth.AuthenticationService.createSession

FILE:
AuthenticationService.java

LINE:
142

CALL SEQUENCE:
LoginController.login:54
    ->
LoginController.authenticate:87
    ->
AuthenticationService.createSession:142

DIRECT TECHNICAL FINDING:
The UserSession object is null when setToken() is invoked.

POTENTIAL TECHNICAL HYPOTHESIS:
The session object may not have been initialized before
setToken() was called.
"""


# =========================================================
# DUPLICATE FINDINGS
# =========================================================

duplicate = """
DUPLICATE STATUS:

RELATED DEFECT

MOST RELEVANT HISTORICAL CANDIDATE:

Apache Bug 24901:
User authentication error causes a 500 Internal Server Error.

The historical defect is related to authentication handling
but has a different failure mode and should not be treated
as an exact duplicate.
"""


# =========================================================
# HISTORICAL EVIDENCE
# =========================================================

historical = """
1. Apache Bug 24901
User authentication error causes a 500 Internal Server Error.

2. Apache Bug 55471
Clearing cookies after each iteration leads to application error.

3. Mozilla Bug 1389812
orbit.chat may freeze or crash the browser.

These defects provide supporting historical context only.
"""


# =========================================================
# RUN ROOT CAUSE ANALYSIS
# =========================================================

result = analyze_root_cause(

    bug_description=bug,

    triage_findings=triage,

    log_findings=logs,

    duplicate_findings=duplicate,

    historical_evidence=historical

)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n")

print("=" * 75)

print("ROOT CAUSE AGENT RESULT")

print("=" * 75)

print()

print(
    result["root_cause_analysis"]
)