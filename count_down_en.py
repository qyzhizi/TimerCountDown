"""
This program implements a simple countdown timer and it can also runs in the system tray. 
"""
import sys
from PyQt5.QtCore import QTimer,Qt,QTime
from PyQt5.QtGui import QIcon, QFont, QPalette
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget 
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTimeEdit


class CountdownWidget(QWidget):
    def __init__(self, time_left, reset_value, break_time):
        super().__init__()
        
        # Initialize instance variables
        self.time_left = time_left  # 30 minutes in seconds
        self.reset_value = reset_value
        # set break time
        self.break_time = break_time
        # create timer
        self.timer = QTimer()

    def create_widget_layout(self):
        """Create widget window layout"""

        # When a timeout signal is sent,
        # the self.update timer method is triggered
        self.timer.timeout.connect(self.update_timer)

        # Create the label used to display the countdown
        hours,minutes,seconds =self.get_time(self.time_left)
        self.label = QLabel(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.label.setAlignment(Qt.AlignCenter)

        # Create the Start button to start the countdown
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)

        # Create the Pause button to pause the countdown
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)

        # Create button to reset countdown and start countdown immediately
        hours,minutes,seconds =self.get_time(self.reset_value)
        self.reset_button = QPushButton(f"{hours:02d}:{minutes:02d}:{seconds:02d} countdown")
        self.reset_button.clicked.connect(self.custom_countdown)

        # Create a rest button to reset the countdown and
        # start countdown to rest immediately
        hours,minutes,seconds =self.get_time(self.break_time)
        self.break_time_button = QPushButton(f"break: {hours:02d}:{minutes:02d}:{seconds:02d}")
        self.break_time_button.clicked.connect(self.break_time_countdown)

        # Create a q widget containing q time edit and add it to the layout
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm:ss")
        hours,minutes,seconds =self.get_time(self.time_left)
        self.time_edit.setTime(QTime(hours, minutes, seconds))
        self.time_edit.timeChanged.connect(self.update_time_left)

        # Create a checkbox to pin the window on top
        self.pin_checkbox = QCheckBox("Pin to top")
        self.pin_checkbox.setChecked(False)
        self.pin_checkbox.stateChanged.connect(self.toggle_pin)

        # Create the layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.pause_button)
        layout.addLayout(control_layout)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.break_time_button)
        layout.addWidget(self.time_edit)
        layout.addWidget(self.pin_checkbox)
        self.setLayout(layout)

    def create_tray_icon(self):
        """Create a tray icon and its menu"""
        menu = QMenu()

        self.icon = QIcon("icon.png")
        self.tray_icon = QSystemTrayIcon(self.icon)
        self.tray_icon.show()

        # Add the time left action to the menuG
        self.time_left_action = QAction("Time left: 30:00")
        menu.addAction(self.time_left_action)
        menu.addSeparator()

        # Add the Open action to the menu
        open_action = QAction("Open main window", app)
        open_action.triggered.connect(self.show)
        menu.addAction(open_action)
        menu.addSeparator()

        # Add the Start, Pause, 30minutes and Quit actions to the menu
        open_action = menu.addAction(f"Start")
        open_action.triggered.connect(self.start)
        menu.addSeparator()
        stop_action = menu.addAction("Pause")
        stop_action.triggered.connect(self.pause)   
        menu.addSeparator()
        hours,minutes,seconds =self.get_time(self.reset_value)
        reset_action = menu.addAction(f"{hours:02d}:{minutes:02d}:{seconds:02d} countdown")
        reset_action.triggered.connect(self.custom_countdown)        
        menu.addSeparator()
        hours,minutes,seconds =self.get_time(self.break_time)
        reset_action = menu.addAction(f"break {hours:02d}:{minutes:02d}:{seconds:02d}")
        reset_action.triggered.connect(self.break_time_countdown)        
        menu.addSeparator()
        quit_action = menu.addAction("quit")
        quit_action.triggered.connect(self.quit)

        self.tray_icon.setContextMenu(menu)
    
    def create_layout_menu(self):
        """Widget creates layout, system status bar creates menu"""
        self.create_widget_layout()
        self.create_tray_icon()
        self.update_tray_icon()         

    def resize_windows(self, width, high):
        """Set the default size of the window"""
        self.resize(width, high)

    def get_time(self, time):
        """
        Get the amount of time left in hours, minutes,
        and seconds format
        """
        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = time % 60
        return hours, minutes, seconds

    def start(self):
        """
        Start the countdown timer and update the tray icon
        """
        # Start a timer that emits a timeout signal 
        # every 1000 milliseconds (ie 1 second)
        self.timer.start(1000)
        self.update_tray_icon()
        hours, minutes, seconds = self.get_time(self.time_left)
        self.show_notification("timer starts",
                               f"start {hours:02d}:{minutes:02d}:{seconds:02d}")

    def pause(self):
        """
        Pause the countdown timer and update the tray icon
        """
        self.timer.stop()
        self.update_tray_icon()
        hours, minutes, seconds = self.get_time(self.time_left)
        # self.show_notification("Time pause",
        #                        f"Start {hours:02d}:{minutes:02d}:{seconds:02d}")

    def custom_countdown(self):
        """
        Reset the countdown timer to 30 minutes and
        start the countdown immediately
        """
        self.time_left = self.reset_value
        hours,minutes,seconds =self.get_time(self.reset_value)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.time_edit.setTime(QTime(hours, minutes,seconds))
        self.start()
        self.update_tray_icon()

    def break_time_countdown(self):
        """Set a countdown to a break and start the countdown immediately
        """
        self.time_left = self.break_time
        hours,minutes,seconds =self.get_time(self.break_time)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.time_edit.setTime(QTime(hours, minutes,seconds))
        self.start()
        self.update_tray_icon()


    def time_left_set_zero(self):
        """
        Set the time left to 0, pause the countdown timer,
        and update the label and time edit
        """
        self.time_left = 0
        self.pause()
        self.label.setText("00:00:00")
        self.time_edit.setTime(QTime(0, 0, 0))
        self.update_tray_icon()

    def update_timer(self):
        """
        Update the countdown label and tray icon every second,
        and show a notification when the time is up
        """
        if self.time_left < 0:
            self.time_left_set_zero()
            self.show_notification("Time's up",
                                   "Your countdown timer has expired!")
            return
        hours, minutes, seconds = self.get_time(self.time_left)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.update_tray_icon()
        self.time_left -= 1

    def update_tray_icon(self):
        """
        Update the tray icon with the time left and tooltip
        """
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        text = f"Time left: {minutes:02d}:{seconds:02d}"
        self.time_left_action.setText(text)
        self.tray_icon.setToolTip(text)
        self.tray_icon.setIcon(self.icon)

    def quit(self):
        """
        Hide the tray icon and exit the application
        """
        self.tray_icon.hide()
        sys.exit()
    
    def update_time_left(self, qtime):
        """
        Update the time left based on the user input in the time edit
        """
        try:
            hours, minutes, seconds = qtime.hour(), qtime.minute(), qtime.second()
            self.time_left = hours * 3600 + minutes * 60 + seconds
            if self.time_left == 0:
                self.label.setText("00:00:00")
                return 
            self.update_timer()
        except ValueError:
            pass
    
    def toggle_pin(self, state):
        """
        Toggle the pin checkbox to keep the window on top or not

        The | operator can be used to process flags
        In the code, the | operator is used to add the
        Qt.WindowStaysOnTopHint flag to the flags of the current window.
        """
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
    
    def show_notification(self, string1, string2):
        """
        Show a notification with a message and title
        """
        self.tray_icon.showMessage(string1, string2, QSystemTrayIcon.Information)
    
    def closeEvent(self, event):
        """
        Override the close event to hide the window instead of closing it
        """
        self.hide()
        event.ignore()
    
    def showEvent(self, event):
        """
        Override the show event to move the window to the bottom right
        of the screen
        """
        super().showEvent(event)
        tray_geometry = self.tray_icon.geometry()
        widget_geometry = self.frameGeometry()
        x = tray_geometry.right()
        y = tray_geometry.bottom() - int(widget_geometry.height()*(1+1/3))
        self.move(x, y)


if __name__ == "__main__":

    # initialization constant
    # Set the number of seconds for the initial value of the timer
    INIT_TIME_LEFT_AMOUNT = 1800
    # Set the number of seconds to reset the timer
    RESET_VALUE = 60*60
    # Set break time seconds
    BREAK_TIME = 60*15

    app = QApplication(sys.argv)
    # Set the application window name
    app.setApplicationName("Countdown")

    # Set the palette to black background and white font
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.lightGray)
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Button, Qt.gray)
    palette.setColor(QPalette.ButtonText, Qt.black)
    app.setPalette(palette)
    
    # Set global font size
    font = QFont("Arial", 14, QFont.Bold)
    QApplication.setFont(font)

    # Create a CountdownWidget object and start the countdown
    countdownwidget = CountdownWidget(time_left=INIT_TIME_LEFT_AMOUNT,
                                      reset_value=RESET_VALUE,
                                      break_time=BREAK_TIME)
    # set window size
    countdownwidget.resize_windows(300, 200)
    # Widget creates layout, system status bar creates menu
    countdownwidget.create_layout_menu()

    # If you want to start countdown immediately then uncomment below
    # countdownwidget.start()

    sys.exit(app.exec_())