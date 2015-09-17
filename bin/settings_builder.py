import os

def create_settings():
    """
    Safely creates a `local.py` in the `settings` directory, if one does not
    exist.
    """
    target_path = os.path.join('..', 'playbook', 'config', 'settings', 'local.py')

    print("Checking to see if {0} exists...".format(target_path))

    if not os.path.exists(target_path):
        print("{0} not found. Creating it!".format(target_path))
        open(target_path, 'w').close()

if __name__ == __main__:
    create_settings()
