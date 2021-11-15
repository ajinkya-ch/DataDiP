'''was a test script to evaluate for DP in images'''
import cv2
import numpy as np
import numpy as np
from diffprivlib.mechanisms import Laplace
from diffprivlib.mechanisms import Gaussian
import random
import png
def privateImage(filename, eppsilon):
#read image (uploaded image) and other params
    img = cv2.imread(f"files/{filename}")
    params_list= eppsilon
    num_mech_choice=random.randint(1,2)
    local_epsilon = float(params_list[0])
    sensitivity = float(params_list[1]) 
    delta_val = float(params_list[2])

    #convert to floats
    img = np.array(img).astype(np.float)
    #normalizing data between 0 and 1 so that each pixel value has a value between 0 and 1. (0-254->0-1)
    img -= np.mean(img, axis=0)  
    img /= np.std(img, axis=0)

    imagenoise(img, num_mech_choice, local_epsilon, sensitivity, delta_val)

    
#noise addig function
def imagenoise(img, num_mech_choice, local_epsilon, sensitivity, delta_val):
    if num_mech_choice==1:
        x = Laplace(epsilon=local_epsilon, delta=delta_val, sensitivity=sensitivity)
    else:    
        x = Gaussian(epsilon=local_epsilon, delta=delta_val, sensitivity=sensitivity)
        
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            for k in range(0,img.shape[2]):
                new = x.randomise(img.item(i,j,k)) 
                img.itemset((i,j,k),new)
    # print(img)
    cv2.imshow('blur',img)
    cv2.waitKey(0)
    # png.from_array(img, mode="L").save("/files/foo.png") # works
    # img = cv2.convertScaleAbs(img, alpha=(255.0)
    

    # cv2.imwrite('static/fooo.jpg',img*255)
    # cv2.waitKey(0)


