import os
import datetime
import shutil
import traceback
import ConfigFile

try:
    full_path = os.path.realpath(__file__)
    file_name = os.path.splitext(os.path.basename(full_path))[0]

    # global current_date
    current_date = datetime.date.today().strftime('%d-%m-%Y')

    # --------Local device Output Folder---------------
    Local_Device_Output_Folder = os.path.join(ConfigFile.Outputdir, "Output")
    os.makedirs(Local_Device_Output_Folder, exist_ok=True)

    # Create the Currentdate folder
    currentdate_folder = os.path.join(Local_Device_Output_Folder, current_date)
    os.makedirs(currentdate_folder, exist_ok=True)
    print("Current Date Fodler: ", currentdate_folder)

    logsfolders = "Logs"
    Logs_folder_path = os.path.join(currentdate_folder, logsfolders)
    os.makedirs(Logs_folder_path, exist_ok=True)

    print("Folder Structure Created")
except Exception as e:

    tb = traceback.extract_tb(e.__traceback__)
    print(tb)
    line_number = tb[-1][1]
    print(line_number)
    # Email_AutomationSSM.error_Mail(file_name,line_number,e)