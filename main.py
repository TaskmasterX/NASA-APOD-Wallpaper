
import sys
import schedule
import threading
import time

from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtGui import QIcon

import gui



def start_daily_scheduler(window):
    # Run at 9:00 AM every day (change as needed)
    schedule.every().day.at("09:00").do(window.auto_update_wallpaper)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)

    threading.Thread(target=run_schedule, daemon=True).start()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(gui.resource_path("images/saturn.ico")))
    window= gui.MainWindow()
    window.show()
    start_daily_scheduler(window)
    sys.exit(app.exec_())