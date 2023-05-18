"""
这个程序实现了一个简单的倒计时器，可以在系统托盘中运行
"""
import sys
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QIcon, QFont, QPalette
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTimeEdit


class CountdownWidget(QWidget):
    def __init__(self, time_left, reset_value, break_time):
        super().__init__()
        """初始化实例变量"""

        # 定时器剩余时间，以秒为单位
        self.time_left = time_left  
        # 重置定时器时，设置的定时器剩余时间
        self.reset_value = reset_value
        # 设置休息时间
        self.break_time = break_time
        # 创建定时器
        self.timer = QTimer()

    def create_widget_layout(self):
        """创建Widget窗口布局"""

        # 当发送超时信号时，触发self.update_timer方法
        self.timer.timeout.connect(self.update_timer)

        # 创建用于显示倒计时的标签
        hours,minutes,seconds =self.get_time(self.time_left)
        self.label = QLabel(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.label.setAlignment(Qt.AlignCenter)

        # 创建“开始”按钮以启动倒计时
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start)

        # 创建“暂停”按钮以暂停倒计时
        self.pause_button = QPushButton("暂停")
        self.pause_button.clicked.connect(self.pause)

        # 创建按钮以重置倒计时并立即开始倒计时
        hours,minutes,seconds =self.get_time(self.reset_value)
        self.reset_button = QPushButton(f"{hours:02d}:{minutes:02d}:{seconds:02d} 倒计时")
        self.reset_button.clicked.connect(self.custom_countdown)

        # 创建休息按钮以重置倒计时并立即开始休息倒计时
        hours,minutes,seconds =self.get_time(self.break_time)
        self.break_time_button = QPushButton(f"休息: {hours:02d}:{minutes:02d}:{seconds:02d}")
        self.break_time_button.clicked.connect(self.break_time_countdown)

        # 创建一个包含QTimeEdit的QWidget并将其添加到布局中
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("hh:mm:ss")
        hours,minutes,seconds =self.get_time(self.time_left)
        self.time_edit.setTime(QTime(hours, minutes, seconds))
        self.time_edit.timeChanged.connect(self.update_time_left)

        # 创建一个复选框以将窗口固定在顶部
        self.pin_checkbox = QCheckBox("置顶")
        self.pin_checkbox.setChecked(False)
        self.pin_checkbox.stateChanged.connect(self.toggle_pin)

        # 创建窗口布局
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
        """创建托盘图标及其菜单"""
        menu = QMenu()

        self.icon = QIcon("icon.png")
        self.tray_icon = QSystemTrayIcon(self.icon)
        self.tray_icon.show()

        # 将剩余时间操作添加到菜单
        self.time_left_action = QAction("剩余时间: 30:00")
        menu.addAction(self.time_left_action)
        menu.addSeparator()

        # 将打开操作添加到菜单
        open_action = QAction("打开页面", app)
        open_action.triggered.connect(self.show)
        menu.addAction(open_action)
        menu.addSeparator()

        # 将开始、暂停、自定义倒计时和退出操作添加到菜单
        open_action = menu.addAction(f"开始")
        open_action.triggered.connect(self.start)
        menu.addSeparator()
        stop_action = menu.addAction("暂停")
        stop_action.triggered.connect(self.pause)   
        menu.addSeparator()
        hours,minutes,seconds =self.get_time(self.reset_value)
        reset_action = menu.addAction(f"{hours:02d}:{minutes:02d}:{seconds:02d}倒计时")
        reset_action.triggered.connect(self.custom_countdown)        
        menu.addSeparator()
        hours,minutes,seconds =self.get_time(self.break_time)
        reset_action = menu.addAction(f"休息{hours:02d}:{minutes:02d}:{seconds:02d}")
        reset_action.triggered.connect(self.break_time_countdown)        
        menu.addSeparator()
        quit_action = menu.addAction("退出")
        quit_action.triggered.connect(self.quit)

        self.tray_icon.setContextMenu(menu)
    
    def create_layout_menu(self):
        """widget 创建布局，系统状态栏创建菜单"""
        self.create_widget_layout()
        self.create_tray_icon()
        self.update_tray_icon()         

    def resize_windows(self, width, high):
        """设置窗口的默认大小"""
        self.resize(width, high)

    def get_time(self, time):
        """
        获取以小时、分钟为单位的剩余时间量，
        和秒格式
        """
        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = time % 60
        return hours, minutes, seconds

    def start(self):
        """
        启动倒计时并更新托盘图标
        """
        # 启动一个发出超时信号的定时器
        # 每 1000 毫秒（即 1 秒）
        self.timer.start(1000)
        self.update_tray_icon()
        hours, minutes, seconds = self.get_time(self.time_left)
        self.show_notification("定时器开始",
                               f"开始 {hours:02d}:{minutes:02d}:{seconds:02d}")

    def pause(self):
        """
        暂停倒数计时器并更新托盘图标
        """
        self.timer.stop()
        self.update_tray_icon()
        hours, minutes, seconds = self.get_time(self.time_left)
        # self.show_notification("Time pause",
        #                        f"Start {hours:02d}:{minutes:02d}:{seconds:02d}")

    def custom_countdown(self):
        """
        将倒数计时器重置为 self.reset_value，然后
        立即开始倒计时
        """
        self.time_left = self.reset_value
        hours,minutes,seconds =self.get_time(self.reset_value)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.time_edit.setTime(QTime(hours, minutes,seconds))
        self.start()
        self.update_tray_icon()

    def break_time_countdown(self):
        """设置休息倒计时，并立即开始倒计时
        """
        self.time_left = self.break_time
        hours,minutes,seconds =self.get_time(self.break_time)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.time_edit.setTime(QTime(hours, minutes,seconds))
        self.start()
        self.update_tray_icon()


    def time_left_set_zero(self):
        """
        将剩余时间设置为0，暂停倒计时，
        并更新标签和时间编辑
        """
        self.time_left = 0
        self.pause()
        self.label.setText("00:00:00")
        self.time_edit.setTime(QTime(0, 0, 0))
        self.update_tray_icon()

    def update_timer(self):
        """
        每秒更新倒计时标签和托盘图标，
        并在时间到了时显示通知
        """
        if self.time_left < 0:
            self.time_left_set_zero()
            self.show_notification("时间到",
                                   "您的倒计时已过期！")
            return
        hours, minutes, seconds = self.get_time(self.time_left)
        self.label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.update_tray_icon()
        self.time_left -= 1

    def update_tray_icon(self):
        """
        用剩余时间和工具提示更新托盘图标
        """
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        text = f"剩余时间: {minutes:02d}:{seconds:02d}"
        self.time_left_action.setText(text)
        self.tray_icon.setToolTip(text)
        self.tray_icon.setIcon(self.icon)

    def quit(self):
        """
        隐藏托盘图标并退出应用程序
        """
        self.tray_icon.hide()
        sys.exit()
    
    def update_time_left(self, qtime):
        """
        根据时间编辑中的用户输入更新剩余时间
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
        切换固定复选框以保持窗口在顶部或不在顶部
        
        | 运算符可以用于标志位的处理
        代码中，| 运算符用于将 Qt.WindowStaysOnTopHint 标志添加到当前窗口的标志中。
        """
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
    
    def show_notification(self, string1, string2):
        """
        显示带有消息和标题的通知
        """
        self.tray_icon.showMessage(string1, string2, QSystemTrayIcon.Information)
    
    def closeEvent(self, event):
        """
        覆盖关闭事件以隐藏窗口而不是关闭它
        """
        self.hide()
        event.ignore()
    
    def showEvent(self, event):
        """
        覆盖显示事件以将窗口移动到右下角
        屏幕的
        """
        super().showEvent(event)
        tray_geometry = self.tray_icon.geometry()
        widget_geometry = self.frameGeometry()
        x = tray_geometry.right()
        y = tray_geometry.bottom() - int(widget_geometry.height()*(1+1/3))
        self.move(x, y)


if __name__ == "__main__":

    # 初始化常量
    # 设置定时器的定时初始值的秒数
    INIT_TIME_LEFT_AMOUNT = 1800
    # 设置定时器重置的秒数
    RESET_VALUE = 60*60
    # 设置休息时间秒数
    BREAK_TIME = 60*15

    app = QApplication(sys.argv)
    # 设置应用程序窗口名称
    app.setApplicationName("倒计时")

    # 将调色板设置为黑色背景和白色字体
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.lightGray)
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Button, Qt.gray)
    palette.setColor(QPalette.ButtonText, Qt.black)
    app.setPalette(palette)
    
    # 设置全局字体大小
    font = QFont("Arial", 14, QFont.Bold)
    QApplication.setFont(font)

    # 创建一个 CountdownWidget 对象并开始倒计时
    countdownwidget = CountdownWidget(time_left=INIT_TIME_LEFT_AMOUNT,
                                      reset_value=RESET_VALUE,
                                      break_time=BREAK_TIME)
    # 设置窗口大小
    countdownwidget.resize_windows(300, 200)
    # widget 创建布局，系统状态栏创建菜单
    countdownwidget.create_layout_menu()

    # 如果您想立即开始倒计时，请取消下面的代码注释
    # countdownwidget.start()

    sys.exit(app.exec_())