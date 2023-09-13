"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
from pathlib import Path
from typing import Dict, List
import os

def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    """
     # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    dir = Path(dir)
   
    # Check if the path exists
    if not dir.exists():
        raise NotADirectoryError(f"The path {dir} is not a directory.")
    
    # Check if the path is pointing to a directory
    if not dir.is_dir():
        raise NotADirectoryError(f"The path {dir} is not pointing to a directory.")
    
    # Traverse the directory and find its contents
    contents = dir.rglob('*')

    # Count folders and total num. of files
    for path in contents:
     
        if path.is_dir(): # Check if the item is a directory
            res["subdirectories"] += 1
        elif path.is_file(): # Check if the item is a file 
            res["files"] += 1

            # Categorize/count the file based on it's extension
            if path.suffix == '.csv':
                res[".csv files"] += 1
            elif path.suffix == '.txt':
                res[".txt files"] += 1
            elif path.suffix == '.npy':
                res[".npy files"] += 1
            elif path.suffix == '.md':
                res[".md files"] += 1
            # Counts all other files as "other files"
            else:
                res['other files'] += 1

    return res

def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """

    if not dir.exists():
        raise NotADirectoryError(f"The path {dir} is not a directory.")
    
    if not dir.is_dir():
        raise NotADirectoryError(f"The path {dir} is not pointing to a directory.")
    
    if not isinstance(contents, dict):
        raise TypeError(f"Expected a dictionary as the second parametet, but recived another type.")

    print(f"Diagnostics for directory: {dir}\n" + "="*40)
    for key, value in contents.items():
        print(f"{key.capitalize()}: {value}")

    print("="*40)

    # Print the summary to the terminal
    


def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """
    # NOTE: This is a bonus task, if you implementing it, remove `raise NotImplementedError`
    raise NotImplementedError("Remove me if you implement this bonus task")

    ...


def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """
    path = Path(path)

    # Do correct error handling first
    if not isinstance(path, (str, Path)):
        raise TypeError(f"Expected a path, but recived a non path-like object.")
    
    if path.suffix != ".csv":
        raise ValueError(f"{path} does not pont to a .csv file.")
    
    # Extract the filename from the .csv file and check if it is a valid greenhouse gas
    
    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]
    
    return path.stem.upper() in gasses

def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:

    

    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """
    dest_parent = Path(dest_parent)
    file_path = Path(file_path)

    # Do correct error handling first

    if not isinstance(dest_parent, Path) or not isinstance(file_path, Path):
        raise TypeError("Expected a path, but received a non path-like object.")

    if not dest_parent.exists():
        raise NotADirectoryError(f"{dest_parent} does not exist.")

    if not file_path.exists():
        raise ValueError(f"{file_path} does not exist.")

    if not dest_parent.is_dir():
        raise NotADirectoryError(f"{dest_parent} is not pointing to an existing directory.")

    if not file_path.is_file() or file_path.suffix != '.csv':
        raise ValueError(f"{file_path} is not a valid .csv file path.")

    gasses = ['CO2', 'CH4', 'NO2', 'SF6', 'H2']
    if file_path.stem.upper() not in gasses:
        raise ValueError(f"{file_path.stem} is not a recognized gas")

    # If the input file is valid:
   
    # Derive the name of the directory, pattern: gas_[gas_formula] directory
    dest_name = f"gas_{file_path.stem.upper()}"
    
    # Derive its absolute path
    dest_path = dest_parent / dest_name

    # Check if the directory already exists, and create one of not
    if dest_path.exists():
        return dest_path
    else:
        dest_path.mkdir()
        return dest_path
    
def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path

    """
   
    if not isinstance(path, (str, Path)):
        raise TypeError("Expected a path, but received a non path-like object.")
    
    path_object = Path(path)

    if path_object.parent.name == "":
        raise ValueError("The provided path does not have a parent directory.")
    
    # New, merged, basename of the path, which will be the new filename
    new_base = f"{path_object.parent.name}_{path_object.name}".replace(os.sep, '_')
    return new_base


def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    # NOTE: This is an optional task, no points assigned. If you are skipping it, remove `raise NotImplementedError` in the function body
    raise NotImplementedError("Remove me if you implement this optional task")

    ...