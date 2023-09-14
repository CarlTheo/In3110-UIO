"""This is the mane script orchestrating the restructuring and plotting of the content of the pollution_data directory.
"""

# Import necessary packages here
from pathlib import Path
import os
import shutil
from analytic_tools.plotting import plot_pollution_data
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
    display_diagnostics,
)

def restructure_pollution_data(pollution_dir: str | Path, dest_dir: str | Path) -> None:
    """This function searches the tree of pollution_data directory pointed to by pollution_dir for .csv files
        that satisfy the criteria described in the assignment. It then moves a renamed copy of these files to gas-specific
        sub-directories in dest_dir, which will be created based on the gasses present in pollution_data directory.

    Parameters:
        - pollution_dir (str or pathlib.Path) : The absolute path to pollution_data directory
        - dest_dir (str or pathlib.Path) : The absolute path to new directory where gas-specific subdirectories will
                                     be created, which must be pollution_data_restructured/by_gas

    Returns:
    None

    Pseudocode:
    1. Iterate through the contents of `pollution_dir`
    2. Find valid .csv files for gasses ([`[gas_formula].csv` files of correct gas types).
    3. Create/assign new directory to store them under `dest_dir` using `get_dest_dir_from_csv_file`
    4. Assign a new name using `merge_parent_and_basename` and copy the file to the new destination.
       If the file happens already to exist there, it should be overwritten.
    """

    if not isinstance(pollution_dir, (str, Path)) or not isinstance(dest_dir, (str, Path)):
        raise TypeError("Expected a path-like object, but received an invalid type.")

    pollution_dir = Path(pollution_dir)
    dest_dir = Path(dest_dir)

    if not pollution_dir.exists() or not pollution_dir.is_dir():
        raise NotADirectoryError(f"{pollution_dir} either doesn't exist or isn't a directory.")
    
    if not dest_dir.exists() or not dest_dir.is_dir():
        raise NotADirectoryError(f"{dest_dir} either doesn't exist or isn't a directory.")

    for path in pollution_dir.rglob('*'):
        if path.is_file() and is_gas_csv(path):  
           
            dest_sub_dir_path = get_dest_dir_from_csv_file(dest_dir, path)
            
            new_file_name = merge_parent_and_basename(path)
            shutil.copy2(path, dest_sub_dir_path / new_file_name)

def analyze_pollution_data(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data and plot
       the statistics showing emissions of each gas as function of all the corresponding
       sources. The new structure and the plots are saved in a separate directory under work_dir

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the new directories will be created

    Returns:
    None

    Pseudocode:
    - Create pollution_data_restructured in work_dir
    - Populate it with a by_gas subdirectory
    - Make a call to restructure_pollution_data
    - Populate pollution_data_restructured with a subdirectory named figures
    - Make a call to plot_pollution_data
    """
    
    if not isinstance(work_dir, (str, Path)):
        raise TypeError("Expected a path-like object, but received an invalid type.")

    work_dir = Path(work_dir)

    if not work_dir.exists() or not work_dir.is_dir():
        raise NotADirectoryError(f"{work_dir} either doesn't exist or isn't a directory.")
    
    # Create pollution_data_restructured in work_dir
    pollution_dir = work_dir / "pollution_data"
    restructured_dir = work_dir / "pollution_data_restructured"
    
    if not pollution_dir.exists() or not pollution_dir.is_dir():
        raise NotADirectoryError(f"{pollution_dir} either doesn't exist or isn't a directory.")
    
    restructured_dir.mkdir(parents=True, exist_ok=True)

    contents = get_diagnostics(pollution_dir)

    display_diagnostics(pollution_dir, contents)

    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_dir / "by_gas"
    by_gas_dir.mkdir(parents=True, exist_ok=True)

    # Make a call to restructure_pollution_data
    restructure_pollution_data(pollution_dir, by_gas_dir)

    # Populate pollution_data_restructured with a sub folder named figures
    figures_dir = restructured_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Make a call to plot_pollution_data
    plot_pollution_data(by_gas_dir, figures_dir)
    

def analyze_pollution_data_tmp(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data in a temporary directory and create the figures
       showing emissions of each gas as function of all the corresponding
       sources. The new figures are saved in a real directory under work_dir.

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the figures will be saved

    Returns:
    None

    Pseudocode:
    - Create a temporary directory and copy pollution_data directory to it
    - Perform the same operations as in analyze_pollution_data
    - Copy (or directly save) the figures to a directory named `figures` under the original working directory pointed to by `work_dir`
    """

    # NOTE: This is a bonus task, if you are skipping it, remove `raise NotImplementedError()`
    # in the function body
    raise NotImplementedError("Remove me if you implement this optional task")

if __name__ == "__main__":
    # Create a variable holding the path to your working directory
    work_dir = os.getcwd()
    # Make a call to analyze_pollution_data
    analyze_pollution_data(work_dir)

