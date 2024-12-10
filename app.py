from flask import Flask, render_template, jsonify, request
import os
import sqlite3
import datetime
import subprocess
import threading
import tempfile
from desktop_environment_histories import fetch_recently_used_files

app = Flask(__name__)

# Function to fetch Firefox history with search term filter
def get_firefox_history(search_term):
    history_path = os.path.expanduser('~/.mozilla/firefox/')
    if not os.path.exists(history_path):
        print("Firefox history path does not exist.")
        return []

    profiles = [p for p in os.listdir(history_path) if p.endswith('.default-release') or p.endswith('.default-esr')]

    firefox_history = []
    for profile in profiles:
        db_path = os.path.join(history_path, profile, 'places.sqlite')
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id ORDER BY visit_date DESC LIMIT 10")
                
                for row in cursor.fetchall():
                    url, title, visit_date = row
                    if search_term in url.lower() or (title and search_term in title.lower()):
                        visit_time = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=visit_date)
                        firefox_history.append({'url': url, 'title': title, 'visit_time': visit_time})
                conn.close()
            except sqlite3.Error as e:
                print(f"Error reading Firefox history: {e}")
        else:
            print(f"Profile database at {db_path} does not exist or is not accessible.")
    return firefox_history

# Function to fetch Chrome history with search term filter
def get_chrome_history(search_term):
    history_path = os.path.expanduser('~/.config/google-chrome/')
    if not os.path.exists(history_path):
        print("Chrome history path does not exist.")
        return []

    profiles = [p for p in os.listdir(history_path) if p.startswith('Default') or p.startswith('Profile')]

    chrome_history = []
    for profile in profiles:
        db_path = os.path.join(history_path, profile, 'History')
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
                
                for row in cursor.fetchall():
                    url, title, last_visit_time = row
                    if search_term in url.lower() or (title and search_term in title.lower()):
                        visit_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
                        chrome_history.append({'url': url, 'title': title, 'visit_time': visit_time})
                conn.close()
            except sqlite3.Error as e:
                print(f"Error reading Chrome history: {e}")
        else:
            print(f"Profile database at {db_path} does not exist or is not accessible.")
    return chrome_history

# Function to handle browser history fetching in a separate thread (to avoid blocking)
def fetch_browser_history(search_term, result_dict):
    result_dict['firefox'] = get_firefox_history(search_term)
    result_dict['chrome'] = get_chrome_history(search_term)

# Function to fetch journalctl user logs
def fetch_journalctl_user_logs():
    try:
        result = subprocess.run(
            ['journalctl', '--user', '-n', '100', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.stderr:
            return {'error': result.stderr}
        
        lines = result.stdout.splitlines()
        return {'logs': lines}
    except FileNotFoundError:
        return {'error': "The 'journalctl' command is not available. Please ensure systemd is installed."}
    except Exception as e:
        return {'error': str(e)}

# Function to fetch user session logs
def get_user_session_logs():
    xsession_errors_path = os.path.expanduser('~/.xsession-errors')
    if os.path.exists(xsession_errors_path):
        try:
            with open(xsession_errors_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.readlines()
        except Exception as e:
            return [f"An error occurred while reading the file: {e}"]
    else:
        return ["The .xsession-errors file does not exist or is not accessible."]

# Function to fetch Vim history
def get_vim_history():
    viminfo_path = os.path.expanduser('~/.viminfo')
    file_history, command_history = [], []
    
    if os.path.exists(viminfo_path):
        with open(viminfo_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if line.startswith('> '):
                    filepath = line[2:].strip()
                    if filepath not in file_history:
                        file_history.append(filepath)
                elif line.startswith(':'):
                    command = line.strip()
                    command_history.append(command)
    else:
        return {'error': "Vim history file not found."}

    return {'file_history': file_history, 'command_history': command_history}

# Function to fetch recently used files in desktop environment by running the script
def get_desktop_environment_history():
    # Define the path to the script file
    script_path = os.path.join(os.path.dirname(__file__), 'desktop_environment_histories.py')
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Create a temporary file
    
    try:
        # Run the script and capture the output in the temporary file
        with open(temp_file.name, 'w') as f:
            subprocess.run(['python3', script_path], stdout=f, stderr=subprocess.PIPE, text=True)

        # Read the output from the temporary file
        with open(temp_file.name, 'r') as f:
            output = f.readlines()

        # Parse the output into structured data
        history = []
        for line in output:
            if line.startswith("File:"):
                parts = line.split("| Last Accessed: ")
                if len(parts) == 2:
                    file = parts[0].replace("File: ", "").strip()
                    last_accessed = parts[1].strip()
                    history.append({"file": file, "last_accessed": last_accessed})
        
        return history

    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}

    finally:
        # Clean up the temporary file
        os.remove(temp_file.name)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shell-history')
def shell_history():
    return render_template('shell_history.html')

@app.route('/browser-history')
def browser_history():
    return render_template('browser_history.html')

@app.route('/desktop-env-history')
def desktop_environment_history():
    return render_template('desktop.html')

@app.route('/journalctl-entry')
def journalctl_entry():
    return render_template('journal.html')

@app.route('/user-session-logs')
def user_session_logs():
    return render_template('user.html')

@app.route('/vim-history')
def vim_history_page():
    return render_template('vim.html')

@app.route('/get-journalctl-entry', methods=['GET'])
def get_journalctl_entry():
    result = fetch_journalctl_user_logs()
    return jsonify(result)

@app.route('/get-shell-history', methods=['GET'])
def get_shell_history():
    search_term = request.args.get('search', '').lower()
    home_dir = os.path.expanduser('~')
    bash_history_path = os.path.join(home_dir, '.bash_history')
    zsh_history_path = os.path.join(home_dir, '.zsh_history')

    def get_history_file(shell_name, file_path):
        history = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    command = line.strip()
                    if command and (search_term in command.lower()):
                        history.append(command)
        else:
            history.append(f"{shell_name} history file not found at {file_path}.")
        return history

    bash_history = get_history_file('Bash', bash_history_path)
    zsh_history = get_history_file('Zsh', zsh_history_path)

    return jsonify({'bash': bash_history, 'zsh': zsh_history})

@app.route('/get-browser-history', methods=['GET'])
def get_browser_history():
    search_term = request.args.get('search', '').lower()
    result_dict = {}

    thread = threading.Thread(target=fetch_browser_history, args=(search_term, result_dict))
    thread.start()
    thread.join()

    return jsonify(result_dict)

@app.route('/get-user-session-logs', methods=['GET'])
def get_user_session_logs_api():
    logs = get_user_session_logs()
    return jsonify({'logs': logs})

@app.route('/get-vim-history', methods=['GET'])
def get_vim_history_api():
    vim_history = get_vim_history()
    return jsonify(vim_history)

@app.route('/get-desktop-env-history', methods=['GET'])
def get_desktop_env_history():
    history = get_desktop_environment_history()
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
