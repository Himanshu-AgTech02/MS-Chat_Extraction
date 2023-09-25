import ConfigFile
import FolderCreation
import os
import csv
import logging

log_file_path = f"{FolderCreation.Logs_folder_path}\ProcessLog.log"
# logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

folder_path = ConfigFile.ShareFolder

# Check if the folder is accessible-----------------------------------------------------------------------------------
if os.access(folder_path, os.R_OK):
    logging.info("Folder is accessible")
    print("Folder is accessible")

    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    if csv_files:
        logging.info("CSV file(s) found in the folder")
        print("CSV file(s) found in the folder:")

        for csv_file in csv_files:
            csv_file_path = os.path.join(folder_path, csv_file)
            try:
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)

                    if 'IDs' in csv_reader.fieldnames:
                        logging.info(f"IDs in {csv_file}:")
                        print(f"IDs in {csv_file}:")
                        for row in csv_reader:
                            ids = row['IDs']
                            if ids.strip():
                                print(ids)
                            else:
                                print("No data in the CSV")
                    else:
                        logging.warning(f"No 'IDs' column found in {csv_file}")
                        print(f"No 'IDs' column found in {csv_file}")
            except Exception as e:
                error_message = f"Error reading {csv_file}: {e}"
                logging.error(error_message)
                print(error_message)
    else:
        logging.warning("No CSV files found in the folder")
        print("No CSV files found in the folder.")
else:
    logging.error("Folder is not accessible")
    print("Folder is not accessible")