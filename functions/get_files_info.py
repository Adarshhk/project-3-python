import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:

        if os.path.isfile(directory):
            return f'Error: "{directory}" is not a directory'

        working_directory_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_directory_abs , directory))

        is_valid = os.path.commonpath([target_dir , working_directory_abs]) == working_directory_abs

        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        res = ""
        print(f"Result for {directory} directory:")
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir , file)
            print(f"    -{file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
            res += f"{file}\n"

        return res
    except Exception as e:
        return f"Error: {str(e)}"

    


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}