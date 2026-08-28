from agents.remediation_agent import generate_remediation


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
"""


# =========================================================
# LOG FINDINGS
# =========================================================

logs = """
EXCEPTION:
java.lang.NullPointerException

ERROR:
Cannot invoke "UserSession.setToken(String)"
because "session" is null

FAILURE LOCATION:
AuthenticationService.java:142

CALL SEQUENCE:
LoginController.login:54
LoginController.authenticate:87
AuthenticationService.createSession:142

DIRECT FINDING:
UserSession is null when setToken() is invoked.
"""


# =========================================================
# DUPLICATE FINDINGS
# =========================================================

duplicate = """
DUPLICATE STATUS:
RELATED DEFECT

Apache Bug 24901 concerns authentication errors
resulting in HTTP 500 responses.

It is not considered an exact duplicate.
"""


# =========================================================
# ROOT CAUSE FINDINGS
# =========================================================

root_cause = """
PRIMARY ROOT CAUSE:

UserSession is null before setToken() is invoked
inside AuthenticationService.createSession().

ROOT CAUSE STATUS:

CONFIRMED CRASH MECHANISM.

The exact reason why UserSession became null is still unknown.

POTENTIAL UNDERLYING CAUSES:

1. Session creation dependency returned null.
2. A conditional branch bypassed session initialization.
3. Dependency injection or configuration issue.
"""


# =========================================================
# HISTORICAL EVIDENCE
# =========================================================

historical = """
Apache Bug 24901:
User authentication error causes a 500 Internal Server Error.

Apache Bug 55471:
Clearing cookies leads to application error.

Historical defects provide supporting context only.
"""


# =========================================================
# RUN REMEDIATION
# =========================================================

result = generate_remediation(

    bug_description=bug,

    triage_findings=triage,

    log_findings=logs,

    duplicate_findings=duplicate,

    root_cause_findings=root_cause,

    historical_evidence=historical

)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n")

print("=" * 75)

print("REMEDIATION AGENT RESULT")

print("=" * 75)

print()

print(
    result["remediation"]
)