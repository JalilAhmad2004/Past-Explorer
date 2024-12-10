import os

def get_history_file(shell_name, file_path):
    """Checks if the history file exists and reads the content with error handling."""
    if os.path.exists(file_path):
        print(f"\n--- {shell_name} Command History ---")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # Strip leading/trailing whitespace and print non-empty lines
                command = line.strip()
                if command:
                    print(command)
    else:
        print(f"\n{shell_name} history file not found at {file_path}.")

def main():
    # Define the paths to the history files
    home_dir = os.path.expanduser('~')
    bash_history_path = os.path.join(home_dir, '.bash_history')
    zsh_history_path = os.path.join(home_dir, '.zsh_history')

    # Get and print Bash history
    get_history_file('Bash', bash_history_path)

    # Get and print Zsh history
    get_history_file('Zsh', zsh_history_path)

if __name__ == "__main__":
    main()

