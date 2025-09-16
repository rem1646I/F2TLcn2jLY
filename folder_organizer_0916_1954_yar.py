# 代码生成时间: 2025-09-16 19:54:12
# folder_organizer.py
# This script is a Bottle application that organizes the structure of folders.

from bottle import route, run, request, response, static_file
import os
import shutil
from pathlib import Path

# Define the root directory for the web application
ROOT_DIR = Path("./")

# Define a function to organize the folder structure
def organize_folder_structure(directory):
    """Organize the given directory by moving files into their respective folders."""
    try:
        # Ensure the directory exists
        if not directory.exists():
            raise FileNotFoundError(f"The directory {directory} does not exist.")

        # Define the target subfolders
        target_folders = ["Documents", "Images\, "Videos", "Music"]

        # Create target folders if they don't exist
        for folder in target_folders:
            folder_path = directory / folder
            if not folder_path.exists():
                folder_path.mkdir()

        # Move files into their respective folders
        for file in directory.iterdir():
            if file.is_file():
                # Determine the file type and move accordingly
                if file.suffix in ['.txt', '.doc', '.pdf']:
                    shutil.move(str(file), str(directory / "Documents" / file.name))
                elif file.suffix in ['.jpg', '.png', '.gif']:
                    shutil.move(str(file), str(directory / "Images" / file.name))
                elif file.suffix in ['.mp4', '.avi', '.mov']:
                    shutil.move(str(file), str(directory / "Videos" / file.name))
                elif file.suffix in ['.mp3', '.wav', '.aac']:
                    shutil.move(str(file), str(directory / "Music" / file.name))
                else:
                    # Handle unknown file types
                    print(f"Unknown file type: {file.name}. Skipping...")
    except FileNotFoundError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    return "Folder structure organized successfully."

# Define the Bottle route for organizing folder structure
@route('/organize', method='GET')
def organize():
    """Handle GET requests to organize the folder structure."""
    try:
        # Get the directory path from the query parameter
        dir_path = request.query.dir_path
        if not dir_path:
            return "Please provide a directory path."

        # Convert the path to a Path object and organize the folder structure
        directory = Path(dir_path)
        result = organize_folder_structure(directory)
        return result
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Define the Bottle route for serving static files
@route('/static/<filepath:path>')
def server_static(filepath):
    "