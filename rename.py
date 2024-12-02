import os

# Specify the directory where your .xlsx files are located
base_directory = r"C:\Users\Jayed\Desktop\ebook"

# Walk through the base directory
for root, dirs, files in os.walk(base_directory):
    # Check if there are any .xlsx files in the current directory
    if any(file.endswith(".xlsx") for file in files):
        for dir_name in dirs:
            if dir_name.lower() == "images":
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, "IMAGES")
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} to {new_path}")
