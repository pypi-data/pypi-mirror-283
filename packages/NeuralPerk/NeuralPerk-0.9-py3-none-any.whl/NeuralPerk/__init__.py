import json
import requests
import keras
import pickle
import sys

from PyQt5.QtCore import Qt  # Import Qt module for alignment
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox



from keras import models as keras_models


from .NeuralPerk_Tensorflow import Tensorflow_Manager 
from .NeuralPerk_Torch import Torch_Manager
