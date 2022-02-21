import threading

from PySide6.QtCore import (
	QObject,
	QPoint,
	QRect,
	Slot,
	Qt
)
from PySide6.QtGui import (
	QFont,
	QIcon
)
from PySide6.QtWidgets import (
	QCommandLinkButton,
	QApplication,
	QMainWindow,
	QScrollArea,
	QSizePolicy,
	QVBoxLayout,
	QMenuBar,
	QWidget,
	QLabel
)

from breakfast import BreakFast
import resources


class BreakFastWindow(QMainWindow):
	def set_breakfast(self):
		def set_recipe():
			self.breakfast = BreakFast.random()
		
		thread = threading.Thread(target=set_recipe)
		thread.start()
		thread.join()
	
	def __init__(self):
		super().__init__()
		
		self.set_breakfast()
		
		self.setObjectName(u"MainWindow")
		self.setWindowTitle(self.tr(u"Breakfast"))
		self.setWindowIcon(QIcon("://breakfast.ico"))
		self.setFixedSize(465, 485)
		
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName(u"centralwidget")
		
		self.recipeButton = QCommandLinkButton(self.tr(u"Next Recipe"), self.centralwidget)
		self.recipeButton.setObjectName(u"recipeButton")
		self.recipeButton.setGeometry(QRect(330, 410, 121, 41))
		font = QFont()
		font.setPointSize(12)
		self.recipeButton.setFont(font)
		self.recipeButton.clicked.connect(self.newRecipe)
		
		self.breakfastTitleLabel = QLabel(self.tr(u"Breakfast Recipe:"), self.centralwidget)
		self.breakfastTitleLabel.setObjectName(u"breakfastTitleLabel")
		self.breakfastTitleLabel.setGeometry(QRect(0, 10, 465, 61))
		self.breakfastTitleLabel.setFont(QFont("Segoe UI", 14))
		self.breakfastTitleLabel.setAlignment(Qt.AlignCenter)
		
		self.breakfastLabel = QLabel(self.tr(self.breakfast["name"]), self.centralwidget)
		self.breakfastLabel.setObjectName(u"breakfastLabel")
		self.breakfastLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.breakfastLabel.setGeometry(QRect(0, 60, 465, 70))
		self.breakfastLabel.setFont(QFont("Segoe UI", 16, QFont.Bold))
		self.breakfastLabel.setAlignment(Qt.AlignCenter)
		self.breakfastLabel.setWordWrap(True)
		
		self.scrollArea = QScrollArea(self.centralwidget)
		self.scrollArea.setObjectName(u"scrollArea")
		self.scrollArea.setGeometry(QRect(40, 140, 381, 261))
		self.scrollArea.setWidgetResizable(True)
		
		self.recipeScrollArea = QWidget()
		self.recipeScrollArea.setObjectName(u"recipeScrollArea")
		self.recipeScrollArea.setGeometry(QRect(0, 0, 379, 259))
		
		self.verticalLayout_2 = QVBoxLayout(self.recipeScrollArea)
		self.verticalLayout_2.setObjectName(u"verticalLayout_2")
		
		self.durationLabel = QLabel(self.tr(f"Cook Time: {self.breakfast['duration']} minutes"))
		self.durationLabel.setObjectName(u'durationLabel')
		self.durationLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.durationLabel.setFont(QFont("Segoe UI", 12))
		self.verticalLayout_2.addWidget(self.durationLabel)
		
		self.ingredientsTitleLabel = QLabel(self.tr(u"Ingredients:"), self.recipeScrollArea)
		self.ingredientsTitleLabel.setObjectName(u"ingredientsTitleLabel")
		self.ingredientsTitleLabel.setFont(font)
		self.ingredientsTitleLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.verticalLayout_2.addWidget(self.ingredientsTitleLabel)
		
		self.ingredientsLabel = QLabel(self.recipeScrollArea)
		self.ingredientsLabel.setObjectName(u"ingredientsLabel")
		self.ingredientsLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		font3 = QFont()
		font3.setPointSize(11)
		self.ingredientsLabel.setFont(font3)
		self.populateIngredients()
		self.verticalLayout_2.addWidget(self.ingredientsLabel)
		
		self.directionsTitleLabel = QLabel(self.tr(u"Directions:"), self.recipeScrollArea)
		self.directionsTitleLabel.setObjectName(u"directionsTitleLabel")
		self.directionsTitleLabel.setFont(font)
		self.verticalLayout_2.addWidget(self.directionsTitleLabel)
		
		self.directionsLabel = QLabel(self.tr(self.breakfast["directions"]), self.recipeScrollArea)
		self.directionsLabel.setObjectName(u"directionsLabel")
		self.directionsLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.directionsLabel.setWordWrap(True)
		self.directionsLabel.setFont(font3)
		self.directionsLabel.setIndent(30)
		
		self.verticalLayout_2.addWidget(self.directionsLabel)
		
		self.scrollArea.setWidget(self.recipeScrollArea)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QMenuBar(self)
		self.menubar.setObjectName(u"menubar")
		self.menubar.setGeometry(QRect(0, 0, 462, 22))
		self.setMenuBar(self.menubar)
		
		self.show()
	
	def populateIngredients(self):
		z = ""
		
		for i in self.breakfast["ingredients"]:
			z += "<ul><li>" + i.title() + "</li></ul>"
		
		self.ingredientsLabel.setText(z)
	
	@Slot()
	def newRecipe(self):
		self.set_breakfast()
		
		with self.breakfast as breakfast:
			ing = ""
			
			for i in breakfast["ingredients"]:
				ing += f"<ul><li>{i.title()}</li></ul>"
			
			self.breakfastLabel.setText(breakfast["name"])
			self.durationLabel.setText(f"Cook Time: {breakfast['duration']} minutes")
			self.ingredientsLabel.setText(ing)
			self.directionsLabel.setText(breakfast["directions"])


if __name__ == '__main__':
	import sys
	import ctypes
	
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
		"alice.BreakfastApp"
	)  # So the window icon shows up on the taskbar
	
	app = QApplication(sys.argv)
	window = BreakFastWindow()
	
	sys.exit(app.exec())
 
