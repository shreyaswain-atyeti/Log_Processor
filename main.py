import services.log_parser as log_parser
import utils.db_connection as db_connect
import os
import logging
import zipfile
import services.generate_json
import json
import shutil

logging.basicConfig(
    filename='db_connection_issues.log',            
    filemode='a',                     
    format='%(asctime)s - %(levelname)s - %(message)s',                 
)

def cut_files_to_archive():
    archive_folder_path = r"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\Log_processor_git\Log_Processor\logs\archive"
    input_folder_path = r"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\Log_processor_git\Log_Processor\logs\input"
    
    for files in os.listdir(input_folder_path):
        if os.path.exists(os.path.join(archive_folder_path,files)):
            os.remove(os.path.join(archive_folder_path,files))
        shutil.move(os.path.join(input_folder_path,files),archive_folder_path)

log_folder_path = r"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\Log_processor_git\Log_Processor\logs\input"
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
    final_json=services.generate_json.create_json(file_dict[file_name])
    json_file_name=f"{file_name}.json"
    if os.path.exists(json_file_name):
        open(json_file_name, 'w').close()
    with open(rf"C:\Users\ShreyaSwain\OneDrive - Atyeti Inc\Desktop\Log_processor_git\Log_Processor\logs\output\{json_file_name}", "w") as file:
        json.dump(final_json, file, indent=4) 

    try:
        db_connect.add_into_db(file_name,log_types)
        print(f"Values added successfully in db for {file_name}")
    except Exception as e:
        print(f"Got this error {e}")
        logging.error("Error in db")


cut_files_to_archive()


    

