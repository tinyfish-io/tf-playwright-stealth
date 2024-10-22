import os


def from_file(name) -> str:
    """Read script from ./js directory"""
    base_path = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(base_path, "..", "playwright_stealth"))
    js_folder_path = os.path.join(project_root, "js")
    file_path = os.path.join(js_folder_path, name)

    print(f"Reading script from {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")

    with open(file_path, encoding="utf-8") as f:
        return f.read()
