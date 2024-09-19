import os

def search(entrance_term: str, search_term: str):
    if os.path.isdir(entrance_term):
        try:
            files = os.listdir(entrance_term)
            for file in files:
                print(file)
        except PermissionError:
            print("Permission denied: Unable to access some directories.")
        except FileNotFoundError:
            print("The directory does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif os.path.isfile(entrance_term):
        try:
            with open(entrance_term, 'r') as file:
                content = file.read()
                print(content)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
    else:
        print(f"{entrance_term} does not exist.")