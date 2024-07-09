import sys

def get_constants(system_path: str, partition_str: str):

    # Get path to repo where Constants.py lives.
    head, sep, tail = system_path.partition(partition_str)
    repo_path = head+sep

    # Dynamically reference repo in order to point to relevant Constants.py file.
    sys.path.insert(0, repo_path)
    import Constants

    return Constants