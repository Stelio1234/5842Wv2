#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
left_motor_b = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 219.44, 295, 40, MM, 5)
inertial_19 = Inertial(Ports.PORT19)
controller_1 = Controller(PRIMARY)
# AI Vision Color Descriptions
# AI Vision Code Descriptions
ai_vision_21 = AiVision(Ports.PORT21, AiVision.ALL_TAGS)
range_finder_g = Sonar(brain.three_wire_port.g)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

batery_level = brain.battery.capacity()

disabled = False


while disabled == True :
    remote_control_code_enabled = True


if batery_level < 20:
    controller_1.rumble("..-----")

if batery_level < 10:
    controller_1.rumble("...----")


def closest90(angle):
    return round(angle / 90) * 90


def turnTo(tagetangle):
    while True:
        currentAngle = inertial_19.rotation(DEGREES)
        notangle = tagetangle - currentAngle
        controller_1.screen.clear_line(1)
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print("Angle: " + str(round(currentAngle, 1)))

        if notangle > 180:
            notangle -= 360
        elif notangle < -180:
            notangle += 360
    
        if abs(notangle) <= 1:
            break

        speed = notangle * 0.5

        if speed > 50:
            speed = 50
        elif speed < -50:
            speed = -50

        left_drive_smart.spin(FORWARD, speed, PERCENT)
        right_drive_smart.spin(REVERSE, speed, PERCENT)

        wait(20, MSEC)

    left_drive_smart.stop()
    right_drive_smart.stop()


def AutoAlign():
    current = inertial_19.rotation(DEGREES)
    target = closest90(current)
    turnTo(target)

#Buttons
def SetingsButton():
    brain.screen.set_cursor(3, 5)
    brain.screen.set_fill_color(Color.WHITE)
    brain.screen.set_font(FontType.MONO12)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(1, 1, 100, 60)
    brain.screen.print("Settings")

def AutoSelectorButton():
    brain.screen.set_font(FontType.MONO12)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(1, 178, 100, 60)
    brain.screen.set_cursor(18,3)
    brain.screen.print("Auto Selector")
    
def MainMenuButton():
    brain.screen.set_font(FontType.MONO12)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.RED)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(1, 178, 100, 60)
    brain.screen.set_cursor(18,3)
    brain.screen.print("Main Menu")

def RedSideButton():
    brain.screen.set_font(FontType.MONO20)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.RED)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(120, 150, 100, 60)
    brain.screen.set_cursor(10,16)
    brain.screen.print("Red")

def BlueSideButton():
    brain.screen.set_font(FontType.MONO20)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(120, 90, 100, 60)
    brain.screen.set_cursor(6,16)
    brain.screen.print("Blue")

def SampleAuto():
    brain.screen.set_font(FontType.MONO20)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(120, 90, 100, 60)
    brain.screen.set_cursor(6,16)
    brain.screen.print("Sample Auto\n This Auto is not color Specific")

def explode():
    brain.screen.clear_screen(Color.BLACK)
    brain.screen.set_cursor(8,8)
    brain.screen.print("THIS ROBOT WILL EXPLODE")
    explodee = 1
    if explodee == 1:
        while True:
            drivetrain.drive(FORWARD)
            drivetrain.drive(REVERSE)
            drivetrain.drive(FORWARD)
            drivetrain.drive(REVERSE)
            drivetrain.drive(FORWARD)
            drivetrain.drive(REVERSE)
            

def CalibrateInternal():
    pass

def getrange():
    range_finder_g.found_object() 
    
    while True:
        distance = range_finder_g.distance(INCHES)
        brain.screen.clear_line(6) 
        brain.screen.set_cursor(6, 7)
        brain.screen.print(str(round(distance)))
        wait(60, MSEC)

#Autos
def Auto1():
    drivetrain.drive_for(FORWARD, 200, MM)
#Menus

#Custom GUI's
Gui = "MainMenu"
LastGui = ""

while True:

    if Gui != LastGui:
        brain.screen.clear_screen()
        controller_1.screen.clear_row(1)
       #Gui Menues
        if Gui == "MainMenu":
            disabled = False
            controller_1.buttonA.pressed(AutoAlign)
            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Enabled")
            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(1 ,15)
            brain.screen.print("Main Menu")
            AutoSelectorButton()
            SetingsButton()

        elif Gui == "SettingsMenu":
            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")
            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_cursor(1 ,15)
            brain.screen.print("Settings")
            MainMenuButton()

        elif Gui == "AutoSelector":
            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")
            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_cursor(1 ,1)
            brain.screen.print("Auto Selector")
            MainMenuButton()
            BlueSideButton()
            RedSideButton()


        LastGui = Gui

    if brain.screen.pressing():
        x = brain.screen.x_position()
        y = brain.screen.y_position()

        if Gui == "MainMenu":
            #Sets the Gui based of where the scrren was clicked
            if 1 <= x <= 121 and 1 <= y <= 61:
                Gui = "SettingsMenu"

            elif 1 <= x <= 100 and 178 <= y <= 278:
                Gui = "AutoSelector"
        else:
            if 1 <= x <= 100 and 178 <= y <= 278:
                Gui = "MainMenu"

        #Detects the button Press for the AutoSelector
        if Gui == "AutoSelector":
            pass
        wait(150, MSEC)
    wait(10, MSEC)
    
   
controller_1.buttonA.pressed(AutoAlign)

#Game Stuff
def pre_autonomous():
    controller_1.buttonA.pressed(AutoAlign)
pre_autonomous()

def autonmous():
    pass

autonmous()
 
def driver_control(): 

   

    controller_1.buttonA.pressed(AutoAlign)

driver_control()

