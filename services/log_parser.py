import re
from datetime import datetime

def valid_dateTime(date_str):
    try:
        datetime.strptime(date_str,r"%Y%m%d")
        return True
    except ValueError:
        return False


def parsing_logs(file_name):
    log_types={
        "error":0,
        "info":0,
        "warning":0
    }
    
    with open(file_name, "r") as file_content:
        content = file_content.readlines()
        #import pdb;pdb.set_trace()
        first_line_value=content[0].split(",")
        only_file_name=file_name.split("\\")[-1].lower()
        if first_line_value[0].lower()!=only_file_name or not valid_dateTime(first_line_value[1].strip()) or not content[-1].strip().isdigit() and int(content[-1].strip()==len(content)-2):
            #import pdb;pdb.set_trace()
            return False


         #content is a list
        for each_line in content:
            type = re.findall(r"(ERROR|INFO|WARNING)",each_line,re.IGNORECASE)
            if len(type)>0:
                type=type[0].lower()
            else:
                continue
            if type=="info":
                log_types["info"] +=1
            elif type =="error":
                log_types["error"] +=1
            elif type == "warning":
                log_types["warning"] +=1
                
    return log_types





            



