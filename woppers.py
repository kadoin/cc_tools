from cc_data import *
from cc_dat_utils import *
import sys
import json

def make_data_file_from_json(data):
    smsyjuco_ccl = CCDataFile() #use this json to make our level
    for level_data in data: #look at all the level data

        level = CCLevel()
        level.level_number = level_data["level number"]
        level.time = level_data["time"]
        level.num_chips = level_data["chip number"]
        level.upper_layer = level_data["upper layer"]
        level.lower_layer = level_data["lower layer"]
        fields = level_data["optional fields"]

        title_field = CCMapTitleField(fields[2])
        #print(fields[2])
        print(title_field)
        print(type(title_field))
        print("cats")
        level.add_field(title_field)

        #how to put in traps
        brown_button_traps = []# an array to store the traps
        for trap in fields[3]:# for every trap in the json file
            button_coord = trap["BrownButtonCoord"]# get the button coords
            trap_coord = trap["TrapCoord"]# get the trap coords
            #create a button trap with all of those coords
            button_trap = CCTrapControl(button_coord["x"], button_coord["y"],
                                        trap_coord["x"], trap_coord["y"])
            #put that into the end of the button trap array
            brown_button_traps.append(button_trap)
        #add the button trap field
        level.add_field(CCTrapControlsField(brown_button_traps))

        #how to add red button traps in
        red_button_traps = []#create an array to store them in
        for trap in fields[4]:
            #get the coordinates you need to set the trap
            button_coord = trap["RedButtonCoord"]
            trap_coord = trap["CloningCoord"]
            cloning_trap = CCCloningMachineControl(button_coord["x"], button_coord["y"],
                                                trap_coord["x"], trap_coord["y"])
            #put the tray into the array
            red_button_traps.append(cloning_trap)
        level.add_field(CCCloningMachineControlsField(red_button_traps))#add the field

        #put in the encoded password from the json file
        encoded_password = CCEncodedPasswordField(fields[5])
        level.add_field(encoded_password)

        #put in the hint text from the json file
        hint_text = CCMapHintField(fields[6])
        level.add_field(hint_text)

        #creating monsters
        moving_objects = []
        for moving_object in fields[9]:
            #Get the coords the monsters should be at and add them to the array and level
            monster_coord = CCCoordinate(moving_object["x"],
                                         moving_object["y"])
            moving_objects.append(monster_coord)
        level.add_field(CCMonsterMovementField(moving_objects))

        #add all the information
        smsyjuco_ccl.add_level(level)
    return smsyjuco_ccl


default_input_json_file = "ccjason.json" # the json file we are accessing

if len(sys.argv) == 2:
    input_json_file = sys.argv[0]
    output_json_file = sys.argv[1]
    print("Using command line args:", input_json_file)
else:
    print("Unknown command line options. Using default values:", default_input_json_file)
    input_json_file = default_input_json_file
    output_json_file = "./smsyjuco_ccl.dat"

#loading the json file and saving it into dat
json_data = open(input_json_file)
d = json.load(json_data)
game_data_file = make_data_file_from_json(d)
print(game_data_file)
write_cc_data_to_dat(game_data_file, output_json_file)
