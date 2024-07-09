import sys

def get_constants(system_path: str, partition_str: str):

    # Get path to repo where Constants.py lives.
    head, sep, tail = system_path.partition(partition_str)
    root_repo_path = head+sep
    static_data_functions_dir_path = root_repo_path+"/common/src"

    # Dynamically reference repo in order to point to relevant Constants.py file.
    sys.path.insert(0, root_repo_path)
    import Constants

    # Dynamically reference static data functions parent dir in order to point to static_data_functions.py.

    sys.path.insert(0, static_data_functions_dir_path)
    import static_data_functions

    return Constants, static_data_functions