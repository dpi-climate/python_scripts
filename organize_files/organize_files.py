import os
import shutil

source_folders = [
    "WRF_2019_faltantes_4",
    "WRF_2019_faltantes_3",
    "WRF_2019_faltantes_2",
    "WRF_2019_faltantes",
    "WRF_Abril_2019_4_schemes_002",
    "WRF_Abril_2019_4_schemes",
]

destination_folder = "1_Organized"

os.makedirs(destination_folder, exist_ok=True)

copied_files = set()

for folder in source_folders:
    print(f"Active Folder: {folder}")
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            if os.path.isfile(file_path) and filename not in copied_files:
                shutil.copy(file_path, os.path.join(destination_folder, filename))
                copied_files.add(filename)
    else:
        print(f"Folder '{folder}' does not exist.")

print("Files copied successfully!")
