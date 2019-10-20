#    Copyright 2019, iGEM Marburg 2019
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# coding: utf-8

# # Plasmid Purification Protocol - Single Pipette

# ### Loading Python modules

# In[1]:


from opentrons import robot, labware, instruments, modules
import serial
import time
import json


# ### Loading custom functions

# In[2]:


#Custom mix function compatible with shaker defined as coordinates
def custom_mix(times, volume, coord):
    p300.move_to(coord, strategy = 'arc')
    for i in range(0,times):
        p300.aspirate(volume)
        p300.dispense(volume ,coord)


# In[3]:


#Custom transfer function without pick_up_tip() and drop_tip()
def custom_transfer(volume, source, destination):
    p300.move_to(source)
    p300.aspirate(volume)
    p300.dispense(volume, destination)


# ### Defining metadata

# In[4]:


metadata = {
    'protocolName': 'Promega Wizard MagneSil Plasmid Purification Protocol',
    'author': 'iGEM Marburg 2019',
    'description': 'Script for performing plasmid purification for a small number of samples (1-6)',
}


# In[5]:


amount = 3


# ### Loading shaker module coordinates from json file

# In[6]:


### DEPRECATED, WAIT FOR PRINT TO FINISH OR MAKE CUSTOM LABWARE ###
with open("CoordinatesOrdered.json", "r") as infile:
    coordinates = json.loads(infile.read())

#Correcting Offset (can change after renewed calibration)
for x in ["A","B","C","D","E","F","G","H"]:
    for y in [str(x) for x in range(1,13)]:
        coordinates["%s%s"%(x,y)]["x"] += 6
        coordinates["%s%s"%(x,y)]["y"] -= 8
        coordinates["%s%s"%(x,y)]["z"] += 25 #75 
        


# ### Connecting robot and modules

# In[7]:


robot.connect()
robot.discover_modules()


# ### Custom function to get ordered jason

# In[8]:


#Pass the json above as an argument and return it as an ordered list 
def order_json(unord_json):
    coords = []
    for i in sorted(unord_json, key=lambda x: (int(x[1:]), x[0])):
        coords.append(unord_json[i])
    return coords


# In[9]:


# Input: well_start: Integer where to start on the labware
#        well_end: Integer where to stop on the labware
#        coords_json: Pass the ordered json from order_json return
# Output: returns (x, y, z) coordinates as a list of tuples from well_start to well_end

def well_coords(well_start:int, well_end:int, coords_json):
    if (well_start<0) or (well_end > 96) or (well_start>=well_end):
        return None
    
    well_list = []
    for i in range(well_start, well_end):
        well_list.append((coords_json[i]['x'], coords_json[i]['y'], coords_json[i]['z']))
    
    return well_list


# In[10]:


coordinates = order_json(coordinates)


# ### Defining labware

# In[11]:


tip_rack = labware.load('opentrons_96_tiprack_300ul','8')
tip_rack2 = labware.load('opentrons_96_tiprack_300ul','9')
liquid = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '7')
plate_shake = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '3')
magdeck = modules.load('magdeck', 10)
plate_mag = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '10', share = True)
final_plate = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '11')
p300 = instruments.P300_Single(
    mount = 'left', 
    tip_racks = [tip_rack, tip_rack2],
    aspirate_flow_rate = 75)


# ### Shaker command list

# In[15]:


#########################Activate Shaker Module#######################
import serial
import time


######################### Working code ################################
#with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:

#    #ELM closes, ready for shaking 
#     ser.write(b'setElmLockPos\r')

#    #Set the mixing speed target of 2,000 rpm 
#    ser.write(b'ssts1000\r')

#    #Shaker starts movement with 2,000 rpm 
#    ser.write(b'son\r')

    #Shaker stops in home position and lock in 
#    ser.write(b'soff\r')

    #ELM opens for gripping microplates 
#    ser.write(b'setElmUnlockPos\r')
##################################


# ### Step 1 - Cell Resuspension Solution

# In[16]:


#Put shaker at home
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'soff\r')

#Add Resuspension Solution
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(90, liquid.wells('A1'))
    p300.dispense(90, (plate_shake, coordinates[x]))
    p300.mix(10, 45, (plate_shake, coordinates[x]))
    p300.drop_tip()


# In[17]:


#Shake at 1500 rpm for 2 min to resuspend cell pellet
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'ssts1500\r')
    time.sleep(0.2) 
    ser.write(b'sonwr120\r')
    time.sleep(120)
    ser.write(b'soff\r')


# ### Step 2 - Cell Lysis Solution

# In[18]:


#Add Cell Lysis Solution
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(120, liquid.wells('A2'))
    p300.dispense(120, (plate_shake, coordinates[x]))
    p300.mix(10, 105, (plate_shake, coordinates[x]))
    p300.drop_tip()

#Incubate for 3 minutes
p300.delay(minutes = 3)


# ### Step 3 - Neutralization Buffer

# In[19]:


#Add Neutralization Buffer
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(120, liquid.wells('A3'))
    p300.dispense(120, (plate_shake, coordinates[x]))
    p300.mix(10, 155, (plate_shake, coordinates[x]))
    p300.drop_tip()


# ### Step 4 - MagneSil Blue

# In[20]:


#Add MagneSil Blue
for x in range(0,amount):
    p300.pick_up_tip()
    p300.mix(10, 80, liquid.wells('A4'))
    p300.aspirate(25, liquid.wells('A4'))
    p300.dispense(25, (plate_shake, coordinates[x]))
    p300.mix(10, 155, (plate_shake, coordinates[x]))
    p300.drop_tip()


# In[21]:


#Shake at 1200 rpm for 3 min
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    time.sleep(3) 
    ser.write(b'ssts1200\r')
    time.sleep(0.2) 
    ser.write(b'sonwr180\r')
    time.sleep(60)
    ser.write(b'soff\r')


# ### Step 5 - Transfer to Magnetic Module

# In[22]:


#x+8 everytime we want to change column
#Shake before every transfer step, because otherwise the lysate will clump and clog the tip

for x in range(0,amount):
    #Shake
    with serial.Serial('/dev/ttyUSB0', timeout=1) as ser: 
        ser.write(b'ssts1200\r')
        time.sleep(0.2) 
        ser.write(b'sonwr180\r')
        time.sleep(10)
        ser.write(b'soff\r')
        
    #Transfer from shaker to magnetic module
    p300.pick_up_tip()
    custom_mix(10,170, (plate_shake, coordinates[x]))
    p300.aspirate(170, (plate_shake, coordinates[x]))
    p300.dispense(170, plate_mag.wells(x))
    
    #Do it twice cause the volume is too high for one transfer step
    custom_mix(10,170, (plate_shake, coordinates[x]))
    p300.aspirate(170, (plate_shake, coordinates[x]))
    p300.dispense(170, plate_mag.wells(x))
    
    #Turn on magnetic module
    magdeck.engage(height = 10)
    time.sleep(20)
    
    #Cell trash is now attached to blue beads, transfer supernatant back to shaker
    p300.aspirate(170, plate_mag.wells(x))
    p300.dispense(170, (plate_shake, coordinates[x + 16]))
    
    #Do it twice cause the volume is too high for one transfer step
    p300.aspirate(170, plate_mag.wells(x))
    p300.dispense(170, (plate_shake, coordinates[x + 16]))
    
    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()


# ### Step 6 - MagneSil Red

# In[ ]:


#Add MagneSil Red
for x in range(0, amount):
    p300.pick_up_tip()
    p300.mix(10, 175, liquid.wells('A5'))
    p300.aspirate(50, liquid.wells('A5'))
    p300.dispense(50, (plate_shake, coordinates[x + 16]))
    p300.drop_tip()


# In[ ]:


#Add Isopropanol
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(175, liquid.wells('A6'))
    p300.dispense(175, (plate_shake, coordinates[x + 16]))
    p300.drop_tip()
    p300.pick_up_tip()
    p300.aspirate(175, liquid.wells('A7'))
    p300.dispense(175, (plate_shake, coordinates[x + 16]))
    p300.drop_tip()


# In[ ]:


#Shake at 1200 rpm for 5 min to catch all plasmids
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'ssts1200\r')
    time.sleep(0.2) 
    ser.write(b'sonwr300\r')
    time.sleep(180)
    ser.write(b'soff\r')


# ### Step 7 - Transfer to Magnetic Module

# In[ ]:


#Shake before every transfer step, because otherwise the beads clump and clog the tip

for x in range(0,amount):
    #Shake
    with serial.Serial('/dev/ttyUSB0', timeout=1) as ser: 
        ser.write(b'ssts1200\r')
        time.sleep(0.2) 
        ser.write(b'sonwr180\r')
        time.sleep(10)
        ser.write(b'soff\r')
        
    #Transfer back to magnetic module 
    p300.pick_up_tip()    
    custom_mix(10,175,(plate_shake, coordinates[x + 16]))
    custom_transfer(280, (plate_shake, coordinates[x + 16]), plate_mag.wells(x + 8))
    custom_transfer(280, (plate_shake, coordinates[x + 16]), plate_mag.wells(x + 8))
    custom_transfer(280, (plate_shake, coordinates[x + 16]), plate_mag.wells(x + 8))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
    
    # Discard supernatant, plasmids are attached to Red Beads -> Trash to first column of plate on the shaker
    p300.aspirate(250, plate_mag.wells(x + 8))
    p300.dispense(250, (plate_shake, coordinates[x]))
    p300.aspirate(250, plate_mag.wells(x + 8))
    p300.dispense(250, (plate_shake, coordinates[x]))
    p300.aspirate(250, plate_mag.wells(x + 8))
    p300.dispense(250, (plate_shake, coordinates[x]))
    magdeck.disengage()
    p300.drop_tip()


# ### Step 8 - Washing Solution

# In[ ]:


#Add Washing Solution
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(240, liquid.wells('A8'))
    p300.dispense(240, plate_mag.wells(x + 8))
    p300.mix(3,120, plate_mag.wells(x + 8))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
    
    #Discard supernatant -> Trash to first column of plate on the shaker
    p300.aspirate(200, plate_mag.wells(x + 8))
    p300.dispense(200, (plate_shake, coordinates[x]))
    magdeck.disengage()
    p300.drop_tip()


# ### Step 9 - Ethanol

# In[ ]:


#Add Ethanol
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(250, liquid.wells('A9'))
    p300.dispense(250, plate_mag.wells(x + 8))
    p300.mix(3,120, plate_mag.wells(x + 8))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
    
    #Discard supernatant, need to test
    p300.aspirate(250, plate_mag.wells(x + 8))
    p300.dispense(250, (plate_shake, coordinates[x + 16]))
    magdeck.disengage()
    p300.drop_tip()


# ### Step 10 - Ethanol Second Time

# In[ ]:


#Add Ethanol
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(250, liquid.wells('A10'))
    p300.dispense(250, plate_mag.wells(x + 8))
    p300.mix(3,120, plate_mag.wells(x + 8))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
    
    #Discard supernatant
    p300.aspirate(170, plate_mag.wells(x + 8))
    p300.dispense(170, (plate_shake, coordinates[x + 16]))
    p300.aspirate(170, plate_mag.wells(x + 8))
    p300.dispense(170, (plate_shake, coordinates[x + 16]))
    magdeck.disengage()
    p300.drop_tip()
    
p300.delay(minutes = 5)


# ### Step 11 - Nuclease Free Water

# In[ ]:


#Add Nuclease Free Water to elute the plasmid
for x in range(0,amount):
    p300.pick_up_tip()
    p300.aspirate(100, liquid.wells('A11'))
    p300.dispense(100, plate_mag.wells(x + 8))
    p300.mix(10,75, plate_mag.wells(x + 8))
    p300.delay(seconds = 10)
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
    
    #Now DNA is in Nuclease Free Water, pipette to final 96 Well Plate
    p300.aspirate(100, plate_mag.wells(x + 8))
    p300.dispense(100, final_plate.wells(x))
    
    magdeck.disengage()
    p300.drop_tip()

