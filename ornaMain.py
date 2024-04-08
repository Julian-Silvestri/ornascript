#CRITICAL COMMANDS
# adb exec-out uiautomator dump /dev/tty     -> outputs the current xml into the terminal
# adb exec-out uiautomator dump              -> outputs the current xml into a file
#
import time
from pprint import pprint
from ppadb.client import Client
from xml.dom import minidom
import uiautomator2 as u2

last_enemy_fought = "ice_troll"
current_pet = "living_armor"
items_x, items_y = 714 , 2082
continue_x , continue_y = 426, 2067
auto_heal_x, auto_heal_y = 654, 1962
major_spell_x , major_spell_y = 264,1713
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()
current_keys_from_xml = {}

if len(devices) == 0:
    print("No devices")
    # quit()

device = devices[0]

def grabXml():
    global current_keys_from_xml

    my_phone = u2.connect()
    # print(my_phone.dump_hierarchy())
    saveXmlFile("please_work", my_phone.dump_hierarchy())
    time.sleep(1)
    dom = minidom.parse('please_work.xml')
    elements = dom.getElementsByTagName('node')

    for element in elements:
        text_key = element.attributes['text'].value
        if text_key != "":
            partitioned_string =  element.attributes['bounds'].value
            head, sep, tail = partitioned_string.partition("]")
            head = head.replace("[" , "")
            head = head.replace("," , " ") # space to separate on
            current_keys_from_xml[text_key] = head
            # print(element.attributes['text'].value, head)
    print("Data grab ---- complete")
    # print("THIS IS THE DICT => ")
    # pprint(current_keys_from_xml)


def tapOnEnemy():
    print("tapping on enemy func")
    global current_keys_from_xml , last_enemy_fought
    enemy_dict = {}
    current_keys_from_xml = {}
    grabXml()
    time.sleep(1)
    # print("current_keys_from_xml" , current_keys_from_xml)
    with open("orna_enemy_keys.txt") as file:
        for enemy_key in file:
            for key, value in current_keys_from_xml.items():
                x_coord, y_coord = value.split(" ")
                if enemy_key.rstrip() == key:
                    x_coord = str(x_coord)
                    y_coord = float(y_coord)
                    if (y_coord > 1890):
                        print("too low on screen")
                        # print("ENEMY => ", enemy_key,"y position => ", y_coord)
                        continue
                    else:
                        if(last_enemy_fought == enemy_key):
                            print("Already Fought this enemy ====> ", enemy_key)
                            continue
                        else:
                            print("FOUND ENEMY => ", enemy_key, "x position => ", x_coord, "y position => ", y_coord)
                            enemy_dict[enemy_key] = x_coord, y_coord
                            last_enemy_fought = enemy_key
                            performTap(x_coord, y_coord)
                            grabXml()
                            time.sleep(1)
                            tapBattleToStart()
                            return




def tapBattleToStart():
    global current_keys_from_xml
    print("TAPPIGN BATTLE TO START")
    battle_x_coord = ""
    battle_y_coord = ""
    grabXml()
    time.sleep(1)
    for key, value in current_keys_from_xml.items():
        if(key == "BATTLE"):
            print("FOUND BATTLE !")
            battle_x_coord, battle_y_coord = value.split(" ")
            break

    performTap(battle_x_coord, battle_y_coord)
    grabXml()
    time.sleep(1)
    attackMonster()


def attackMonster():
    global current_keys_from_xml
    print("ATTACKING MONSTERS")

    while(True):
        performTap(major_spell_x, major_spell_y) # pretty sure these coordinates will NEVER change as this is the first big spell button
        grabXml()
        time.sleep(2)
        for key, value in current_keys_from_xml.items():
            if key == "CONTINUE":
                print("FIGHT IS OVER")
                performTap(continue_x,continue_y)  # pretty sure these coordinates will NEVER change as this is continue button
                time.sleep(1)
                autoHealCharacter()
                break
            else:
                continue


def autoHealCharacter():
    global current_keys_from_xml
    performTap(items_x, items_y)
    x_coord , y_coord = "" , ""
    print("AUTO HEALING CHARACTER")
    grabXml()
    time.sleep(2)
    for key , values in current_keys_from_xml.items():
        if key == 'Auto-heal':
            print("FOUND AUTO-HEAL")
            x_coord, y_coord = values.split(" ")
            break

    performTap(x_coord, y_coord)
    time.sleep(1)
    performTap(530, 2100)
    time.sleep(1)
    tapOnEnemy()


def saveXmlFile(fileName, data):

    f = open(f"{fileName}.xml", "w", encoding='utf-8')
    f.write(data)
    f.close()
    time.sleep(1)
    return

def performTap(x,y):
    device.shell(f'input touchscreen tap {x} {y}')
    return



tapOnEnemy()


# def hasColor(row, rgb):
#     pixels = [list(i[:3]) for i in row]
#     for pixel in pixels:
#         if pixel[0] == rgb[0] and pixel[1] == rgb[1] and pixel[2] == rgb[2]:
#             return True
#     return False

# image = device.screencap()
#
# with open('screen.png', 'wb') as f:
#     f.write(image)

# image = Image.open('screen.png')
# image2 = Image.open('screen.png')
# image = numpy.array(image, dtype=numpy.uint)
# # print(image2)
#
# pixels = [list(i[:3]) for i in image[2100]]
# # pprint(pixels)
#
#
# def startFishing():
#     # 44, 95, 135# blue pond
#     # 79 ,110, 80 #continue color button
#     while(True):
#
#         #cast if there is no fishing line
#         if hasColor(image[1300],(234, 255, 0)): #fishing line - great line ? not sure which one - > its yellow
#             device.shell('input touchscreen tap 500 1200')
#             print('found good line')
#
#         elif hasColor(image[1300],(159, 166, 189)): #basic line
#             device.shell('input touchscreen tap 500 1200')
#             print('found basic line')
#
#         elif hasColor(image[1300], (140, 70, 195)):  # unknown line pink line
#             device.shell('input touchscreen tap 500 1200')
#             print('found basic line')
#             break
#         else:
#             print('starting cast')
#             device.shell('input touchscreen tap 500 1200')
#             time.sleep(1)
#             device.shell('input touchscreen tap 500 1200')
#             break


# startFishing()