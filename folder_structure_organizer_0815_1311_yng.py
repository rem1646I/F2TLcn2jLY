# 代码生成时间: 2025-08-15 13:11:47
from bottle import route, run, request, response
import os
import shutil
from datetime import datetime

# Define the Bottle application
app = application = default_app()

# Define the route for the folder structure organizer
@route('/organize', method='POST')
def organize_folder_structure():
    # Check if the request has a file
    if 'folder_path' not in request.files:
        response.status = 400
        return {"error": "No folder path provided"}
    
    folder_path = request.files['folder_path'].file.read().decode('utf-8')
    
    # Check if the folder path is valid
    if not os.path.exists(folder_path):
        response.status = 404
        return {"error": "Folder path does not exist"}
    
    try:
        organize_folder(folder_path)
        return {"message": "Folder structure organized successfully"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}

# Function to organize the folder structure
def organize_folder(folder_path):
    """
    Organize the folder structure by moving files into subfolders based on file types.
    """
    # Get the list of file extensions and create corresponding subfolders
    file_extensions = {'images': ['.jpg', '.jpeg', '.png', '.gif'],
                      'documents': ['.pdf', '.doc', '.docx', '.txt'],
                      'videos': ['.mp4', '.avi', '.mov', '.mkv'],
                      'audio': ['.mp3', '.wav', '.flac', '.aac']}
    
    for file_extension_set, type_name in file_extensions.items():
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_extension_set):
                    file_path = os.path.join(root, file)
                    target_folder = os.path.join(folder_path, type_name)
                    
                    # Create the target folder if it does not exist
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    
                    # Move the file to the target folder
                    target_file_path = os.path.join(target_folder, file)
                    shutil.move(file_path, target_file_path)

# Run the Bottle application
if __name__ == '__main__':
    run(app, host='localhost', port=8080)