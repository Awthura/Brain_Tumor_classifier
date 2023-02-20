import sys, asyncio

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QApplication,
	QHBoxLayout,
	QLabel,
	QMainWindow,
	QSplashScreen,
	QVBoxLayout,
	QWidget,
	QSlider,
	QPushButton
)
from PyQt6.QtGui import QPixmap

class CustomSlider(QWidget):
	def __init__(self, label, func, minmax=[0, 100]):
		super(CustomSlider, self).__init__()

		layout = QVBoxLayout()
		
		self.l1 = QLabel(label)
		self.l1.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
		layout.addWidget(self.l1)
		
		self.sl = QSlider(Qt.Orientation.Horizontal)
		self.sl.setMinimum( minmax[0] )
		self.sl.setMaximum( minmax[1] )
		self.sl.setValue( int( (minmax[0]+minmax[1])/2 ) )
		self.sl.setTickInterval(1)
		
		layout.addWidget(self.sl)
		self.sl.sliderReleased.connect(func)
		self.setLayout(layout)

class CustomImage(QWidget):
	def __init__(self, path, scaledContent=False):
		super(CustomImage, self).__init__()

		layout = QVBoxLayout()
		
		self.img = QLabel(self)
		pixmap = QPixmap(path)
		self.img.setPixmap(pixmap)
		self.img.setScaledContents(scaledContent)
		
		layout.addWidget(self.img)
		self.setLayout(layout)

class ImageWindow(QMainWindow):
	def __init__(self, custom_img, parent=None, title="Window"):
		super(ImageWindow, self).__init__(parent)

		self.setWindowTitle(title)

		imglayout = QVBoxLayout()
		imglayout.addWidget(custom_img)
		
		# Central Widget #
		widget = QWidget()
		widget.setLayout(imglayout)
		self.setCentralWidget(widget)

		

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Brain Tumor App")

		# Creating Layouts #
		pagelayout = QHBoxLayout()
		sliderlayout = QVBoxLayout()

		# Populating Slider Layout #
		self.slider0 = CustomSlider('Entropy', self.sliderfunc)
		sliderlayout.addWidget(self.slider0)

		self.slider1 = CustomSlider('Homogeneity', self.sliderfunc)
		sliderlayout.addWidget(self.slider1)
		
		sliderlayout.addStretch()
		
		self.plabel = QLabel('Brain Tumor : Positive \nPrecicion : 92%')
		self.plabel.setAlignment(Qt.AlignmentFlag.AlignBottom)
		sliderlayout.addWidget(self.plabel)

		self.stats = ImageWindow(CustomImage("res/Visualizations_ss.png"), self, "Stats")

		def stats_window ():
			self.stats.show()

		self.statbtn = QPushButton('Stats')
		self.statbtn.clicked.connect(stats_window)
		sliderlayout.addWidget(self.statbtn)

		self.heatmap = ImageWindow(CustomImage("res/Correlation_plot_ss.png"), self, "Heatmap")

		def heatmap_window ():
			self.heatmap.show()
		
		self.heatbtn = QPushButton('Heatmap')
		self.heatbtn.clicked.connect(heatmap_window)
		sliderlayout.addWidget(self.heatbtn)

		pagelayout.addLayout(sliderlayout)

		# Creating Tumor Image #
		self.tumorimg = CustomImage('data/BrainTumor/Image3.jpg', True)

		pagelayout.addWidget(self.tumorimg, 2)

		# Central Widget #
		widget = QWidget()
		widget.setLayout(pagelayout)
		self.setCentralWidget(widget)

		self.sliderfunc()

	def sliderfunc (self):

		def lerp(a: float, b: float, t: float) -> float:
			return (1 - t) * a + t * b

		# Get slider values
		s_entropy =    lerp( nmdl.df.min()['Entropy'], nmdl.df.max()['Entropy'], float(self.slider0.sl.value()/100) )
		s_homogenity = lerp( nmdl.df.min()['Homogeneity'], nmdl.df.max()['Homogeneity'], float(self.slider1.sl.value()/100) )

		# What I am doing here is heresy but I couldnt find a clever way to get two closest values with minimal cpu time
		entropy_closest =    nmdl.df.iloc[(nmdl.df['Entropy']-s_entropy).abs().argsort()[0:300]]
		homogenity_closest = nmdl.df.iloc[(entropy_closest['Homogeneity']-s_homogenity).abs().argsort()[:1]]
		df_closest = homogenity_closest
		
		# Update Slider Label
		self.slider0.l1.setText('Entropy: {0:.3f}'.format(s_entropy))
		self.slider1.l1.setText('Homogeneity: {0:.3f}'.format(s_homogenity))

		# Convert DF to a list and predict
		dfp = df_closest
		dfp.drop(dfp.columns[[0, 1]], axis=1, inplace=True)
		dfp = dfp.values.tolist()[0]
		y_pred = nmdl.predict_inst(dfp, mdl)

		# Update the label and image
		result = 'Positive' if y_pred else 'Negative'
		cm = nmdl.plotCm(data, mdl)
		TP = cm[0][0]
		FP = cm[0][1]
		FN = cm[1][0]
		PV = TP/(TP+FP)
		recall = TP/(TP+FN)

		txt = 'Brain Tumor : {0} \nAccuracy : {1:0.3f}%\nPrecicion : {2:0.3f}%\nRecall : {3:0.3f}%'.format(result, acc*100, PV*100, recall*100)
		self.plabel.setText(txt)
		txt = 'data/BrainTumor/Image{}.jpg'.format( df_closest.index.item()+1 )
		pixmap = QPixmap(txt)
		self.tumorimg.img.setPixmap(pixmap)

mdl = 0
acc = 0
nmdl = 0
data = 0

async def import_model():
	global mdl, acc, nmdl, data
	from model import Mdl
	nmdl = Mdl()
	data = nmdl.preprocess()
	mdl, acc = nmdl.train(data)

async def main():
	app = QApplication(sys.argv)
	pixmap = QPixmap('res/Splash.jpg')
	splash = QSplashScreen(pixmap)
	splash.show()
	await import_model()
	splash.hide()
	window = MainWindow()
	# window.resize(872, 745)
	window.show()

	app.exec()

asyncio.run(main())