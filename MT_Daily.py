import datetime
print("start time", datetime.datetime.now())
import ConfigFile
import FolderCreation
import datetime
import os
import requests
import csv
import pandas as pd
import logging
import time
import shutil
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import pygetwindow as gw
import re
from datetime import timedelta, date
from concurrent.futures import ThreadPoolExecutor
import threading
import traceback
import Email_Automation
from bs4 import BeautifulSoup
import pyautogui
import numpy as np

full_path = os.path.realpath(__file__)
files_namess = os.path.splitext(os.path.basename(full_path))[0]

try:
    # Create a lock for thread safety
    thread_lock = threading.Lock()
    logging.info("Starting Fetching the Chat from Chats on Daily Basis")

    # Function to fetch chat messages
    def fetch_and_process_chat_data(csv_file_path, group_name):
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            if 'Chat_ID' in csv_reader.fieldnames:
                for row in csv_reader:
                    Chat_Status = row['ChatStatus']
                    print(f"!@#$%^&*(*) {Chat_Status}")
                    if Chat_Status == 'Active':
                        print(f"+++++++++CHATTTT {Chat_Status} ")

                        ids = row['Chat_ID']
                        Gname = row['ChatName']
                        if ids.strip():
                            id_list = ids.split(',')
                            current_datess = datetime.datetime.now()
                            current_datess = current_datess.strftime('%B-%Y')
                            Group_Name_Folder = os.path.join(FolderCreation.currentdate_folder, Gname)
                            os.makedirs(Group_Name_Folder, exist_ok=True)
                            Group_Attachment_Folder = os.path.join(Group_Name_Folder, fr"{Gname}_Attachment")
                            os.makedirs(Group_Attachment_Folder, exist_ok=True)

                            token_url = ConfigFile.Token_url
                            data = {
                                "client_id": ConfigFile.Client_id,
                                "client_secret": ConfigFile.Client_secret,
                                "grant_type": ConfigFile.Grant_type,
                                "scope": ConfigFile.Scope
                            }
                            response = requests.post(token_url, data=data)

                            if response.status_code == 200:
                                token_data = response.json()
                                access_token = token_data.get("access_token")
                                # Fetch all messages for the chat
                                all_chat_messages = fetch_all_messages(ids, access_token, group_name)
                                logging.info(f"Fetched the Chat of {ids}")

                                if all_chat_messages:
                                    try:
                                        # Initialize lists to store message data
                                        message_data = []
                                        content_message = []
                                        # name_parts =[]
                                        a = 1
                                        for message in all_chat_messages:
                                            message_id = message.get('id')
                                            created_date = message.get('createdDateTime')
                                            from_user = message.get('from')

                                            if from_user is not None and 'user' in from_user:
                                                user_name = from_user['user'].get('displayName')
                                                user_id = from_user['user'].get('id')
                                            else:
                                                user_name = 'N/A'
                                                user_id = 'N/A'

                                            content = message.get('body', {}).get('content')
                                            content_message = message.get('body', {}).get('content')
                                            content_type = message.get('body', {}).get('contentType')
                                            last_modified = message.get('lastModifiedDateTime')
                                            last_item = ""
                                            name_parts = ""

                                            attachments = message.get('attachments', [])
                                            # print('@#$', attachments)
                                            if not attachments:
                                                # print("ATT", content)
                                                if content == "<systemEventMessage/>":
                                                    continue

                                                if re.search(r'<img\s[^>]*>', content):
                                                    # If 'content' contains image tags, print it as it is
                                                    # print("Image Tag:", content)
                                                    content_message = "Screenshot Attachment"  # Set content_message to the current content
                                                    print(f"BBBB{a}", content_message)
                                                else:
                                                    # If 'content' doesn't contain image tags, remove tags and add the message to the list
                                                    content_without_tags = re.sub(r'<[^>]*>', '', content)
                                                    # print("Message:", content_without_tags)
                                                    content_message = content_without_tags
                                                    print(f"qwerty{a}", content_message)
                                                    print("asd", content_message)
                                                    # content_message = content_message.replace("&nbsp;", "")

                                            else:
                                                # pass
                                                # content_message = ""
                                                content_without_tags = re.sub(r'<[^>]*>', '', content)
                                                # print("Message:", content_without_tags)
                                                # content_message = content_without_tags.replace("", "")
                                                content_message = content_without_tags
                                            # print("MES", content_message)
                                            content_message = content_message.replace("&nbsp;", "")

                                            attachment_urls_per_message = [item.get("contentUrl") for item in attachments]

                                            # Split content by "</attachment>" and extend the lists
                                            if content:
                                                content_parts = content.split("</attachment>")
                                                # name_parts = content.split("</attachment>")
                                            else:
                                                content_parts = []
                                                # name_parts = []

                                            max_length = max(len(attachment_urls_per_message), len(content_parts))

                                            # name_parts = ""
                                            for i in range(max_length):
                                                attachment_url = attachment_urls_per_message[i] if i < len(
                                                    attachment_urls_per_message) else None

                                                if attachment_url and attachment_url.strip():
                                                    match = re.search(r'/([^/]+)$', attachment_url)
                                                    # pattern = r"\/([^\/]+)$"
                                                    # match = re.search(pattern, match)
                                                    # print("=====----MMAATTCCHH----=======", match)
                                                    if match:
                                                        match_value = match.group(1)
                                                        # Replace '%20' with a space
                                                        match_value = match_value.replace('%20', ' ')
                                                        print("=====---------MMAATTCCHH---------=======", match_value)
                                                        content_parts.append(match_value)
                                                        # name_parts.append(match_value)
                                                        name_parts = match_value
                                                        # print("CONT", match_value)
                                                    else:
                                                        content_parts.append("No match found")
                                                        # name_parts.append("")
                                                        name_parts = ""
                                                    # name_parts = match_value

                                                else:
                                                    name_parts = ""
                                                    content_parts.append(content_parts[i] if i < len(
                                                        content_parts) else None)  # Handle the case where the attachment URL is blank
                                                # print('A', content_parts)
                                                for item in content_parts:
                                                    if item:
                                                        print('AA', item)
                                                        # Parse the item with BeautifulSoup
                                                        soup = BeautifulSoup(item, 'html.parser')

                                                        # Check if the item contains an image tag
                                                        img_tag = soup.find('img')
                                                        if img_tag:
                                                            src_value = img_tag.get('src')
                                                            # print("AA", item)
                                                            if src_value:
                                                                # last_item = f"{ConfigFile.Before}{src_value}{ConfigFile.After}"
                                                                last_item = content
                                                                name_parts = item
                                                            else:
                                                                last_item = "No src attribute found"
                                                        else:
                                                            # If no image tag is found, extract the text content
                                                            # Check if the value contains HTML tags
                                                            if BeautifulSoup(item, "html.parser").find():
                                                                # last_item = soup.get_text()
                                                                print(f"Contains HTML tags: {item}")
                                                            else:
                                                                print(f"Without HTML tags: {item}")
                                                            # print('AA', item)

                                                            # print('BB', last_item)
                                                    else:
                                                        last_item = ""
                                                # name_parts = match_value
                                                # print(last_item)
                                                a = a + 1
                                                logging.info(
                                                    f"Extracting Required Details from Chat and Appending it in CSV file")
                                                message_data.append({
                                                    'Created Datetime': created_date,
                                                    'User Name': user_name,
                                                    'Message': content_message,
                                                    'Attachment Name': name_parts,
                                                    'Attachment Url': attachment_url,
                                                    'Last Modified Date': last_modified
                                                })

                                        # Create a DataFrame
                                        df = pd.DataFrame(message_data)
                                        # Define the condition to drop rows where 'Message', 'Attachment Name', and 'Attachment Url' are all blank
                                        condition = (df['Message'].isna() | (df['Message'] == '')) & (
                                                    df['Attachment Name'].isna() | (df['Attachment Name'] == '')) & (
                                                                df['Attachment Url'].isna() | (df['Attachment Url'] == ''))
                                        # Drop rows that meet the condition
                                        df = df[~condition]

                                        if os.path.exists(f"{Group_Name_Folder}\\{Gname}.csv"):

                                            # If the CSV file already exists, read it and append the new data
                                            existing_df = pd.read_csv(f"{Group_Name_Folder}\\{Gname}.csv")
                                            combined_df = pd.concat([df, existing_df], ignore_index=True)
                                            combined_df.to_csv(f"{Group_Name_Folder}\\{Gname}.csv", index=False)
                                            logging.info(f"CSV File with Output Data is Append in the Output Folder")
                                        else:
                                            # If the CSV file doesn't exist, create a new one
                                            df.to_csv(f"{Group_Name_Folder}\\{Gname}.csv", index=False)
                                            logging.warning(f"CSV File has not Found, Created new {Group_Name_Folder}\\{Gname}.csv")


                                    except Exception as e:
                                        print(f"Error processing message: {str(e)}")
                                        logging.error(f"Error CSV File message: {str(e)}")
                                        # tb = traceback.extract_tb(e.__traceback__)
                                        # line_number = tb[-1][1]
                                        # print("LineError", line_number)
                                        # print(f"Message ID: {message_id}")
                                        # print(f"Content: {content}")
                                else:
                                    print(f"No messages found for chat ID: {ids}")
                                    logging.warning(f"No messages found for chat ID: {ids}")
                            else:
                                print(f"API request failed with status code {response.status_code}")
                                logging.warning(f"API request failed with status code {response.status_code}")
                        else:
                            print("No data in the CSV")
                            logging.warning(f"No data in the Input CSV File")
                    else:
                        print(f"=======----This {Chat_Status} is Inactive---=============")

    # Function to fetch all messages
    def fetch_all_messages(chat_id, access_token, group_name):
        api_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages?$top=50"
        headers = {"Authorization": f"Bearer {access_token}"}
        all_messages = []
        api_url_creation_count = 0  # Initialize a variable to count the times api_url is created
        condition_break = False  # Initialize a flag to control the loop

        # Calculate the cutoff date (yesterday's date)
        cutoff_date = (datetime.datetime.now() - timedelta(days=1)).date()

        while api_url and not condition_break:
            api_url_creation_count += 1  # Increment the counter each time api_url is created
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                messages = response_data.get('value', [])
                if not messages:
                    break

                for message in messages:
                    print('TIMEEEEE', message['createdDateTime'])
                    # Define the regular expression pattern
                    pattern = r'\d{4}-\d{2}-\d{2}'
                    # Use re.findall to find all matches
                    matches = re.findall(pattern, message['createdDateTime'])
                    # Fetch the first (and in this case, only) match
                    date_re = matches[0] if matches else None
                    now_date = datetime.date.today()
                    now_yes = date.today()
                    # Calculate yesterday's date
                    yesterday = now_yes - timedelta(days=1)
                    print('yesterday', yesterday)
                    # if str(date_re) != str(now_date) and str(date_re) != str(yesterday):
                    if str(date_re) == str(now_date):
                        continue
                    elif str(date_re) != str(yesterday):
                        print('BREAK')
                        condition_break = True
                        break
                    all_messages.append(message)
                next_link = response_data.get('@odata.nextLink')
                api_url = next_link
        print(f"Number of times 'api_url' was created: {api_url_creation_count}")

        return all_messages

    # # Specify the folder path
    # folder_path1 = ConfigFile.SearchFilePath
    # # Specify the file name you want to check
    # file_name = 'Run_Daily_Chat.csv'
    # # Create the full file path by joining the folder path and file name
    # full_file_path = os.path.join(folder_path1, file_name)

    # # Check if the file exists
    # if os.path.exists(full_file_path):
    #     print('YES')

    folder_path = ConfigFile.ShareFolder
    if os.access(folder_path, os.R_OK):
        logging.info("Folder is accessible")
        print("Folder is accessible")

        csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

        if csv_files:
            logging.info("CSV file(s) found in the folder")
            print("CSV file(s) found in the folder:")

            # Create a list to hold thread objects
            threads = []

            for csv_file in csv_files:
                csv_file_path = os.path.join(folder_path, csv_file)
                group_name = os.path.splitext(csv_file)[0]
                thread = threading.Thread(target=fetch_and_process_chat_data, args=(csv_file_path, group_name))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()
        else:
            logging.warning("No CSV files found in the folder")
            print("No CSV files found in the folder.")
    else:
        logging.error("Folder is not accessible")
        print("Folder is not accessible")
    # else:
    #     print('Run_Daily_Chat file is not present')

    #==============================================================================================================================
    logging.info("Daily Attachment Download Part has been Started")
    CDT = datetime.datetime.now()
    valid_date_str = CDT.strftime("%d-%m-%Y")

    current_datess = datetime.date.today().strftime('%B-%Y')
    # Specify the folder where your CSV files are located
    folder_pathss = fr"{ConfigFile.LogFilePath}\{valid_date_str}"
    # chrome_command = fr'@echo off & cd {ConfigFile.ChromeApplicationPath} & start chrome.exe --remote-debugging-port=2023 --user-data-dir={ConfigFile.ChromeDriverPath}'
    # subprocess.Popen(chrome_command, shell=True)
    # time.sleep(2)
    logging.info("Opened Chrome Application")
    # Specify the directory containing your folders
    root_directory = fr"{ConfigFile.LogFilePath}\{current_datess}"
    # Iterate through all subdirectories (folders) in the root directory
    for folder_name in os.listdir(root_directory):
        folder_pathss = os.path.join(root_directory, folder_name)
        # Check if the item is a directory
        if os.path.isdir(folder_path):
            # print(f"Processing folder: {folder_name}")
            if folder_name == "Logs":
                continue
            else:

                # Loop through all files in the folder
                for filenamess in os.listdir(folder_pathss):

                    # Check if the file is a CSV file (you can use a more specific check if needed)
                    if filenamess.endswith('.csv'):
                        # Construct the full path to the CSV file
                        file_pathss = os.path.join(folder_pathss, filenamess)
                        logging.info(f"Access the Output CSV file {filenamess} and Fetch the Attachment URL's")
                        opt = Options()
                        opt.add_experimental_option("debuggerAddress", "localhost:2023")
                        service = Service(ConfigFile.WebDriver)
                        driver = webdriver.Chrome(service=service, options=opt)
                        print("Attachment Download Starts Here..............")

                        # chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
                        # chrome_window.activate()

                        time.sleep(3)
                        file_path = file_pathss
                        df = pd.read_csv(file_path)
                        b=0
                        # Load the CSV file into a Pandas DataFrame
                        df = pd.read_csv(file_path)

                        # Define the function to extract image source values
                        def extract_img_src(content):
                            if pd.isna(content) or not isinstance(content, str):
                                return []
                            soup = BeautifulSoup(content, 'html.parser')
                            img_tags = soup.find_all('img')
                            src_values = [tag.get('src') for tag in img_tags]
                            return src_values

                        # Check if the "Created Datetime" column includes "2023-10-19" and apply the logic to the "Content Type" column
                        for index, row in df.iterrows():
                            created_datetime = row['Created Datetime']
                            content = row['Attachment Name']
                            current_date = datetime.datetime.now()
                            previous_date = current_date - timedelta(days=1)
                            Previous_ChatDate = previous_date.strftime('%Y-%m-%d')

                            # Check if the "Created Datetime" column includes "2023-10-19"
                            if Previous_ChatDate in created_datetime:
                                src_values = extract_img_src(content)
                                if src_values:
                                    print(f"Extracted src values for row at index {index}:-  {src_values}")

                                    token_url = ConfigFile.Token_url  # You'll need to define ConfigFile and its Token_url
                                    # Use token_url as needed

                                    data = {
                                        "client_id": ConfigFile.Client_id,
                                        "client_secret": ConfigFile.Client_secret,
                                        "grant_type": ConfigFile.Grant_type,
                                        "scope": ConfigFile.Scope
                                    }
                                    response = requests.post(token_url, data=data)
                                    if response.status_code == 200:
                                        token_data = response.json()
                                        access_token = token_data.get("access_token")

                                        # Iterate through each URL in src_values
                                        for file_download_url in src_values:
                                            headers = {
                                                "Authorization": f"Bearer {access_token}"
                                            }
                                            file_response = requests.get(file_download_url, headers=headers)
                                            if file_response.status_code == 200:
                                                # Generate a unique filename using the current timestamp (milliseconds)
                                                current_MS = int(time.time() * 1000)
                                                file_path = rf"{root_directory}\{folder_name}\{folder_name}_Attachment\{current_MS}_Screenshot.jpg"
                                                with open(file_path, 'wb') as file:
                                                    file.write(file_response.content)
                                                print(f"File downloaded and saved at: {file_path}")
                                            else:
                                                print(f"File download failed for URL: {file_download_url} with status code {file_response.status_code}")
                                                logging.warning(f"Screenshot download failed for URL: {file_download_url} with status code {file_response.status_code}")
                                    else:
                                        print(f"Token request failed with status code {response.status_code}")
                                        logging.warning(f"Token request failed with status code {response.status_code}")

                        # Add the 'Image_Src' column to the DataFrame
                        df['Screenshot URL'] = df['Attachment Name'].apply(extract_img_src)
                        df['Screenshot URL'] = df['Screenshot URL'].apply(lambda x: ', '.join(x))

                        for index, row in df.iterrows():
                            if pd.isna(row["Attachment Url"]):
                                continue
                            Created_Date_Time = row['Created Datetime']
                            patternss = r'\d{4}-\d{2}-\d{2}'
                            # Use re.findall to find all matches
                            matchesss = re.findall(patternss, Created_Date_Time)
                            # Fetch the first (and in this case, only) match
                            date_ress = matchesss[0] if matchesss else None
                            now_datess = datetime.date.today()
                            # Get the current date
                            now_yesss = date.today()
                            # Calculate yesterday's date
                            yesterdayss = now_yesss - timedelta(days=1)
                            if str(date_ress) == str(yesterdayss):
                                value = row["Attachment Url"]
                                b=b+1
                                if value.endswith((".txt", ".png", ".jpg", ".jpeg", ".jif", ".webm", ".pdf")):
                                    file_name = os.path.basename(value)
                                    file_name_parts = os.path.splitext(file_name)
                                    file_name_without_extension = file_name_parts[0]
                                    file_extension = file_name_parts[1]
                                    file_with_ex = file_name_without_extension + file_extension
                                    driver.get(value)
                                    time.sleep(1)
                                    # Check the tab title for "Access required"
                                    if "Access required" in driver.title:
                                        print("File not accessible")
                                        time.sleep(1)
                                        # df.at[a - 1, 'Status'] = "File not accessible"
                                        df.at[index, 'Status'] = "File not accessible"
                                        df.to_csv(file_path, index=False)
                                    else:
                                        time.sleep(1)
                                        pyautogui.hotkey('ctrl', 's')
                                        # pyautogui.press('enter')
                                        time.sleep(3)
                                        pyautogui.typewrite(rf"{root_directory}\{folder_name}\{folder_name}_Attachment\{b}_{file_with_ex}")
                                        time.sleep(2)
                                        pyautogui.press('enter')
                                        df.at[index, 'Status'] = "File is Downloaded and moved in attachment Folder"
                                        df.to_csv(file_path, index=False)
                                else:
                                    driver.get(value)
                                    if "Access required" in driver.title:
                                        print("File not accessible")
                                        time.sleep(3)
                                        file_name = os.path.basename(value)
                                        file_name_parts = os.path.splitext(file_name)
                                        file_name_without_extension = file_name_parts[0]
                                        file_name_without_extension = file_name_without_extension.replace("%20", " ")
                                        # df.at[a - 1, 'Status'] = "File not accessible"
                                        df.at[index, 'Status'] = "File not accessible"
                                        df.to_csv(file_path, index=False)
                                    else:
                                        time.sleep(3)
                                        pyautogui.press('enter')
                                        time.sleep(3)
                                        file_name = os.path.basename(value)
                                        file_name_parts = os.path.splitext(file_name)
                                        file_name_without_extension = file_name_parts[0]
                                        file_name_without_extension = file_name_without_extension.replace("%20", " ")
                                        print("ELSE ka ELSE",file_name_without_extension)
                                    def files_move():
                                            # Specify the download folder path
                                            download_folder = ConfigFile.DownloadsPath
                                            file_patterns = [file_name_without_extension]
                                            # Get the list of files in the downloads folder
                                            files_in_downloads = os.listdir(download_folder)

                                            # Move files based on the matching patterns
                                            for pattern in file_patterns:
                                                matching_files = [file_name for file_name in files_in_downloads if pattern in file_name]
                                                if matching_files:
                                                    # Move the matching files to the corresponding folder
                                                    folder_path = os.path.join(rf"{root_directory}\{folder_name}\{folder_name}_Attachment")
                                                    for file_name in matching_files:
                                                        source_path = os.path.join(download_folder, file_name)
                                                        destination_path = os.path.join(folder_path, file_name)
                                                        shutil.move(source_path, destination_path)
                                                        df.at[index, 'Status'] = "File is Downloaded and moved in attachment Folder"
                                                        df.to_csv(file_path, index=False)
                                                else:
                                                    print(f"No file with pattern '{pattern}' is present in the downloads folder.")
                                                    df.at[index, 'Status'] = "File Unable to move, Please check file in Download folder"
                                                    df.to_csv(file_path, index=False)
                                    files_move()
                        logging.info("Attachment has been Downloaded and Moved in Attachment Folder")
    print("End time", datetime.datetime.now())
except Exception as e:
    print(e)
    tb = traceback.extract_tb(e.__traceback__)
    line_number = tb[-1][1]
    logging.error(f"Main Error:- {e}")
    Email_Automation.errorMail(files_namess,line_number,e)
print("End time", datetime.datetime.now())