import os
from typing import List, Union
import aiofiles
from fastapi import UploadFile


async def save_uploaded_files(files: List[UploadFile], upload_dir: str, single: bool = False) -> Union[str, List[str]]:
    """Salva arquivos enviados via upload."""
    os.makedirs(upload_dir, exist_ok=True)

    if single:
        file = files[0]
        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        return file_path

    file_paths = []
    for file in files:
        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        file_paths.append(file_path)

    return file_paths
