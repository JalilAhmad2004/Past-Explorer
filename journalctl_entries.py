import subprocess

def fetch_journalctl_user_logs():
    try:
        # Run the journalctl command to fetch the 100 most recent user logs
        result = subprocess.run(
            ['journalctl', '--user', '-n', '100', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if there is any error in fetching the logs
        if result.stderr:
            print(f"Error: {result.stderr}")
        else:
            # Split the output into individual lines and print them with line numbers
            lines = result.stdout.splitlines()
            for i, line in enumerate(lines, 1):
                print(f"{i}: {line}")
    except FileNotFoundError:
        print("The 'journalctl' command is not available. Please ensure systemd is installed and available.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_journalctl_user_logs()

