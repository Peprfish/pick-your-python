import os
import inspect

def set_cwd_to_self():

    # must be called at first

    # Sets current working directory to this file's own directory (CODE)
    os.chdir(os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))))

def ensure_folder_present(path_str):

    # Ensures the presence of a folder outlined by path_str

    # path_str is something like "..\DATA"

    if not os.path.exists(path_str):
        os.makedirs(path_str)

def get_textfile_contents(path_str):

    # returns a list of lines in the textfile outlined by path_str, rstripped

    file = open(path_str, "r")

    contents_unformatted = file.readlines()
    contents_formatted = [line.rstrip("\n") for line in contents_unformatted]

    file.close()

    return contents_formatted

def main():
    pass

if __name__ == "__main__":
    main()