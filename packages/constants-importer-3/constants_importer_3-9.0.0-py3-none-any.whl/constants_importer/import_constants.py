import sys

def get_constants(system_path: str, root_repo: str):

    # Get path to repo where Constants.py lives.
    head, sep, tail = system_path.partition(root_repo)
    repo_path = head+sep

    # Dynamically reference repo in order to point to relevant Constants.py file.
    sys.path.insert(0, repo_path)
    import Constants

    return Constants

def get_static_data_functions(system_path: str, root_repo: str):
    # Get path to repo where static_data_functions.py lives.
    head, sep, tail = system_path.partition(root_repo)
    repo_path = head+sep+'/common/src'

    # Dynamically reference repo in order to point to file.
    sys.path.insert(0, repo_path)
    import static_data_functions

    return static_data_functions
