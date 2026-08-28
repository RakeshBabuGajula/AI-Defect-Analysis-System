from agents.agent_orchestrator import run_defect_analysis


# =========================================================
# TEST BUG
# =========================================================

bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button.

The login request reaches the server, but the application
terminates before the dashboard is displayed.

The issue occurs consistently during login.
"""


# =========================================================
# TECHNICAL LOG
# =========================================================

technical_logs = """
2026-08-28 10:32:41 ERROR LoginController
Login request completed.

2026-08-28 10:32:41 ERROR AuthenticationService
Failed to initialize user session.

java.lang.NullPointerException:
Cannot invoke "UserSession.setToken(String)"
because "session" is null

    at com.example.auth.AuthenticationService.createSession(
        AuthenticationService.java:142
    )

    at com.example.auth.LoginController.authenticate(
        LoginController.java:87
    )

    at com.example.auth.LoginController.login(
        LoginController.java:54
    )
"""


# =========================================================
# RUN COMPLETE SYSTEM
# =========================================================

result = run_defect_analysis(

    bug_description=bug,

    technical_logs=technical_logs

)


# =========================================================
# DISPLAY FINAL RESULT
# =========================================================

print("\n")

print("=" * 80)
print("FINAL AI DEFECT ANALYSIS REPORT")
print("=" * 80)

print("\n")

print("1. TRIAGE")
print("-" * 80)
print(result["triage"])

print("\n")

print("2. DUPLICATE DETECTION")
print("-" * 80)
print(result["duplicate_detection"])

print("\n")

print("3. LOG ANALYSIS")
print("-" * 80)
print(result["log_analysis"])

print("\n")

print("4. ROOT CAUSE")
print("-" * 80)
print(result["root_cause"])

print("\n")

print("5. REMEDIATION")
print("-" * 80)
print(result["remediation"])

print("\n")

print("=" * 80)
print("END-TO-END ANALYSIS COMPLETED")
print("=" * 80)