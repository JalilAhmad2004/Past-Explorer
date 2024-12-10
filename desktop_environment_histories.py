import os
import xml.etree.ElementTree as ET

def fetch_recently_used_files(xbel_path):
    """Parses the recently-used.xbel file and displays the history of accessed files."""
    if os.path.exists(xbel_path):
        try:
            # Parse the XBEL XML file
            tree = ET.parse(xbel_path)
            root = tree.getroot()

            print("\n--- Recently Used Files ---")
            for item in root.findall('./bookmark'):
                uri = item.get('href')
                timestamp_element = item.find('./metadata/Timestamp')
                if uri:
                    timestamp = timestamp_element.text if timestamp_element is not None else 'Unknown'
                    print(f"File: {uri} | Last Accessed: {timestamp}")
        except ET.ParseError:
            print("Error: The recently-used.xbel file is not well-formed.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print(f"The file {xbel_path} does not exist.")

def main():
    # Path to the recently used file history
    xbel_path = os.path.expanduser('~/.local/share/recently-used.xbel')
    
    # Fetch and display the history
    fetch_recently_used_files(xbel_path)

if __name__ == "__main__":
    main()

