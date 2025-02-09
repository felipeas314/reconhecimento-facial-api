import os

def save_uploaded_files(files, upload_dir, single=False):
    if single:
        file = files.get("File1")
        if file:
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            return file_path
    else:
        file_paths = []
        for key in files:
            file = files[key]
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)
            file_paths.append(file_path)
        return file_paths
