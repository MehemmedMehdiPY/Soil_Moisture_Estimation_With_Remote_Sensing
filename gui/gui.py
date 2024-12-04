from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView, QVBoxLayout, QMessageBox
from .constants import CITIES
import os
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import sys
sys.path.append("../")
from models import Dubois
from utils import (
    free_outliers,
    get_sar,
    transform2rgb,
    convert2image,
    ANGLE,
    apply_red2yellow_filter
)

class LaunchWIndow(QMainWindow):
    selected = False
    
    def __init__(self, root: str = "./data"):
        self.root = root
        
        super().__init__()
        
        self.setGeometry(800, 400, 500, 500)

        selection = QListWidget()
        selection.setSelectionMode(QAbstractItemView.NoSelection)
        self.__upload_items(selection)
        selection.currentRowChanged.connect(lambda : self.selection_triggered(selection))

        button = QPushButton("Button")
        button.clicked.connect(lambda : self.button_triggered(selection))

        layout = QVBoxLayout()
        layout.addWidget(selection)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
                
    def __upload_items(self, selection):
        for city in CITIES:
            item = QListWidgetItem(city)
            selection.addItem(item)
    
    def selection_triggered(self, selection):
        if selection.currentRow() != -1:
            self.selected = True        
    
    def button_triggered(self, selection):
        if not self.selected:
            message = "Choose an item"
            message_box = QMessageBox()
            message_box.setText(message)
            message_box.setGeometry(800, 500, 500, 500)
            message_box.exec_()
        
        else:
            sleep(1)
            choice_idx = selection.currentRow()
            self.plot_soil_moisture(choice_idx)
            selection.setCurrentRow(-1)
            self.selected = False
    
    def plot_soil_moisture(self, choice_idx):
        path_tiff = self.get_tiff_path(choice_idx=choice_idx)
        sar, _ = get_sar(path_sar=path_tiff)
        image = self.get_soil_moisture(sar)
        plt.imshow(image)
        plt.show()

    def get_soil_moisture(self, sar):
        vv, vh = sar[0], sar[1]
        sm = Dubois(vv=vv, vh=vh, angle=ANGLE)
        sm = free_outliers(sm[None], whis=1.5)[0]
        sm[sm < 0.2] = 0.2
        sm_mapped_before = transform2rgb(sm)
        sm_mapped_after = apply_red2yellow_filter(sm_mapped_before, f=0.5)

        image = self.combine_images(sm_mapped_before, sm_mapped_after)
        image = convert2image(image)
        
        return image

    def combine_images(self, image_1, image_2):
        image_1.shape[0]
        border = np.zeros((image_1.shape[0], 20, 3))
        image = np.concatenate((image_1, border, image_2), axis=1)
        return image

    def get_tiff_path(self, choice_idx):
        city_name = CITIES[choice_idx]
        path_folder = os.path.join(self.root, city_name, "tiff")
        tiff_name = os.listdir(path_folder)[0]
        path_tiff = os.path.join(path_folder, tiff_name)
        return path_tiff
    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = LaunchWIndow()
    window.show()
    app.exec()