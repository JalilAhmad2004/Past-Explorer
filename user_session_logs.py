import os

def display_xsession_errors():
    # Path to the user's .xsession-errors file
    xsession_errors_path = os.path.expanduser('~/.xsession-errors')
    
    # Check if the file exists
    if os.path.exists(xsession_errors_path):
        try:
            with open(xsession_errors_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.readlines()
                
                # Display the content with line numbers for better readability
                for i, line in enumerate(content, 1):
                    print(f"{i}: {line.strip()}")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
    else:
        print("The .xsession-errors file does not exist or is not accessible.")

if __name__ == "__main__":
    display_xsession_errors()

