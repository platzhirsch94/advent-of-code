def read_lines_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
