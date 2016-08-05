# -*- coding=utf-8 -*-

import cStringIO
import urllib2

import pytesseract
from PIL import Image

file = cStringIO.StringIO(urllib2.urlopen("http://www.cnshipnet.com/extend/image.php?auth=UDAEaVo3XS0KZAg%2FVDVUYFYnW2AEOAo6UWVWMQE%2FVDE%3D").read())
img = Image.open(file)
print pytesseract.image_to_string(img)