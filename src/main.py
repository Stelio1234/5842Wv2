#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
left_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 219.44, 295, 40, MM, 1.6666666666666667)
Internal_Sensor = Inertial(Ports.PORT1)


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
    controller_1.rumble("...--- -")

# Robot Actions
def closest90(angle):
    return round(angle / 90) * 90


def turnTo(tagetangle):
    while True:
        currentAngle = Internal_Sensor.rotation(DEGREES)
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
    current = Internal_Sensor.rotation(DEGREES)
    target = closest90(current)
    turnTo(target)




#Random Crap

def SampleAuto():
    brain.screen.set_font(FontType.MONO20)
    brain.screen.set_pen_color(Color.BLACK)
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(120, 90, 100, 60)
    brain.screen.set_cursor(6,16)
    brain.screen.print("Sample Auto\n This Auto is not color Specific")


            

def CalibrateInternal():
    pass



#Menus

Gui = "MainMenu"
LastGui = ""

auto_side = "Blue"
auto_mode = "Match"
drive_speed = 100
drive_reverse = False


def button(x, y, w, h, name):

    brain.screen.set_fill_color(Color.BLACK)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.set_pen_width(2)
    brain.screen.draw_rectangle(x, y, w, h)

    brain.screen.set_font(FontType.MONO15)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.print_at(name, x=x + 15, y=y + 27)


def MainMenuButton():

    button(15, 195, 100, 30, "Back")


def AutoSelectorButton():

    button(20, 55, 200, 50, "Auto")


def SetingsButton():

    button(260, 55, 200, 50, "Settings")


def FieldButton():

    button(20, 120, 200, 50, "Field")


def InfoButton():

    button(260, 120, 200, 50, "Info")


def BlueSideButton():

    if auto_side == "Blue":
        brain.screen.set_fill_color(Color.BLUE)
    else:
        brain.screen.set_fill_color(Color.BLACK)

    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.draw_rectangle(20, 55, 200, 50)

    brain.screen.set_font(FontType.MONO15)
    brain.screen.print_at("Blue", x=90, y=82)


def RedSideButton():

    if auto_side == "Red":
        brain.screen.set_fill_color(Color.RED)
    else:
        brain.screen.set_fill_color(Color.BLACK)

    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.draw_rectangle(260, 55, 200, 50)

    brain.screen.set_font(FontType.MONO15)
    brain.screen.print_at("Red", x=330, y=82)


    
        


while True:

#disable Robot
    



    if Gui != LastGui:

        brain.screen.clear_screen()
        controller_1.screen.clear_row(1)

        if Gui == "MainMenu":

            disabled = False

            controller_1.buttonA.pressed(AutoAlign)

            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Enabled")

            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)

            brain.screen.print_at("Main Menu", x=170, y=30)

            AutoSelectorButton()
            SetingsButton()
            FieldButton()
            InfoButton()

        elif Gui == "SettingsMenu":

            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")

            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)

            brain.screen.print_at("Settings", x=175, y=30)

            brain.screen.set_font(FontType.MONO15)

            brain.screen.print_at(
                "Speed: " + str(drive_speed) + "%",
                x=20,
                y=65
            )

            button(20, 80, 100, 35, "50%")
            button(135, 80, 100, 35, "75%")
            button(250, 80, 100, 35, "100%")

            

            MainMenuButton()

        elif Gui == "AutoSelector":

            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")

            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)

            brain.screen.print_at("Auto Selector", x=125, y=30)

            BlueSideButton()
            RedSideButton()

            brain.screen.set_font(FontType.MONO15)

            brain.screen.print_at(
                "Side: " + auto_side,
                x=20,
                y=140
            )

            brain.screen.print_at(
                "Mode: " + auto_mode,
                x=20,
                y=165
            )

            MainMenuButton()

        elif Gui == "FieldMap":

            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")

            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)

            brain.screen.print_at("Override", x=175, y=30)

            # Field

            brain.screen.set_pen_width(2)
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_fill_color(Color.BLACK)

            brain.screen.draw_rectangle(75, 50, 330, 140)

            # Center

            brain.screen.draw_line(240, 50, 320, 120)
            brain.screen.draw_line(320, 120, 240, 190)
            brain.screen.draw_line(240, 190, 160, 120)
            brain.screen.draw_line(160, 120, 240, 50)

            # Midfield lines

            brain.screen.draw_line(75, 120, 160, 120)
            brain.screen.draw_line(320, 120, 405, 120)

            # Corner

            brain.screen.set_fill_color(Color.BLUE)
            brain.screen.draw_rectangle(80, 55, 45, 25)

            brain.screen.set_fill_color(Color.RED)
            brain.screen.draw_rectangle(355, 55, 45, 25)

            brain.screen.set_fill_color(Color.BLUE)
            brain.screen.draw_rectangle(80, 160, 45, 25)

            brain.screen.set_fill_color(Color.RED)
            brain.screen.draw_rectangle(355, 160, 45, 25)

            # Robot

            brain.screen.set_fill_color(Color.WHITE)
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.draw_circle(240, 120, 7)

            MainMenuButton()

        elif Gui == "InfoMenu":

            controller_1.screen.set_cursor(1, 1)
            controller_1.screen.print("Driving Disabled")

            brain.screen.set_font(FontType.MONO30)
            brain.screen.set_fill_color(Color.BLACK)
            brain.screen.set_pen_color(Color.WHITE)

            brain.screen.print_at("Robot Info", x=150, y=30)

            brain.screen.set_font(FontType.MONO15)

            brain.screen.print_at(
                "Battery: " +
                str(round(brain.battery.capacity(), 0)) +
                "%",
                x=20,
                y=70
            )

            brain.screen.print_at(
                "Temp: " +
                str(round(drivetrain.temperature(PERCENT), 0)) +
                " C",
                x=20,
                y=100
            )

            brain.screen.print_at(
                "Auton: " + auto_side + " " + auto_mode,
                x=20,
                y=130
            )

            brain.screen.print_at(
                "Speed: " + str(drive_speed) + "%",
                x=20,
                y=160
            )

            MainMenuButton()

        LastGui = Gui


    if brain.screen.pressing():

        x = brain.screen.x_position()
        y = brain.screen.y_position()


        if Gui == "MainMenu":

            if 20 <= x <= 220 and 55 <= y <= 105:
                Gui = "AutoSelector"

            elif 260 <= x <= 460 and 55 <= y <= 105:
                Gui = "SettingsMenu"

            elif 20 <= x <= 220 and 120 <= y <= 170:
                Gui = "FieldMap"

            elif 260 <= x <= 460 and 120 <= y <= 170:
                Gui = "InfoMenu"


        elif Gui == "SettingsMenu":

            if 15 <= x <= 115 and 195 <= y <= 225:
                Gui = "MainMenu"

            elif 20 <= x <= 120 and 80 <= y <= 115:
                drive_speed = 50
                LastGui = ""

            elif 135 <= x <= 235 and 80 <= y <= 115:
                drive_speed = 75
                LastGui = ""

            elif 250 <= x <= 350 and 80 <= y <= 115:
                drive_speed = 100
                LastGui = ""

            elif 20 <= x <= 170 and 130 <= y <= 165:
                drive_reverse = not drive_reverse
                LastGui = ""

            elif 190 <= x <= 340 and 130 <= y <= 165:
                controller_1.rumble(".")
                

        elif Gui == "AutoSelector":

            if 15 <= x <= 115 and 195 <= y <= 225:
                Gui = "MainMenu"

            elif 20 <= x <= 220 and 55 <= y <= 105:
                auto_side = "Blue"
                LastGui = ""

            elif 260 <= x <= 460 and 55 <= y <= 105:
                auto_side = "Red"
                LastGui = ""


        elif Gui == "FieldMap":

            if 15 <= x <= 115 and 195 <= y <= 225:
                Gui = "MainMenu"
            


        elif Gui == "InfoMenu":

            if 15 <= x <= 115 and 195 <= y <= 225:
                Gui = "MainMenu"


        wait(150, MSEC)

    wait(10, MSEC)
    
    #antiTip
    current_yaw = Internal_Sensor.orientation(OrientationType.PITCH, DEGREES)
    target_yaw = 0
    not_yaw = target_yaw - current_yaw
    speed = not_yaw * 0.5
        
    if not_yaw < -5:
        left_drive_smart.spin(REVERSE, speed, PERCENT)
        right_drive_smart.spin(REVERSE, speed, PERCENT)
    elif not_yaw > 5:
        left_drive_smart.spin(FORWARD, speed, PERCENT)
        right_drive_smart.spin(FORWARD, speed, PERCENT)
    else:
        left_drive_smart.stop()
        right_drive_smart.stop()
            
    wait(20, MSEC)

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
