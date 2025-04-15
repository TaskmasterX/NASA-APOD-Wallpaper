import os
import sys
import ctypes

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QAction,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QMessageBox,
                             QLineEdit, QTextEdit, QPushButton, QRadioButton, QScrollArea, QDialog,
                             QComboBox, QGroupBox, QSystemTrayIcon, QMenu)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QTime

import get_apod

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setup parameters of the main window
        self.setWindowTitle("NASA Astronomy Picture of the Day Wallpaper")
        self.setFixedSize(900, 800)
        self.setWindowIcon(QIcon(resource_path('images/saturn.jpg')))

        #create the menu bar
        menu = self.menuBar()
        help_menu = menu.addMenu("&Help")
        self.instruction_action = QAction("&Instructions", self)
        help_menu.addAction(self.instruction_action)
        self.about_action = QAction("&About", self)
        help_menu.addAction(self.about_action)
        self.instruction_action.triggered.connect(self.show_instructions)
        self.about_action.triggered.connect(self.show_about)

        font = QFont()
        font.setPointSize(11)
        menu.setFont(font)

        
        #create Date group box
        self.date_group_box = QGroupBox("Date")
        self.date_group_layout = QHBoxLayout()
        self.date_group_box.setLayout(self.date_group_layout)
        
        #Create labels and combo boxes for month, day, and year
        #Month
        self.month_label = QLabel("Month:", self)
        self.month_combobox = QComboBox(self)
        self.month_combobox.setFixedSize(100,30)
        self.month_combobox.addItems(["", "January", "February", "March", "April",
                                       "May", "June", "July", "August", "September",
                                       "October", "November", "December"])
        self.month_combobox.setCurrentText("")
        self.month_combobox.setStyleSheet("QComboBox { background-color: white; }")
        #Day
        self.day_label = QLabel("Day:", self)
        self.day_combobox = QComboBox(self)
        self.day_combobox.setFixedSize(80,30)
        self.day_combobox.addItems(["", "01", "02", "03", "04", "05", "06",
                                    "07", "08", "09", "10", "11", "12", "13", "14",
                                    "15", "16", "17", "18", "19", "20", "21", "22",
                                    "23", "24", "25", "26", "27", "28", "29", "30",
                                    "31"])
        self.day_combobox.setCurrentText("")
        self.day_combobox.setStyleSheet("QComboBox { background-color: white; }")
        #Year
        self.year_label = QLabel("Year:", self)
        self.year_textbox = QLineEdit(self)
        self.year_textbox.setFixedSize(80,30)

        self.spacer_label = QLabel("")

        self.get_image_button = QPushButton("Get Image")
        self.get_image_button.setFixedSize(120,40)

        self.get_image_button.clicked.connect(self.display_image_by_date)
        

        self.date_group_layout.addWidget(self.month_label, alignment=Qt.AlignRight)
        self.date_group_layout.addWidget(self.month_combobox)
        self.date_group_layout.addWidget(self.day_label, alignment=Qt.AlignRight)
        self.date_group_layout.addWidget(self.day_combobox)
        self.date_group_layout.addWidget(self.year_label, alignment=Qt.AlignRight)
        self.date_group_layout.addWidget(self.year_textbox)
        self.date_group_layout.addWidget(self.spacer_label)
        self.date_group_layout.addWidget(self.get_image_button)

        
        #Create radio buttons group box for Current and Random
        self.radio_group_box = QGroupBox("Daily Image")
        self.radio_group_layout = QHBoxLayout()
        self.radio_group_layout.setSpacing(30)
        self.radio_group_box.setLayout(self.radio_group_layout)
        self.current_radio = QRadioButton("Current", self)
        self.current_radio.setChecked(True)
        self.random_radio = QRadioButton("Random", self)

        self.radio_group_layout.addWidget(self.current_radio)
        self.radio_group_layout.addWidget(self.random_radio)


        #Create the image and explanation display area
        self.image_label = QLabel("Select a date to view the image for that day.\nJune 16, 1995 - Present Day")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("font-size: 14px;")


        #Create buttons for Set As Wallpaper and Exit
        self.get_current_button = QPushButton("Get Current Image")
        self.get_current_button.setFixedSize(200,50)
        self.save_button = QPushButton("Set As Wallpaper")
        self.exit_button = QPushButton("Exit")
        self.save_button.setFixedSize(200,50)
        self.exit_button.setFixedSize(150,50)
        self.get_current_button.clicked.connect(self.get_current_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)


        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('images/saturn.jpg')))  # Use a valid icon file

        # Create a context menu for the tray icon
        tray_menu = QMenu()

        restore_action = QAction("Restore", self)
        quit_action = QAction("Exit", self)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        restore_action.triggered.connect(self.show_normal_window)
        quit_action.triggered.connect(QApplication.instance().quit)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)


        self.initUI()



    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        bottom_buttons_layout = QHBoxLayout()
        #bottom_buttons_layout.setSpacing(700)

        central_widget.setLayout(layout)

        layout.addWidget(self.date_group_box, 0, 0)
        layout.addWidget(self.radio_group_box, 0, 1)
        layout.addWidget(self.image_label, 2, 0, 1, 2)
        layout.addWidget(self.text_area, 3, 0, 1, 2)
        bottom_buttons_layout.addWidget(self.get_current_button, alignment=Qt.AlignLeft)
        bottom_buttons_layout.addWidget(self.save_button)
        bottom_buttons_layout.addWidget(self.exit_button, alignment=Qt.AlignRight)
        layout.addLayout(bottom_buttons_layout, 4, 0, 1, 2)
        # layout.addWidget(self.get_current_button, 4, 0)
        # layout.addWidget(self.save_button, 4, 1)
        # layout.addWidget(self.exit_button, 4, 2, alignment=Qt.AlignRight)


        self.setStyleSheet("""
            QWidget{
                font-family: "Consolas";
            }
            QGroupBox{
                font-size: 14px;
            }
            QLabel{
                font-size: 14px;
            }
            QPushButton{
                font-size: 16px;
            }
            QPushButton:focus {
                border: 2px solid #0078d4;
                background-color: #e6f7ff;
            }
            QRadioButton{
                font-size: 14px;
            }
            QLineEdit{
                font-size: 14px;
                border: 2px inset gray;
            }
            QComboBox{
                background-color: white; 
                font-size: 14px;
            }
            """)



    #Click the Get Image button to get the image for the selected date
    def display_image_by_date(self):
        # Check if the date is valid
        month = self.month_combobox.currentText()
        day = self.day_combobox.currentText()
        year = self.year_textbox.text()

        if month and day and year:
            month = self.month_combobox.currentIndex()
            if month < 10:
                month = f"0{month}"
            date = f"{year}-{month}-{day}"

            image_data, title, caption = get_apod.get_apod_image(date)
            if image_data is None:
                QMessageBox.warning(self, "Error", "No image found for the selected date.")
                return
            
            self.save_file(image_data)

            #display the image
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # Resize to fit width (optional)
            scaled_pixmap = pixmap.scaledToWidth(780, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

            # Set explanation text
            self.text_area.setText(f"{title}\n\n{caption}")

            self.save_button.setFocus()
        else:
            QMessageBox.warning(self, "Error", "Please select a valid date.")



    #Click the Get Current Image button to get the current image
    def get_current_button_clicked(self):
        # Get the current date
        date = get_apod.get_daily_image(mode="current")
        image_data, title, caption = get_apod.get_apod_image(date)
        if image_data is None:
            QMessageBox.warning(self, "Error", "No image found for the selected date.")
            return
        
        self.save_file(image_data)

        #display the image and text in the app
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaledToWidth(780, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.text_area.setText(f"{title}\n\n{caption}")

        self.save_button.setFocus()



    def save_button_clicked(self):
        if hasattr(self, 'image_path') and os.path.exists(self.image_path):
            try:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, self.image_path, 3)
            except Exception as e:
                QMessageBox.warning(self, "Error", "Failed to set wallpaper.")
        else:
            QMessageBox.warning(self, "Error", "No image available to set as wallpaper.")



    def exit_button_clicked(self):
        msg = QMessageBox()
        font = QFont("Consolas", 12)
        msg.setFont(font)
        msg.setWindowIcon(QIcon(resource_path('images/question.jpg')))
        msg.setWindowTitle("Confirm Exit")
        msg.setText("Are you sure you want to exit?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msg.exec_()
        if result == QMessageBox.Ok:
            QApplication.instance().quit()



    def show_instructions(self):
        instructions_dialog = QDialog()
        instructions_dialog.setWindowIcon(QIcon(resource_path('images/M94.jpg')))
        instructions_dialog.setWindowTitle("Instructions")
        instructions_dialog.resize(700, 800)
        instructions_label = QLabel("""NASA Astronomy Picture of the Day Wallpaper 		.v 1.00.00			By Jason Pritchard


The NASA Astronomy Picture of the Day Wallpaper app allows you to view the current NASA Astronomy Picture of the Day (APOD) or any from the archive and set them as the background image for your Desktop.

If you have any questions or comments, email me at jason.ace72@gmail.com



INSTRUCTIONS

1. Select a month and day from the drop down boxes and type in the year.  The date must be between June 16, 1995 and the current date.
                                    
2. Click the "Get Image" button to retrieve the image for that date.  The image will be displayed in the window along with the title and explanation.
                                    
3. You can use the "Get Current Image" button to quickly display the current image for today.
                                    
4. Click the "Set As Wallpaper" button to set the image as your desktop wallpaper.
                                    
It may take a few seconds for the image to appear in the app since it is being downloaded from the NASA API.

It is also possible, but rare, that the selected date is a video instead of an image.  If this happens, you will be notified with a message box.
                                    

The app will automatically update the wallpaper every day at 9:00 AM using the current or random image, depending on the selected radio button.
                                    
The random image will be selected from a date between June 16, 1995 and the current date.
                                    
The app must be running for the automatic update to work.  You can minimize the app to the system tray by clicking the "X" button in the top right corner.  To restore the app, click the tray icon.
                                    
To exit the app, click the "Exit" button.  You will be prompted to confirm the exit.


-Jason Pritchard
jason.ace72@gmail.com
                                    """)
        instructions_label.setFont(QFont('Consolas', 12))
        instructions_label.setWordWrap(True)
        instructions_label.resize(700, 800)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(instructions_label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        instructions_dialog.setLayout(layout)
        instructions_dialog.exec_()



    def show_about(self):
        about_dialog = QDialog()
        about_dialog.setFont(QFont('Consolas', 20))
        about_dialog.setWindowIcon(QIcon(resource_path('images/ring_nebula.jpg')))
        about_dialog.setWindowTitle("About NASA Astronomy Picture of the Day Wallpaper")
        about_dialog.resize(650, 320)

        #add the image
        pixmap = QPixmap(resource_path('images/galaxy.jpg'))
        about_image = QLabel()
        about_image.setPixmap(pixmap)
        about_image.setAlignment(Qt.AlignLeft)
        about_image.setFixedSize(200, 300)
        about_image.setScaledContents(True)

        # Add text labels
        title_label = QLabel("NASA Astronomy Picture of the Day Wallpaper\n")
        title_label.setFont(QFont('Consolas', 12))
        title_label.setStyleSheet("color: black; font-size: 12px; background-color: rgba(0, 0, 0, 0);")

        # Version and copyright label
        version_label = QLabel("Version 1.0.0.0\n\nCopyright © 2025")
        version_label.setFont(QFont('Consolas', 12))
        version_label.setStyleSheet("color: black; font-size: 12px; background-color: rgba(0, 0, 0, 0);")

        # Author information
        author_label = QLabel("\n\nJason Pritchard\n")
        author_label.setFont(QFont('Consolas', 12))
        author_label.setStyleSheet("color: black; font-size: 12px; background-color: rgba(0, 0, 0, 0);")

        # Information label
        info_label = QTextEdit("""Automatically updates your Desktop background to the current or random NASA Astronomy Picture of the Day image or allows you to select an image manually.
        Contact: jason.ace72@gmail.com"""
        )
        info_label.setFont(QFont('Consolas', 12))
        info_label.setStyleSheet("color: black; font-size: 12px; background-color: rgba(0, 0, 0, 0);")

        # OK button to close the dialog
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(70, 35)
        ok_button.setStyleSheet("color: black; font-size: 14px;")
        ok_button.clicked.connect(about_dialog.accept)

        # Layout setup
        layout = QHBoxLayout()
        info_layout = QVBoxLayout()

        info_layout.addWidget(title_label)
        info_layout.addWidget(version_label)
        info_layout.addWidget(author_label)
        info_layout.addWidget(info_label)
        info_layout.addWidget(ok_button, alignment=Qt.AlignRight)

        layout.addWidget(about_image)
        layout.addLayout(info_layout)
        about_dialog.setLayout(layout)

        # Show as a modal dialog
        about_dialog.exec_()





    #Update the wallpaper automatically every day at 9:00 AM using the current or random image
    def auto_update_wallpaper(self):
        print("Running auto update wallpaper")
        mode = "current" if self.current_radio.isChecked() else "random"
        date = get_apod.get_daily_image(mode=mode)
        image_data, title, caption = get_apod.get_apod_image(date)
        if image_data is None:
            QMessageBox.warning(self, "Error", "No image found for the selected date.")
            return
        
        self.save_file(image_data)

        #display the image and text in the app
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaledToWidth(780, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.text_area.setText(f"{title}\n\n{caption}")
        
        # Set the wallpaper using the Windows API
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.image_path, 3)

            

    #Save the image to a temporary location
    # This is used to set the wallpaper and display the image in the app
    def save_file(self, image_data):
        # Save the image to a temporary location
        self.image_path = os.path.join(os.getenv('TEMP'), "apod_wallpaper.jpg")
        with open(self.image_path, 'wb') as f:
            f.write(image_data)


    
    #System tray icon functions
    #Override close event to minimize to tray
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "Minimized",
            "The app is still running in the system tray.",
            QSystemTrayIcon.Information,
            2000
        )

    #restore window
    def show_normal_window(self):
        self.show()
        self.tray_icon.hide()

    #restore window when tray icon is clicked
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal_window()
        

    def setup_daily_timer(self, target_time_str):
        # Parse target time
        target_time = QTime.fromString(target_time_str, "HH:mm")

        # Current time
        now = QTime.currentTime()
        msecs_until = now.msecsTo(target_time)

        # If the target time already passed today, schedule for tomorrow
        if msecs_until < 0:
            msecs_until += 24 * 60 * 60 * 1000  # add 24 hours

        # Single-shot timer to run once at target time
        self.daily_timer = QTimer(self)
        self.daily_timer.setSingleShot(True)
        self.daily_timer.timeout.connect(self.run_daily_update)
        self.daily_timer.start(msecs_until)
    

    def run_daily_update(self):
        self.auto_update_wallpaper()
        # Set timer again for the next day
        self.setup_daily_timer("16:30")





def resource_path(relative_path):
    #Get absolute path to resource, works for PyInstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("images/saturn.ico")))
    window= MainWindow()
    window.show()
    #start_daily_scheduler(window)
    window.setup_daily_timer("16:30")
    sys.exit(app.exec_())