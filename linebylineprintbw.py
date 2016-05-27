import printer
from numpy import cos, sin
from numpy import array, linspace
from scipy import misc
from time import sleep
import matplotlib.pyplot as plt

from PIL import Image

col = Image.open('girl_line_drawing.jpg')
gray = col.convert('L')
bw = gray.point(lambda x: 0 if x<240 else 255, '1')	
bw.save("result_bw.png")

I = misc.imread('result_bw.png',flatten='True')
print I.shape
S = I.shape
# M = (I[:,:,0] + I[:,:,1] + I[:,:,2] )/3

plt.imshow(I,cmap='Greys')


pressed_ = False
D = I
printer.home()
while D.any():
	for y in xrange(S[0]):
		for x in xrange(S[1]):
			if D[y,x] != 0:
				if pressed_:
					printer.release(100)
					pressed_ = False
				pass
			else:
				printer.moveto( (x,y) )
				if not pressed_:
					printer.press(400)
					pressed_ = True
				D[y,x] = 0;

printer.close()


# plt.show()



