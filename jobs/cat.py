from datetime import datetime


def write_cat_to_file():
    with open("cat_file.txt", "a") as file:
        file.write("cat\n")
        print(f"Wrote 'cat' to file at {datetime.now()}")
