import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python script in a specified file_path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory (default is the working directory itself) where the python script resides",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional arguments list to pass to the python script",
            )
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.normpath(os.path.abspath(working_directory))
        target_file = os.path.normpath(os.path.join(working_directory_abs, os.path.normpath(file_path)))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                                           , timeout=30)
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout is None and completed_process.stderr is None:
            return f"No output produced"
        return_string = ""
        if completed_process.stdout is not None:
            return_string += f"STDOUT:{completed_process.stdout}\n"
        if completed_process.stderr is not None:
            return_string += f"STDERR:{completed_process.stderr}\n"
        return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"