import numpy as np
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
import subprocess
from PIL import ImageEnhance

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def combined_display(image, matte):
    """
    # calculate display resolution
    w, h = image.width, image.height
    rw, rh = 800, int(h * 800 / (3 * w))
    
    # obtain predicted foreground
    image = np.asarray(image)
    if len(image.shape) == 2:
        image = image[:, :, None]
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    elif image.shape[2] == 4:
        image = image[:, :, 0:3]
    matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2)
    print(type(matte))
    foreground = Image.fromarray(np.uint8(image * matte + np.full(image.shape, 255) * (1 - matte)))

    result = Image.fromarray(np.uint8(np.dstack((foreground, Image.fromarray(matte)))*255))
    
    im_f = Image.new(mode='RGB', size=(image.shape[1],image.shape[0]))
    im_f.paste(foreground, (0,0,foreground.size[0],foreground.size[1]))
    im_f.putalpha(255)
    im_f.show()
    print(has_transparency(im_f))
    fff = Image.new('RGBA', foreground.size, (0,0,0,0))
    result = Image.composite(im_f, fff, im_f)
    
    # combine image, foreground, and alpha into one line
    combined = np.concatenate((image, foreground, matte * 255), axis=1)
    #combined = Image.fromarray(np.uint8(combined)).resize((rw, rh))
    """

    image_with_transparency = np.dstack((image, matte))

    return Image.fromarray(image_with_transparency)

# visualize all images

#open image dialog (choose image)
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

#Move image for MODnet
##use original image
os.replace(file_path, "./MODnet/demo/image_matting/colab/input/1.jpg")
##Pre-processing image
#image = Image.open(file_path)
#image = ImageEnhance.Sharpness(image).enhance(1.3)
#image.save("./MODnet/demo/image_matting/colab/input/1.jpg")

#Run MODnet
subprocess.call(['sh', './MODnet/run_MODnet.sh'])

input_folder = "./MODnet/demo/image_matting/colab/input"
output_folder = "./MODnet/demo/image_matting/colab/output"
image_names = os.listdir(input_folder)
for image_name in image_names:
  matte_name = image_name.split('.')[0] + '.png'
  image = Image.open(os.path.join(input_folder, image_name))
  matte = Image.open(os.path.join(output_folder, matte_name)).convert('L')
  im = combined_display(image, matte)
  im.show()
  print(image_name, '\n')
