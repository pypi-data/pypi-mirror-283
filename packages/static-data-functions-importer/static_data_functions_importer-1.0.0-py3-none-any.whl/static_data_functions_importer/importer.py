import sys

def get_static_data_functions(system_path: str):

    # Get path to repo where Constants.py lives.
    head, sep, tail = system_path.partition("platform-enablement")
    repo_path = head+sep+"/common/src"

    # Dynamically reference repo in order to point to relevant Constants.py file.
    sys.path.insert(0, repo_path)
    import static_data_functions

    return static_data_functions