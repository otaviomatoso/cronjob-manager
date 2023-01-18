from datetime import datetime


class Cat:

    @staticmethod
    def write_to_file_job():
        with open("cat_file.txt", "a") as file:
            file.write("cat\n")
            print(f"Wrote 'cat' to file at {datetime.now()}")
