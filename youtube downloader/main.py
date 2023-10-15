import os
from PyQt5 import QtCore
from pytube import YouTube
import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from default import Ui_mainWindow

class Downloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.btnDownload.clicked.connect(self.download_url)
        self.ui.btnBrowse.clicked.connect(self.browse_save_location)
        self.ui.btnClear.clicked.connect(self.clear)
        self.ui.btnExit.clicked.connect(self.exit_app)
        
    def browse_save_location(self):
        options = QFileDialog.Options()
        options &= ~QFileDialog.DontUseNativeDialog 
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4);;All Files (*)", options=options)

        if file_name:
            save_to_folder = os.path.dirname(file_name)
            self.ui.lneSaveTo.setText(save_to_folder)

    def download_url(self):
        link = self.ui.lneUrl.text()
        save_to = self.ui.lneSaveTo.text()

        if link != "":
            youtube_object = YouTube(link)
            youtube_stream = youtube_object.streams.get_highest_resolution()

            if not save_to:
                save_to = os.path.join(os.path.expanduser("~"), "Downloads")

            # Show starting message
            QMessageBox.information(self, "Started", "Downloading started.")

            try:
                youtube_stream.download(output_path=save_to)
                # Show completion message
                QMessageBox.information(self, "Completed", "Download completed.")
            except Exception as e:
                print("An error occurred:", e)
                QMessageBox.warning(self, "Error", "An error occurred during download.")
    
    def clear(self):
        self.ui.lneUrl.clear()
        self.ui.lneSaveTo.clear()
    
    def exit_app(self):
        QApplication.quit()    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Downloader()
    window.show()
    sys.exit(app.exec_())

