#!/usr/bin/env python
# coding: Latin-1
  
# Load library functions we want
import time
import pygame
import os
import PicoBorgRev3 as PicoBorgRev
import tkinter
  
# Settings for the PicoBorg Reverse keyboard movement
interval = 0.01                         # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
 
# Power settings
voltageIn = 12.0                        # Total battery voltage to the PicoBorg Reverse
voltageOut = 6.0                        # Maximum motor voltage
 
# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)
 
# Setup the PicoBorg Reverse
PBR = PicoBorgRev.PicoBorgRev()
#PBR.i2cAddress = 0x44                  # Uncomment and change the value if you have changed the board address
PBR.Init()
if not PBR.foundChip:
    boards = PicoBorgRev.ScanForPicoBorgReverse()
    if len(boards) == 0:
        print ('No PicoBorg Reverse found, check you are attached :)')
    else:
        print ('No PicoBorg Reverse at address %02X, but we did find boards:' % (PBR.i2cAddress))
        for board in boards:
            print ('    %02X (%d)' % (board, board))
        print ('If you need to change the I²C address change the setup line so it is correct, e.g.')
        print ('PBR.i2cAddress = 0x%02X' % (boards[0]))
    sys.exit()
#PBR.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
# Ensure the communications failsafe has been enabled!
PBR.ResetEpo()
 
# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRighte
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
pygame.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("RemoteKeyBorg - Press [ESC] to quit")
  
# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                moveUp = True
            elif event.key == pygame.K_DOWN:
                moveDown = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                moveUp = False
            elif event.key == pygame.K_DOWN:
                moveDown = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_ESCAPE:
                moveQuit = False
  
try:
    print ('Press [ESC] to quit')
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, change the motor outputs
            hadEvent = False
            if moveQuit:
                break
            elif moveLeft:
                PBR.SetMotor1(-maxPower)
                PBR.SetMotor2(+maxPower)
            elif moveRight:
                PBR.SetMotor1(+maxPower)
                PBR.SetMotor2(-maxPower)
            elif moveUp:
                PBR.SetMotor1(+maxPower)
                PBR.SetMotor2(+maxPower)
            elif moveDown:
                PBR.SetMotor1(-maxPower)
                PBR.SetMotor2(-maxPower)
            else:
                # None of our expected keys, stop
                PBR.MotorsOff()
        # Wait for the interval period
        time.sleep(interval)
    # Inform the server to stop
    PBR.MotorsOff()
except KeyboardInterrupt:
    # CTRL+C exit, inform the server to stop
    PBR.MotorsOff()