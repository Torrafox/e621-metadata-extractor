import hashlib
import oshash
import os

def calculate_md5(file_path):
    """
    Calculates the MD5 checksum of a file.
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating MD5 for {file_path}: {e}")
        return None
    
def calculate_oshash(file_path, print_size_error=False):
    """
    Calculates the OSHash (Open Semantic Hash) of a given file.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        str: The calculated OSHash as a hexadecimal string.
    """
    try:
        # Check the file size
        file_size = os.path.getsize(file_path)
        if file_size < 128 * 1024:  # 128 KB
            raise ValueError(f"File size must be at least 128 KB, but it is {file_size / 1024} KB.")
        
        return oshash.oshash(file_path)
    except ValueError as ve:
        if print_size_error:
            print(f"OSHash calculation skipped for file '{file_path}': {ve}")
        return None
    except Exception as e:
        print(f"Error calculating OSHash for file '{file_path}': {e}")
        return None