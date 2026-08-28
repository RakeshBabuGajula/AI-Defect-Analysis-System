from agents.log_analysis_agent import analyze_logs


bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button.
"""


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


result = analyze_logs(

    bug,

    technical_logs

)


print("\n")
print("=" * 75)
print("LOG ANALYSIS AGENT - STACK TRACE TEST")
print("=" * 75)

print()

print(
    result["log_analysis"]
)