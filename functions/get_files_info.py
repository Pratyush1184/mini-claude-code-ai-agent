import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.normpath(os.path.abspath(working_directory))
        target_directory = os.path.normpath(os.path.join(working_directory_abs, os.path.normpath(directory)))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        files_info = f"Result for '{directory}' directory:\n"
        for file in os.listdir(target_directory):
            file_path = os.path.join(target_directory, file)
            file_size = os.path.getsize(file_path)
            file_is_dir = os.path.isdir(file_path)
            files_info += f'- {file}: file_size={file_size} bytes, is_dir={file_is_dir}\n'
        return files_info
    except Exception as e:
        return f'Error:{str(e)}'