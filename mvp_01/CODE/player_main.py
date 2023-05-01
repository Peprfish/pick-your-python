# directory handling
import os
# personal utilities
import __util_dir_handling as udir
from __util_ui_list_selector import ui_list_select

class Flag:

    # reference dictionary for all flags

    ref_flags = {}

    def __init__(self, name, value, shown, descriptors):

        # self.name is pretty much just used for uploading self to Flag.ref_flags

        self.name = name
        Flag.ref_flags[name] = self

        # self.value is simply the value of the flag itself
        # self.shown describes whether to display the flag's descriptor in status
        # both attributes are booleans

        self.value = value
        self.shown = shown

        # self.descriptor is a list of length 2, where
            # self.descriptor[0] is the flag's T descriptor, and
            # self.descriptor[1] is the flag's F descriptor

        self.descriptors = descriptors

    def alter(self, alteration_type):
        # [*1]
        # change oneself based on the nature of alteration_type
        # nature of changes is self-evident, so no elaboration
        if alteration_type == "T":
            self.value = True
        elif alteration_type == "F":
            self.value = False
        elif alteration_type == "!":
            self.value != self.value
        elif alteration_type == "S":
            self.shown = True
        elif alteration_type == "H":
            self.shown = False

    def description(self):
        # automatically provides a self-description for status
        if self.shown:
            if self.value:
                return self.descriptors[0]
            else:
                return self.descriptors[1]
        else:
            return "None"

class Scenario:

    # reference dictionary for all scenarios

    ref_scenarios = {}

    def __init__(self, name, descriptor, paths):

        # self.name is pretty much just used for uploading self to Scenario.ref_scenarios

        self.name = name
        Scenario.ref_scenarios[name] = self

        # self.descriptor is, naturally, the scenario's descriptor

        self.descriptor = descriptor

        # self.paths is a dictionary of all the paths leading from the scenario
        # if we were to take any key-value pair of self.paths then:
            # key would be the path's descriptor
            # value[0] would be the name of the scenario that the path leads to
            # value[1] would be a list of flag trigger instructions, with elements in pairs:
                # the first elements in the pairs would be the names of the flags to be altered, while
                # the second elements in the pairs would be the nature of the alteration, corresponding
                # to one of ["T", "F", "!", "S", "H"] (see [*1])
            # value[2] would be a dictionary of flag conditionals
                # the keys of path[2] would be the names of all flags of interest, while
                # the values of path[2] would be the required values of said flags
            # (see [*2] for more info about the formatting of value[1] and value[2])

        self.paths = paths

    def play(self):
        
        # basically, if this function is being executed, then that means that this is the current scenario

        print_nl_spam()

        print("")
        print("-")
        print("")
        print("SCENARIO:")
        print("")
        print(self.descriptor)
        print("")
        print("-")

        print_status()

        print("")
        print("-")

        valid_paths = {}

        for key, value in self.paths.items():
            if Scenario.conditionals_met(value[2]):
                # if all the conditionals in the path are met, then copy it over to valid_paths
                valid_paths[key] = value

        if len(list(valid_paths.keys())) == 0:
            # dead end reached - intentional softlock time
            print("")
            print("Dead end reached.")
            print("Manual termination of the program is required.")
            while True:
                pass
        else:
            # next scenario
            chosen_path = self.paths[ui_list_select(list(valid_paths.keys()))]
            Scenario.pull_triggers(chosen_path[1])
            Scenario.ref_scenarios[chosen_path[0]].play()

    def pull_triggers(list_triggers):

        for i in range(0, len(list_triggers), 2):
            Flag.ref_flags[list_triggers[i]].alter(list_triggers[i + 1])

    def conditionals_met(dict_conditionals):

        flags_met = True

        for flag_name, value in dict_conditionals.items():
            if Flag.ref_flags[flag_name].value != value:
                flags_met = False

        return flags_met

def print_nl_spam():

    for i in range(99):
        print("")

def print_status():

    print("")
    print("STATUS:")

    flag_empty_status = True

    for flag in Flag.ref_flags.values():
        temp_description = flag.description()
        if temp_description != "None":
            # if there is something to be described about the flag
            flag_empty_status = False
            print("")
            print(temp_description)
    
    if flag_empty_status:
        print("")
        print("...")

def base_formatter(textfile_contents):

    # helps to rearrange textfile_contents (corresponding to udir.get_textfile_contents(*FILE*))
    # into a more useful format based on the "-" and "=" delimiter elements

    # the output is a 2D list, basically:
    # the elements in the higher-level list are split based on the "=" delimiter,
    # while the elements in the lower-level list are split based on the "-" delimiter
    # consecutive elements in textfile_contents not split by the "-" delimiter are joined together
    # into a conglomerate string in the output list using "\n"s

    output_list = []

    temp_str = ""
    temp_list = []
    for element in textfile_contents:
        if element == "=":
            temp_list.append(temp_str)
            temp_str = ""
            output_list.append(temp_list)
            temp_list = []
        elif element == "-":
            temp_list.append(temp_str)
            temp_str = ""
        else:
            if temp_str == "":
                # to prevent temp_str from starting with a "\n"
                temp_str = element
            else:
                temp_str += "\n" + element
    temp_list.append(temp_str)
    output_list.append(temp_list)

    return output_list

def gen_flag_instance_arguments(name, formatted_contents):

    # creates a list of arguments to be passed into the flag instance initialiser function
    # based on formatted_contents (corresponding to output of base_formatter())
    # oh, and the name of the flag instance is just fed in directly

    # def __init__(self, name, value, shown, descriptors):

    if formatted_contents[0][0] == "T":
        value = True
    elif formatted_contents[0][0] == "F":
        value = False
        
    if formatted_contents[0][1] == "S":
        shown = True
    elif formatted_contents[0][1] == "H":
        shown = False

    descriptors = []
    descriptors.append(formatted_contents[0][2])
    descriptors.append(formatted_contents[0][3])

    return [name, value, shown, descriptors]

def gen_scenario_instance_arguments(name, formatted_contents):

    # creates a list of arguments to be passed into the scenario instance initialiser function
    # based on formatted_contents (corresponding to output of base_formatter())
    # oh, and the name of the scenario instance is just fed in directly

    # def __init__(self, name, descriptor, paths):

    descriptor = formatted_contents[0][0]

    paths = {}

    for i in range(1, len(formatted_contents)): # formatting based on [*2]

        temp_path = formatted_contents[i]
        temp_trigger_dict = mini_format_triggers(temp_path[2])
        temp_conditional_dict = mini_format_conditionals(temp_path[3])

        paths[temp_path[0]] = [temp_path[1], temp_trigger_dict, temp_conditional_dict]

    return [name, descriptor, paths]

# [*2]
# the following mini_format functions help convert:
# "flag1 = T\nflag2 = !\nShow flag3" and "flag1 == T\nflag2 == F"
# into:
# {"flag1": "T", "flag2": "!", "flag3": "S"} and {"flag1": True, "flag2": False}

def mini_format_triggers(trigger_str):

    if trigger_str == "None":
        return {}

    trigger_list = trigger_str.split("\n")
    return trigger_list

def mini_format_conditionals(conditional_str):

    if conditional_str == "None":
        return {}

    conditional_list = conditional_str.split("\n")
    conditional_dict = {}
    
    for i in range(0, len(conditional_list), 2):
        if conditional_list[i + 1] == "T":
            conditional_dict[conditional_list[i]] = True
        elif conditional_list[i + 1] == "F":
            conditional_dict[conditional_list[i]] = False
    
    return conditional_dict

def main():
    
    # if this is called, then it means that this file is being executed after player_startup
    # and thus all the appropriate directories are in place
    # and the selected game assets have been unzipped to TEMP

    # set cwd to TEMP
    udir.set_cwd_to_self()
    os.chdir("TEMP")

    # flag instance generation

    ref_flags_main = {}

    for flag_name in os.listdir("FLAGS"):
        textfile_contents_base = udir.get_textfile_contents(f"FLAGS/{flag_name}")
        textfile_contents_formatted = base_formatter(textfile_contents_base)
        # note that flag_name should have its last 4 characters (".txt") removed when used from here on out
        flag_args = gen_flag_instance_arguments(flag_name[:-4], textfile_contents_formatted)
        # print(flag_args)
        ref_flags_main[flag_name[:-4]] = Flag(*flag_args)

    # scenario instance generation

    ref_scenarios_main = {}

    for scenario_name in os.listdir("SCENARIOS"):
        textfile_contents_base = udir.get_textfile_contents(f"SCENARIOS/{scenario_name}")
        textfile_contents_formatted = base_formatter(textfile_contents_base)
        # note that scenario_name should have its last 4 characters (".txt") removed when used from here on out
        scenario_args = gen_scenario_instance_arguments(scenario_name[:-4], textfile_contents_formatted)
        # print(scenario_args)
        ref_scenarios_main[scenario_name[:-4]] = Scenario(*scenario_args)

    # play game!

    ref_scenarios_main["__START__"].play()

def direct_execute_error():

    print("")
    print("This file is not to be executed directly.")
    print("Run main.py instead.")

if __name__ == "__main__":
    direct_execute_error()