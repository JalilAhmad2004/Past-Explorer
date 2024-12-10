import os
import sqlite3
import datetime

def get_firefox_history():
    """Extracts browsing history from Firefox, including the default profile."""
    # Use the current user's home directory to locate the Firefox history path
    history_path = os.path.join(os.environ['HOME'], '.mozilla/firefox/')
    
    # Look for default profiles
    profiles = [p for p in os.listdir(history_path) if p.endswith('.default-release') or p.endswith('.default') or p.endswith('.default-esr')]

    if not profiles:
        print("No Firefox profiles found.")
        return

    print(f"Profiles found: {profiles}")
    
    for profile in profiles:
        db_path = os.path.join(history_path, profile, 'places.sqlite')
        if os.path.exists(db_path):
            print(f"\n--- Firefox Browsing History for Profile: {profile} ---")
            try:
                # Connect to the Firefox history database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, visit_date FROM moz_places JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id ORDER BY visit_date DESC LIMIT 10")
                
                rows = cursor.fetchall()
                if not rows:
                    print(f"No history found in {db_path}.")
                    continue
                
                for row in rows:
                    url, title, visit_date = row
                    # Convert the timestamp from microseconds to a human-readable format
                    if visit_date:
                        visit_time = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=visit_date)
                        print(f"Title: {title if title else 'No Title'}, URL: {url}, Last Visited: {visit_time}")
                conn.close()
            except sqlite3.Error as e:
                print(f"Error reading Firefox history for profile {profile}: {e}")
        else:
            print(f"Profile at {db_path} does not exist or is not accessible.")

def get_chrome_history():
    """Extracts browsing history from Google Chrome, including the default profile."""
    # Use the current user's home directory to locate the Chrome history path
    history_path = os.path.join(os.environ['HOME'], '.config/google-chrome/')
    
    # Look for default profiles
    profiles = [p for p in os.listdir(history_path) if p.startswith('Default') or p.startswith('Profile')]

    if not profiles:
        print("No Chrome profiles found.")
        return

    for profile in profiles:
        db_path = os.path.join(history_path, profile, 'History')
        if os.path.exists(db_path):
            print(f"\n--- Google Chrome Browsing History for Profile: {profile} ---")
            try:
                # Connect to the Chrome history database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
                
                rows = cursor.fetchall()
                if not rows:
                    print(f"No history found in {db_path}.")
                    continue
                
                for row in rows:
                    url, title, last_visit_time = row
                    # Convert the timestamp from microseconds since 1601 to a human-readable format
                    if last_visit_time:
                        visit_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
                        print(f"Title: {title if title else 'No Title'}, URL: {url}, Last Visited: {visit_time}")
                conn.close()
            except sqlite3.Error as e:
                print(f"Error reading Chrome history for profile {profile}: {e}")
        else:
            print(f"Profile at {db_path} does not exist or is not accessible.")

def main():
    # Extract and display Firefox and Chrome histories
    get_firefox_history()
    get_chrome_history()

if __name__ == "__main__":
    main()
