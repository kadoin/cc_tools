import cc_dat_utils
import cc_data
import json


def makeDatFromJson(inputJson, outputDat):
    with open(inputJson) as dataFile:
        jason = json.load(dataFile)
    levels = cc_data.CCDataFile()
    for i in jason:
        newLevel = cc_data.CCLevel(i["level number"], i["time"], i["chip number"],
                                   i["upper layer"], i["lower layer"])
        #print(i["optional fields"])
        cats = []
        traps = []
        clones = []
        monsters = []

        count = 0
        for j in i["optional fields"]:
            count += 1
            #print(count)
            if j["type"] == 3:

                title = cc_data.CCMapTitleField(j["title"])
               # print(title)
                newLevel.add_field(title)
                print("added title")



            elif j["type"] == 4:
                bx = j["trap coords"][0]
                by = j["trap coords"][1]
                tx = j["trap coords"][2]
                ty = j["trap coords"][3]
                traps.append(cc_data.CCTrapControl(bx,by,tx,ty))
            elif j["type"] == 5:
                bx = j["clone coords"][0]
                by = j["clone coords"][1]
                tx = j["clone coords"][2]
                ty = j["clone coords"][3]
                clones.append(cc_data.CCCloningMachineControl(bx, by, tx, ty))
            elif j["type"] == 6:

                newLevel.add_field(cc_data.CCEncodedPasswordField(j["password"]))

            elif j["type"] == 7:

                newLevel.add_field(cc_data.CCMapHintField(j["hint"]))

            elif j["type"] == 10:
                coords = j["monster coords"]
                monsters.append(cc_data.CCCoordinate(coords[0],coords[1]))


            newLevel.add_field(cc_data.CCMonsterMovementField(monsters))
            newLevel.add_field(cc_data.CCTrapControlsField(traps))
            newLevel.add_field(cc_data.CCCloningMachineControlsField(clones))


        #print(newLevel)

        levels.add_level(newLevel)
        newLevel.optional_field = []
        print(newLevel.optional_field)
        print("********************")
    cc_dat_utils.write_cc_data_to_dat(levels,outputDat)
    #print(levels)


makeDatFromJson("ccjason.json", "rattadat.dat")