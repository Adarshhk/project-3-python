import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
          

        abs_working_dir = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(abs_working_dir , file_path))

        is_valid = os.path.commonpath([abs_working_dir , target_path]) == abs_working_dir

        if not is_valid:
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' )

        if os.path.isdir(target_path):
                    return (
                        f'Error: Cannot write to "{file_path}" as it is a directory'
                    )

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path , "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write content inside a file relative to the working directory, providing file path and working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to write content inside, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "content to write inside the file provided",
                },
            },
        },
    },
}