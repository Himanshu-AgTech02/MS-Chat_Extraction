import pandas as pd
import json

def run():
    global Outputdir
    global ShareFolder
    global LogFilePath
    global AuditlogTemplateFolder
    global EmailTo
    global EmailCc
    global Client_id
    global Client_secret
    global Grant_type
    global Scope
    global Token_url

    #-------Fetching Config File Data------------------------------------------
    df = pd.read_excel(r"E:\Python(s)\MS-ChatProcess\ConfigFile\MS-ConfigFile.xlsx", header=0, index_col=0)
    c = {index: value for index, value in df.iloc[:, 0].items()}

    json_c = json.dumps(c)
    data = json.loads(json_c)

    Outputdir = data["sOutput"]
    ShareFolder =data['sShareFolder']
    LogFilePath = data['sLogFilePath']
    AuditlogTemplateFolder = data['sAuditlogTemplateFolder']
    EmailTo = data['sEmailTo']
    EmailCc = data['sEmailCc']

    Token_url = data["sToken_url"]
    Client_id = data["sClient_id"]
    Client_secret = data["sClient_secret"]
    Grant_type = data["sGrant_type"]
    Scope = data["sScope"]
run()