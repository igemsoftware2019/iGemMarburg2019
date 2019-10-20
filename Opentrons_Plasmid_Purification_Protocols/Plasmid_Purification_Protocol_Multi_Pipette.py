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

# # Plasmid Purification Protocol - Multi Pipette

# ### Loading Imports

# In[1]:


from opentrons import robot, labware, instruments, modules
import serial
import time
import json


# ### Running Variables

# In[ ]:


amt_cols = 2 #How many columns you want to purify? (2*8=16)


# ### Metadata

# In[ ]:


metadata = {
    'protocolName': 'Plasmid Purification (Multi_Channel)',
    'author': 'iGEM Marburg 2019',
    'description': 'Promega Wizard MagneSil Plasmid Purification Protocol'
}


# ### Labware

# In[ ]:


tip_rack = labware.load('opentrons_96_tiprack_300ul','8')
tip_rack2 = labware.load('opentrons_96_tiprack_300ul','9')
liquid = labware.load('usascientific_12_reservoir_22ml', slot = '7')
plate_shake = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '3')
magdeck = modules.load('magdeck', 10)
plate_mag = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '10', share = True)
final_plate = labware.load('usascientific_96_wellplate_2.4ml_deep', slot = '11')


# ### Liquids

# In[ ]:


resuspension = liquid.wells(0)
lysis = liquid.wells(1)
neutralization = liquid.wells(2)
magnesil_blue = liquid.wells(3)
magnesil_red = liquid.wells(4)
isopropanol =  liquid.wells(5)
wash_solution = liquid.wells(6)
ethanol = [liquid.wells(7), liquid.wells(8)]
water = liquid.wells(9)


# ### Pipette

# In[ ]:


p300 = instruments.P300_Multi(
    mount = 'left', 
    tip_racks = [tip_rack, tip_rack2],
    aspirate_flow_rate = 75)


#  

# ### Custom Functions

# In[ ]:


def mischen(times, volume, coord):
    p300.move_to(coord, strategy = 'arc')
    for i in range(0,times):
        p300.aspirate(volume)
        p300.dispense(volume ,coord)
        

def custom_transfer(volume, source, destination):
    p300.move_to(source)
    p300.aspirate(volume)
    p300.dispense(volume, destination)


# ### Load Custom Labware

# In[ ]:


with open("coordinates.json", "r") as infile:
    coordinates = json.loads(infile.read())

# Correcting Offset 
for x in ["A","B","C","D","E","F","G","H"]:
    for y in [str(x) for x in range(1,13)]:
        coordinates["%s%s"%(x,y)]["x"] += 6
        coordinates["%s%s"%(x,y)]["y"] -= 8
        coordinates["%s%s"%(x,y)]["z"] += 25 
        
col_cord = []
counter = 0
for i in coordinates.items():
    if counter%8 == 0:
        col_cord.append((i[1]['x'], i[1]['y'], i[1]['z']))
    counter += 1


# ### Connecting

# In[ ]:


robot.connect()
robot.discover_modules()


# ### Step 1 - Cell Resuspension Solution

# In[ ]:


#Put shaker at home
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'soff\r')

#Add Resuspension Solution
for i in range(amt_cols):
    p300.pick_up_tip()
    p300.aspirate(90, resuspsension)
    p300.dispense(90, (plate_shake, col_cord[i]))
    p300.mix(10, 45, (plate_shake, col_cord[i]))
    p300.drop_tip()


# In[ ]:


#Shake at 1500 rpm for 2 min
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'ssts1500\r')
    time.sleep(0.2) 
    ser.write(b'sonwr120\r')
    time.sleep(120)
    #ser.write(b'sgh\r')
    ser.write(b'soff\r')


# ### Step 2 - Cell Lysis Solution

# In[ ]:


#Put shaker at home
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'soff\r')
    
#Add Resuspension Solution
for i in range(amt_cols):
    p300.pick_up_tip()
    p300.aspirate(120, lysis)
    p300.dispense(120, (plate_shake, col_cord[i]))
    p300.mix(10, 105, (plate_shake, cold_cord[i]))
    p300.drop_tip()

#In protocol it is written incubate 3 minutes, but since giving neutralization solution takes time, only do one minute to catch up    
p300.delay(minutes = 3)


# ### Step 3 - Neutralization Buffer

# In[ ]:


#Put shaker at home
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'soff\r')
    
#Add Neutralization Buffer
for i in range(amt_cols):
    p300.pick_up_tip()
    p300.aspirate(120, neutralization)
    p300.dispense(120, (plate_shake, col_cord[i]))
    p300.mix(10, 155, (plate_shake, col_cord[i]))
    p300.drop_tip()


# ### Step 4 - MagneSil Blue

# In[ ]:


#Put shaker at home
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'soff\r')
    
#Add MagneSil Blue
for i in range(amt_cols):
    p300.pick_up_tip()
    p300.mix(10, 80, magnesil_blue)
    p300.aspirate(30, magnesil_blue)
    p300.dispense(30, (plate_shake, col_cord[i]))
    p300.mix(10, 155, (plate_shake, col_cord[i]))
    p300.drop_tip()


# In[ ]:


#Shake at 1200 rpm for 3 min
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    time.sleep(3) 
    ser.write(b'ssts1200\r')
    time.sleep(0.2) 
    ser.write(b'sonwr180\r')
    time.sleep(60)
    ser.write(b'soff\r')


# ### Step 5 - Transfer to Magnetic Module

# In[ ]:


#Shake before every transfer step, because otherwise the lysate will clump and clog the tip

for i in range(amt_cols):
    #Shake
    with serial.Serial('/dev/ttyUSB0', timeout=1) as ser: 
        ser.write(b'ssts1200\r')
        time.sleep(0.2) 
        ser.write(b'sonwr180\r')
        time.sleep(10)
        ser.write(b'soff\r')
        
    p300.pick_up_tip()
    
    #Transfer from shaker to magnetic module
    p300.transfer(
        340,
        (plate_shake, col_cord[i]),
        plage_mag.cols(i),
        mix_before = (10, 170),
        carryover = True,
        new_tip = 'never' 
    )

    #Turn on magnetic module
    magdeck.engage(height = 20)
    time.sleep(20)

    #Cell trash is now attached to blue beads, transfer supernatant back to shaker
    p300.transfer(
        340,
        plate_mag.cols(i),
        (plate_shake, col_cord[i+amt_cols]),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()


# ### Step 6 - MagneSil Red

# In[ ]:


#Add MagneSil Red
for i in range(amt_cols):
    p300.transfer(
        50,
        magnesil_red,
        (plate_shake, col_cord[i+amt_cols]),
        mix_before = (10, 175)
    )


# In[ ]:


#Add Isopropanol
for i in range(amt_cols):
    p300.transfer(
        350,
        isopropanol,
        (plate_shake, col_cord[i+amt_cols]),
        new_tip = 'once',
        carryover = True
    )


# In[ ]:


#Shake at 1200 rpm for 5 min to catch all plasmids
with serial.Serial('/dev/ttyUSB0', timeout=1) as ser:
    ser.write(b'ssts1200\r')
    time.sleep(0.2) 
    ser.write(b'sonwr300\r')
    time.sleep(180)
    ser.write(b'soff\r')


# ### Step 7 - Transfer to Magnetic Module (Anso)

# In[ ]:


#Shake before every transfer step, because otherwise the beads clump and clog the tip

for i in range(amt_cols):
    #Shake
    with serial.Serial('/dev/ttyUSB0', timeout=1) as ser: 
        ser.write(b'ssts1200\r')
        time.sleep(0.2) 
        ser.write(b'sonwr180\r')
        time.sleep(10)
        ser.write(b'soff\r')
        
    #Transfer back to magnetic module 
    p300.pick_up_tip()    
    
    custom_mix(10,175,(plate_shake, col_cord[i+amt_cols]))
    
    #Transfer from shaker to magnetic module
    p300.transfer(
        840,
        (plate_shake, col_cord[i+amt_cols]),
        plage_mag.cols(i+amt_cols),
        mix_before = (10, 170),
        carryover = True,
        new_tip = 'never' 
    )
    
    #Turn on magnetic module
    magdeck.engage(height = 10)
    time.sleep(20)

    #Discard supernatant
    p300.transfer(
        840,
        plate_mag.cols(i+amt_cols),
        (plate_shake, col_cord[i]),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()


# ### Step 8 - Washing Solution

# In[ ]:


#Add Washing Solution
for i in range(amt_cols):
    
    p300.pick_up_tip()
    
    p300.transfer(
        240,
        wash_solution,
        plate_mag.cols(i+amt_cols),
        carryover = True,
        new_tip = 'never',
    )
    
    p300.mix(3,120, plate_mag.cols(i+amt_cols))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
     
    #Discard supernatant
    p300.transfer(
        200,
        plate_mag.cols(i+amt_cols),
        (plate_shake, col_cord[i+amt_cols]),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()


# ### Step 9 - Ethanol

# In[ ]:


#Add Ethanol
for i in range(amt_cols):
    
    p300.pick_up_tip()
    
    p300.transfer(
        250,
        ethanol[1],
        plate_mag.cols(i+amt_cols),
        carryover = True,
        new_tip = 'never',
    )
    
    p300.mix(3,120, plate_mag.cols(i+amt_cols))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
     
    #Discard supernatant
    p300.transfer(
        250,
        plate_mag.cols(i+amt_cols),
        (plate_shake, col_cord[i+amt_cols]),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()


# ### Step 10 - Ethanol

# In[ ]:


#Add Ethanol
for i in range(amt_cols):
    
    p300.pick_up_tip()
    
    p300.transfer(
        250,
        ethanol[2],
        plate_mag.cols(i+amt_cols),
        carryover = True,
        new_tip = 'never',
    )
    
    p300.mix(3,120, plate_mag.cols(i+amt_cols))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
     
    #Discard supernatant
    p300.transfer(
        340,
        plate_mag.cols(i+amt_cols),
        (plate_shake, col_cord[i+amt_cols]),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()

p300.delay(minutes = 5)


# ### Step 11 - Nuclease Free Water

# In[ ]:


#Add Nuclease Free Water to elute the plasmid
for i in range(amt_cols):
    
    p300.pick_up_tip()
    
    p300.transfer(
        100,
        water,
        plate_mag.cols(i+amt_cols),
        carryover = True,
        new_tip = 'never',
    )
    
    p300.mix(10,75, plate_mag.cols(i+amt_cols))
    
    #Turn magnetic module on
    magdeck.engage(height = 10)
    p300.delay(seconds = 10)
     
    #Now DNA is in Nuclease Free Water, pipette to final 96 Well Plate
    p300.transfer(
        100,
        plate_mag.cols(i+amt_cols),
        final_plate.cols(i),
        carryover = True,
        new_tip = 'never',
    )

    #Turn off magnetic module
    magdeck.disengage()
    p300.drop_tip()

