import os
import json
import re
from datetime import datetime


def create_json(valid_file):
    
    info = {"message":[],"count":0}
    error = {"message":[],"count":0}
    warning = {"message":[],"count":0}
    with open(valid_file,"r") as valid:
        file_content = valid.readlines()
    for each_line in file_content:
            type = re.findall(r"(ERROR|INFO|WARNING)",each_line,re.IGNORECASE)
            if len(type)>0:
                type=type[0].lower()
                if type=="info":
                    info["count"]+=1
                    info["message"].append(each_line.strip())
                elif type =="error":
                    error["count"]+=1
                    error["message"].append(each_line.strip())
                elif type == "warning":
                    warning["count"]+=1
                    warning["message"].append(each_line.strip())
                
    log_levels = {
         'info':info,
         'error':error,
         'warning':warning
         }
    today = datetime.today()
    
    final_json={
         "file_name":valid_file.split('\\')[-1],
         "date_of_creation": today.strftime("%Y%m%d"),
         "log_levels":log_levels
    }
    return final_json

                
    

