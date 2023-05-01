def error_message():

    print("")
    
    print("INVALID INPUT")

def ui_list_select(choice_list):

    # prints a basic user interface that allows the user to select an element from a list

    if len(choice_list) == 0:
        # in the event that choice_list is empty, simply return None
        return None

    print("")

    for i in range(len(choice_list)):
        print(f"[{i}] - {choice_list[i]}")

    res_id = -1

    while not ((res_id >= 0) and (res_id < len(choice_list))):

        print("")

        try:
            res_id = int(input(">> "))
            if res_id >= 0:
                selection = choice_list[res_id]
            else:
                error_message()
        except ValueError:
            error_message()
        except IndexError:
            error_message()

    return selection

def main():
    pass

if __name__ == "__main__":
    main()