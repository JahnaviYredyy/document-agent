import hashlib
import shutil
from pathlib import Path

STORAGE_DIR=(Path(__file__).resolve().parents[2]/"data"/"storage")
def calculate_hash(file_path:Path)->str:
  """calculate the SHA-256 hash of a file"""

  sha256=hashlib.sha256()

  with file_path.open("rb")as file:
      for chunk in iter(lambda:file.read(4096),b""):
          sha256.update(chunk)

  return sha256.hexdigest()

def copy_to_storage(file_path:Path,file_hash:str)->Path:
    """copy a file into managed storage"""

    STORAGE_DIR.mkdir(parents=True,exist_ok=True)

    destination=STORAGE_DIR / f"{file_hash}_{file_path.name}"

    shutil.copy2(file_path, destination)  #Copies the original file into aplications storage

    return destination