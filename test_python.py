import os

def search_string_in_files(root_dir, search_string):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                if search_string in file.read():
                    print(f'Found in file: {file_path}')

if __name__ == "__main__":
    root_directory = "/path/to/your/project"
    secret_key = "your_secret_key"
    search_string_in_files(root_directory, secret_key)