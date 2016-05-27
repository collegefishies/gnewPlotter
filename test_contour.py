import painter
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image

for fno in range(1,5):
	I = misc.imread('tree/contour%d.png' % fno,flatten='True')
	print I.shape
	D = I
	plt.imshow(I,cmap='Greys')
	# plt.show()
	pressed_ = False
	painter.setImage(D)
	painter.drawBorder()
	painter.drawImage(-1)
	print 'Done'
# D = misc.imread('pdf/pdf-1.png',flatten='True')
# painter.setImage(D)
# # painter.drawBorder()
# painter.drawImage(-1)