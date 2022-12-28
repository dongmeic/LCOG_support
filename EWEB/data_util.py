
def get_data(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)
    
    renamed_file = dest_folder + '\\Ferns_Noaps_Polygons_' + date.today().strftime("%m%d%Y") + '.gdb'

    if not os.path.exists(renamed_file):
        r = requests.get(url, stream=True)
        if r.ok:
            urllib.request.urlretrieve(url, file_path)
            print("Saving to", os.path.abspath(file_path))
    #         with open(file_path, 'wb') as f:
    #             for chunk in r.iter_content(chunk_size=1024 * 8):
    #                 if chunk:
    #                     f.write(chunk)
    #                     f.flush()
    #                     os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_folder)

        extracted_file = dest_folder + '\\Ferns_Noaps_Polygons.gdb' 
        print("Extracting file to", extracted_file)

        os.renames(extracted_file, renamed_file)
        print("Renaming file to", renamed_file)