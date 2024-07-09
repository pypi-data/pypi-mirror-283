
import os

file_name = "setup.py"

file_path = os.path.join(os.getcwd(), file_name)

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist.")


print(file_path)