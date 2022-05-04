import PicoBorgRev3 as PicoBorgRev
PBR = PicoBorgRev.PicoBorgRev()
PBR.Init()
PBR.ResetEpo()



import keyboard  # using module keyboard
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'q' is pressed 
            print('You Pressed W Key!')
            PBR.SetMotors(100)
            break  # finishing the loop
        if keyboard.is_pressed('s'):  # if key 'q' is pressed 
            print('You Pressed W Key!')
            PBR.SetMotors(-100)
            break  # finishing the loop
        if keyboard.is_pressed('x'):  # if key 'q' is pressed 
            print('You Pressed W Key!')
            PBR.MotorOff()
            break  # finishing the loop
    except:
        PBR.MotorOff()
        break 