from PIL import Image
from PIL import ImageEnhance
import cv2
import numpy as np
import operator
import os
import glob
import time
import shutil
    
import threading
import multiprocessing

    
def enhance_contrast(file):
    #Opening the file
    image = Image.open(file) # Compatible with the Pillow Library
    #Enhancing Contrast
    image1 = ImageEnhance.Contrast(image).enhance(2) # contrast enhancement using Pillow Library
    width,height = image.size    
    right=(width*1)/3
    bottom = right
    image1 = image1.crop((0,0,right,height))
    #Saving image Temporarly(Optional)
    image1.save("./temp/"+file.split(" ")[1]+"image1.jpg","JPEG");

def binarization(file):
     #Opening the file
    image = Image.open(file) # Compatible with the Pillow Library
    #Binarization
    image2=image.convert('1')
    
    width,height = image.size
    #Cropping the Image
    right=(width*2)/3
    left=(width*1)/3
    bottom = right
    image2 = image2.crop((left,0,right,height))
    #Saving image Temporarly(Optional)
    image2.save("./temp/"+file.split(" ")[1]+"image2.jpg","JPEG");


def houge_transform(file):
    #Hog Transformation - Using OpenCV
    img=cv2.imread(file) # Opening the file for hog transformation, compatible with OpenCv
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)    
        cv2.imwrite("./temp/"+file.split(" ")[1]+"image3.jpg",img)
    
    image3 = Image.open("./temp/"+file.split(" ")[1]+"image3.jpg")
    #Opening the file
    image = Image.open(file) # compatible with the Pillow Library
    width,height = image.size
    #Cropping the Image
    left=(width*2)/3
    image3 = image3.crop((left,0,width,height))
    #Saving image Temporarly(Optional)
    image3.save("./temp/"+file.split(" ")[1]+"image3.jpg","JPEG");


def merger(file):
    #Merging the 3 Images
    images = map(Image.open, ["./temp/"+file.split(" ")[1]+"image1.jpg", "./temp/"+file.split(" ")[1]+"image2.jpg", "./temp/"+file.split(" ")[1]+"image3.jpg"])

    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    new_im.save("./final_images/"+file.split(" ")[1],"JPEG")

    

def imgprocess_with_thread(file):
    
    #Stage1 We are creating 3 threads
        #Initializing Threads
    t1= threading.Thread(target=enhance_contrast,args=(file,))
    t2= threading.Thread(target=binarization,args=(file,))
    t3= threading.Thread(target=houge_transform,args=(file,))
                      
                      
        #Starting Threds
    t1.start()
    t2.start()
    t3.start()
        #Waiting for the threads to complete the task
    t1.join()
    t2.join()
    t3.join()
    
    #Stage2
    merger(file)

def imgprocess_without_thread(file):
    #Stage1
    enhance_contrast(file)
    binarization(file)
    houge_transform(file)
                      
    #Stage2
    merger(file)


def imgprocess_with_multiprocess(file):
    
    #Stage1 We are creating 3 processes
        #Initializing Threads
    p1= multiprocessing.Process(target=enhance_contrast,args=(file,))
    p2= multiprocessing.Process(target=binarization,args=(file,))
    p3= multiprocessing.Process(target=houge_transform,args=(file,))
                      
                      
        #Starting Process
    p1.start()
    p2.start()
    p3.start()
        #Waiting for the processes to complete the task
    p1.join()
    p2.join()
    p3.join()
    
    #Stage2
    merger(file)
    

    
if __name__ == '__main__':
    #creating the directories if they do not exist
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("final_images"):
        os.mkdir("final_images")
    #Without Threading
    t = time.time()
    for file in  glob.glob("./images/*.jpg"):
        imgprocess_without_thread(file)
    print ("Successsfully Done Without Thread in :",time.time()-t)

    #With Threading
    t = time.time()
    for file in  glob.glob("./images/*.jpg"):
        imgprocess_with_thread(file)
    print ("Successsfully Done With Multi-Threading in :",time.time()-t)

    #With MultiProcessing
    t = time.time()
    for file in  glob.glob("./images/*.jpg"):
        imgprocess_with_multiprocess(file)
    print ("Successsfully Done With Mult-Processing in :",time.time()-t)

    #Cleaning any temp file Used
    shutil.rmtree("./temp") 

    
    
        

    

   
           
    
    
