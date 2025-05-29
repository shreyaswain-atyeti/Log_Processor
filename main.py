import services.log_parser as log_parser
import utils.db_connection as db_connect
import os
import logging
import zipfile

logging.basicConfig(
    filename='db_connection_issues.log',            
    filemode='a',                     
    format='%(asctime)s - %(levelname)s - %(message)s',                 
)




log_folder_path = r"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\N_Pair_Programming_\logs"
file_dict={}

zip_file_list=[]
for file in os.listdir(log_folder_path):
    if file.endswith('.zip'):
        zip_file_list.append(os.path.join(log_folder_path,file))
for zip in zip_file_list:
    with zipfile.ZipFile(zip,'r') as zip_ob:
        zip_ob.extractall(log_folder_path)
    non_txt_files = [f for f in os.listdir(log_folder_path) if not f.endswith('.txt')]

    if len(non_txt_files)>0:
        for non_txt_file in non_txt_files:
            if non_txt_file.endswith('.zip'):
                continue
            logging.info(f"Found non txt file {non_txt_file}")
            print(f"Invalid File file_name , We are expecting only .txt files to process. invalid file for {non_txt_file}")

for file_name in os.listdir(log_folder_path):
    full_path = os.path.join(log_folder_path,file_name)
    if os.path.isfile(full_path) and file_name.endswith('.txt'):
        file_dict[file_name] = full_path
        

for file_name in file_dict:
    log_types = log_parser.parsing_logs(file_dict[file_name])
    if log_types==False:
        print(f"Skipping for {file_name}")
        continue
    

    try:
        db_connect.add_into_db(file_name,log_types)
        print(f"Values added successfully in db for {file_name}")
    except Exception as e:
        print(f"Got this error {e}")
        logging.error("Error in db")
        


    

