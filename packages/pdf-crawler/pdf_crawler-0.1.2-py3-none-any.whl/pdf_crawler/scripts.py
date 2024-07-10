import os
import shutil

def post_install_script():
    print("Starting to create folder and move .bat file...")

    user_profile = os.environ['USERPROFILE']
    desktop_path = os.path.join(user_profile, 'Desktop', 'Volume II Generator')

    print(f"Creating folder at: {desktop_path}")

    # Create the folder on the desktop
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
        print(f"Folder created at: {desktop_path}")
    else:
        print(f"Folder already exists at: {desktop_path}")

    # Path to the .bat file
    # Adjust the path as needed to match the installed location
    bat_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Volume II Generator.bat'))
    destination_path = os.path.join(desktop_path, 'Volume II Generator.bat')
    print(f"Path to .bat file: {bat_file_path}")
    print(f"Destination path for .bat file: {destination_path}")

    # Move the .bat file to the new location
    try:
        shutil.move(bat_file_path, destination_path)
        print(f".bat file moved to: {destination_path}")
    except Exception as e:
        print(f"Failed to move .bat file: {e}")
