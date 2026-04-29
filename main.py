import os
import shutil
import json
import time
import logging

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

DOWNLOADS_PATH = os.path.expanduser(config["download_path"])
IGNORE_EXTENSIONS = config["ignore_extensions"]

# Setup logging
logging.basicConfig(
    filename="automation_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def organize_files():
    start_time = time.time()

    summary = {
        "total_files": 0,
        "moved": 0,
        "ignored": 0,
        "errors": 0
    }

    if not os.path.exists(DOWNLOADS_PATH):
        logging.error("Downloads folder not found.")
        return

    for file in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, file)

        if not os.path.isfile(file_path):
            continue

        summary["total_files"] += 1

        try:
            ext = file.split(".")[-1] if "." in file else "no_extension"

            if ext in IGNORE_EXTENSIONS:
                summary["ignored"] += 1
                logging.info(f"Ignored {file}")
                continue

            folder_path = os.path.join(DOWNLOADS_PATH, ext)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            shutil.move(file_path, os.path.join(folder_path, file))

            summary["moved"] += 1
            logging.info(f"Moved {file} -> {ext}/")

        except Exception as e:
            summary["errors"] += 1
            logging.error(f"Error processing {file}: {str(e)}")

    end_time = time.time()

    print("\n--- SUMMARY REPORT ---")
    print(summary)
    print(f"Execution Time: {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    organize_files()
