import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        abs_working_dir = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(abs_working_dir , file_path))

        is_valid = os.path.commonpath([abs_working_dir , target_file]) == abs_working_dir

        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file] + (args or [])

        process = subprocess.run(
            command,
            cwd=abs_working_dir,
            timeout=30,
            text=True,
            capture_output=True
        )
        output_string = ""
        if process.returncode != 0:
            output_string += f"Process exited with code {process.returncode}\n"
        print(process.stdout)
        if process.stdout:
            output_string += f"STDOUT: {process.stdout}\n"
        else:
            output_string += "STDOUT: \n"

        if process.stderr:
            output_string += f"STDERR: {process.stderr}\n"
        else:
            output_string += "STDERR: \n"

        return output_string

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "run a file relative to the working directory, providing file path and working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list",
                    "description": "List of arguments to pass while running a file",
                },
            },
        },
    },
}