# directory handling
import os # already called in __util_dir_handling, but here for clarity
import shutil
# zipfile handling
import zipfile
# timer
import time # it's cool, so why not
# personal utilities
import __util_dir_handling as udir
from __util_ui_list_selector import ui_list_select
# to be executed
import player_main

def main():

    # startup directory stuff

    udir.set_cwd_to_self()
    
    udir.ensure_folder_present("../GAMES")
    # we want to purge all content in TEMP that might be leftover from previous sessions
    shutil.rmtree("TEMP")
    udir.ensure_folder_present("TEMP")

    # startup message

    print("")
    print("-")
    print("")
    print("This is Peprfish's PYPGP utility.")
    print("Currently still in early development.")
    print("")
    print("-")

    # create list of zipfiles in GAMES

    list_dir_games_all = os.listdir("../GAMES")
    list_dir_games_zip = []
    for file_path in list_dir_games_all:
        if zipfile.is_zipfile(f"../GAMES/{file_path}"):
            # if the file described by file_path is a zipfile
            list_dir_games_zip.append(file_path)

    if len(list_dir_games_zip) >= 1:
        # if there exists at least 1 zip file in GAMES
        print("")
        print("Select a game:")
        selected_game_name = ui_list_select(list_dir_games_zip)
    else:
        # no zip files in GAMES
        print("")
        print("No zip files were found in the GAMES directory.")
        print("Close the program, add some games and then retry.")
        # intentional softlock
        while True:
            pass

    # successful game selection message

    print("")
    print(f"{selected_game_name} was selected.")
    print("")
    print("-")

    # zipfile.extractall() always extracts to cwd, thus we need to update cwd to TEMP

    os.chdir("TEMP")

    # note that this also means we must tailor selected_game_path to this TEMP-centric cwd

    selected_game_path = f"../../GAMES/{selected_game_name}"

    # now we extract the contents of the selected game to TEMP

    with zipfile.ZipFile(selected_game_path, "r") as selected_game:
        print("")
        print("Extracting game assets...")

        # let's add a timer just because it looks cool
        t0 = time.time()
        selected_game.extractall()
        t1 = time.time()

        print("")
        print(f"Extraction successfully completed in {t1 - t0} seconds.")

    # final message before switching to gameplayer

    print("")
    print("Starting game...")

    # startup completed - execute player_main.py

    player_main.main()

def direct_execute_error():

    print("")
    print("This file is not to be executed directly.")
    print("Run main.py instead.")

if __name__ == "__main__":
    direct_execute_error()