""" Test script executing all the necessary unit tests for the functions in analytic_tools/utilities.py module
    which is a part of the analytic_tools package
"""

# Include the necessary packages here
from pathlib import Path

import pytest

# This should work if analytic_tools has been installed properly in your environment
from analytic_tools.utilities import (
    get_dest_dir_from_csv_file,
    get_diagnostics,
    is_gas_csv,
    merge_parent_and_basename,
)


@pytest.mark.task12
def test_get_diagnostics(example_config):
    """Test functionality of get_diagnostics in utilities module

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
                                     from Figure 1 in assignment2.md

    Returns:
    None
    """
    # Remove if you implement this task
    # raise NotImplementedError("Remove me if you implement this mandatory task")
    res = get_diagnostics(example_config / "pollution_data")
    
    # The expected outcomes    
    expected = {
        "files": 10,
        "subdirectories": 4,
        ".csv files": 8,
        ".txt files": 0,
        ".npy files": 2,
        ".md files": 0,
        "other files": 0,
    }

    for key in expected:
        assert res[key] == expected[key]
    ...


@pytest.mark.task12
@pytest.mark.parametrize(
    "exception, dir",
    [
        (NotADirectoryError, "Not_a_real_directory"),
        (TypeError, 2), # Not a path error/input 
        (NotADirectoryError, Path(__file__).absolute()) #inserting a file and not a directory
        # add more combinations of (exception, dir) here
    ],
)
def test_get_diagnostics_exceptions(exception, dir):
    """Test the error handling of get_diagnostics function

    Parameters:
        exception (concrete exception): The exception to raise
        dir (str or pathlib.Path): The parameter to pass as 'dir' to the function

    Returns:
        None
    """

    with pytest.raises(exception):
        get_diagnostics(dir)

    #raise NotImplementedError("Remove me if you implement this mandatory task")

@pytest.mark.task22
def test_is_gas_csv():
    """Test functionality of is_gas_csv from utilities module

    Parameters:
        None

    Returns:
        None
    """
    assert is_gas_csv(Path("CO2.csv")) == True
    assert is_gas_csv(Path("co2.csv")) == True
    assert is_gas_csv(Path("Co2.csv")) == True

    with pytest.raises(ValueError):
        is_gas_csv(Path("CO2.txt"))
    
    with pytest.raises(TypeError):
        is_gas_csv(123)

    assert isinstance(is_gas_csv("CO2.csv"), bool)

    # Testing with things not in the list
    assert is_gas_csv(Path("H2O.csv")) == False
    assert is_gas_csv(Path("123_CO2.csv")) == False
    assert is_gas_csv(Path("??_CO2.csv")) == False

    assert is_gas_csv(Path("CO2.csv")) == True
    assert is_gas_csv(Path("CH4.csv")) == True
    assert is_gas_csv(Path("N2O.csv")) == True
    assert is_gas_csv(Path("SF6.csv")) == True
    assert is_gas_csv(Path("H2.csv")) == True 


@pytest.mark.task22
@pytest.mark.parametrize(
    "exception, path",
    [
        (ValueError, Path(__file__).parent.absolute()),
        # add more combinations of (exception, path) here
        (ValueError, "file.txt"),
        (TypeError, 123),
        (TypeError, None),
        (ValueError, ""),
    ],
)
def test_is_gas_csv_exceptions(exception, path):
    """Test the error handling of is_gas_csv function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'path' to function

    Returns:
    None
    """
    with pytest.raises(exception):
        is_gas_csv(path)
    ...


@pytest.mark.task24
def test_get_dest_dir_from_csv_file(example_config):
    """Test functionality of get_dest_dir_from_csv_file in utilities module.

    Parameters:
        example_config (pytest fixture): a preconfigured temporary directory containing the example configuration
            from Figure 1 in assignment2.md

    Returns:
        None
    """
    dest_parent = example_config / "pollution_data_restructured" / "by gas"

    csv_files = [
        ("H2", "src_agriculture_H2.csv"),
        ("CO2", "src_airtraffic_CO2.csv"),
        ("CO2", "src_oil_and_gass_CO2.csv"),
        ("CH4", "src_oil_and_gass_CH4.csv")
    ]
   
    for gas, csv_file in csv_files:
        expected_dir_path = dest_parent / f"gas_{gas}"

        result_dir = get_dest_dir_from_csv_file(dest_parent, example_config / csv_file)

        assert result_dir == expected_dir_path, f"Expected {expected_dir_path} but got {result_dir}."

        assert expected_dir_path.exists(), f"Directory {expected_dir_path}, was not created."

        assert (expected_dir_path / csv_file).exists(), f"{csv_file} was not found in {expected_dir_path}"



@pytest.mark.task24
@pytest.mark.parametrize(
    "exception, dest_parent, file_path",
    [
        (ValueError, Path(__file__).parent.absolute(), "foo.txt"),
        # add more combinations of (exception, dest_parent, file_path) here
    ],
)
def test_get_dest_dir_from_csv_file_exceptions(exception, dest_parent, file_path):
    """Test the error handling of get_dest_dir_from_csv_file function

    Parameters:
        exception (concrete exception): The exception to raise
        dest_parent (str or pathlib.Path): The parameter to pass as 'dest_parent' to the function
        file_path (str or pathlib.Path): The parameter to pass as 'file_path' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        get_dest_dir_from_csv_file(dest_parent, file_path)

@pytest.mark.task26
def test_merge_parent_and_basename():
    """Test functionality of merge_parent_and_basename from utilities module

    Parameters:
        None

    Returns:
        None
    """
    assert merge_parent_and_basename("/User/documents/myfile.txt") == "documents_myfile.txt"
    assert merge_parent_and_basename("some_dir/some_sub_dir") == "some_dir_some_sub_dir"
    assert merge_parent_and_basename("another_dir/file.txt") == "another_dir_file.txt"

@pytest.mark.task26
@pytest.mark.parametrize(
    "exception, path",
    [
        (TypeError, 33),
        (TypeError, True),
        (ValueError, "no_parent.txt")
        # add more combinations of (exception, path) here
    ],
)
def test_merge_parent_and_basename_exceptions(exception, path):
    """Test the error handling of merge_parent_and_basename function

    Parameters:
        exception (concrete exception): The exception to raise
        path (str or pathlib.Path): The parameter to pass as 'pass' to the function

    Returns:
        None
    """
    with pytest.raises(exception):
        merge_parent_and_basename(path)