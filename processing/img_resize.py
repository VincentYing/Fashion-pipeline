import PIL
from PIL import Image


img = Image.open('n09835506_9987.jpg')
img = img.resize( (224,224), Image.ANTIALIAS)
img.save('resized.jpg')
