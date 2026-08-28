from agents.log_analysis_agent import analyze_logs


bug = """
The application crashes immediately after a user enters
valid credentials and clicks the Login button.

The login request reaches the server, but the application
terminates before the dashboard is displayed.

The issue occurs consistently during login.
"""


result = analyze_logs(
    bug
)


print("\n")
print("=" * 75)
print("LOG ANALYSIS AGENT - NO LOGS TEST")
print("=" * 75)

print()

print(
    result["log_analysis"]
)