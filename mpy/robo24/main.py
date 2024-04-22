
from window import *
from util import *
from display import Display
from robo24_window import Robo24Window
#from rover_window import RoverWindow
#from roz_window import RozWindow
#from ttrobot_window import TTRobotWindow
from admin_window import AdminWindow
import time, esp32, machine
from machine import Pin


#################
from secret import *
from telemetry import Telemetry
t = Telemetry(ROBO24_MAC_ADDRESS,WIFI_CHANNEL_NUM)
t.send_packet(b"ROBO24 test")
t.shutdown()

#################

sleep_flag = False

def sleep_handler():
    global sleep_flag
    sleep_flag = True

def do_sleep():
    global sleep_flag
    print('Going to sleep')
    sleep_flag = False
    #Pin(TouchManager.TOUCH_INTERRUPT_PIN, Pin.IN, None)
    #esp32.wake_on_ext0(pin = TouchManager.TOUCH_INTERRUPT_PIN, level = esp32.WAKEUP_ANY_HIGH)
    #machine.idle()
    #machine.lightsleep(60000)
    print('Waking from sleep')
    #Pin(TouchManager.TOUCH_INTERRUPT_PIN, Pin.IN, Pin.PULL_DOWN)

class Failsafe:
    def __init__(self):
        print('????? Failsafe Handheld')
        self.display = Display()
        print('Display initialized')

        # Flash robot image on screen before creating window system
        self.display.jpg('ROBO24-240.jpg', 0, 0)
        print('JPG Displayed')
        time.sleep_ms(1000)
        self.display.screen.fill(Color.BACKGROUND.as565())
        print('Screen cleared')

        self.window_manager = WindowManager(self.display, sleep_handler)
        print('Window Manager initialized')

        # add robots to windows chain
        self.robo24 = Robo24Window(self.window_manager, self.display)
        #self.roz = RozWindow(self.window_manager, self.display)
        #self.ttrobot = TTRobotWindow(self.window_manager, self.display)
        #self.robot_chain = WindowChain('Robots', [self.roz.root_window, self.rover.root_window, self.ttrobot.root_window])
        self.robot_chain = WindowChain('Robots', [self.robo24.root_window])

        # create windows chain
        self.admin = AdminWindow(self.window_manager, self.display, self.robot_chain)
        self.admin.register_theme_callback(self.switched_theme)
        self.admin_chain = WindowChain('Admin', [self.admin.window, self.admin.theme_window])
        self.window_manager.push_window_chain(self.admin_chain)

    def shutdown(self):
        self.window_manager.shutdown()

    def switched_theme(self):
        self.window_manager.pop_window()
        self.admin = AdminWindow(self.window_manager, self.display, self.robot_chain)
        self.admin.register_theme_callback(self.switched_theme)
        self.admin_chain = WindowChain('Admin', [self.admin.theme_window, self.admin.window])
        self.window_manager.push_window_chain(self.admin_chain)


#=================================================


theme = Theme.read_from_file('modern_dark')
theme.apply()

failsafe = Failsafe()

try:
    while True:
        time.sleep_ms(100)
        if sleep_flag:
            do_sleep()
except KeyboardInterrupt:
    failsafe.shutdown()
