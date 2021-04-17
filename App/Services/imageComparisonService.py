import cv2
import csv
import time, datetime
import numpy as np
import sys, os
from ..Helpers import telegramBot
from ..Constants import LiveStreamConstant

class imageComparison(object):
    def __init__(self,outputFileName):
        self.data = []
        self.frames = []
        self.outputFileName = outputFileName
        self.initOutputFile()
        self.bot = telegramBot.telegramBot()
        self.url = str(os.environ['DOMAIN_APP']) + '/live/v/'
        self.rate = int(os.environ['RATE'])
            
    def setData(self, data):
        self.frames = []
        self.data = data

    def captureImage(self):
        
        for video in self.data:
            try:
                start_time = time.time()
                cap = cv2.VideoCapture(video['output_url_hls'])
                #total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # get its total frame count
                #print('Total Frame: ', total)
                print('Time:', time.time() - start_time)
                
                #time.sleep(5)
                if (cap.isOpened() == False):
                    print('!!! Unable to open URL')
                    sys.exit(-1)
            
                # read one frame
                ret, frame = cap.read()
                
                # Export image
                cv2.imwrite(str(video['video_id']) + '.jpg' ,frame)
                
                infoDict = {
                    'video_id': video['video_id'],
                    'frame': np.asanyarray(frame)
                }
                
                self.frames.append(infoDict)
            
            except Exception as e: 
                    print(e)    
            

    # Initialize 
    def initOutputFile(self):
        # Creating new file and setting the headers
        with open(self.outputFileName, 'w') as newcsv:
            writer = csv.writer(newcsv, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['image1', 'image2', 'similarity(%)', 'elapsed', 'created at'])

    # Appending to the results.csv file with the paths, similiarity index, and time elapsed for the comparison
    def exportOutput(self, path1, path2, orb_similarity, elapsed_orb, created_at):
        with open(self.outputFileName, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([path1, path2, orb_similarity, elapsed_orb, created_at])
            
    # Necessary in order for SSIM to function. Both images must have the same resolution
    def scaleImages(self, image1, image2, width=640, height=480):
        
        ## Setting constant dimensions, with arbitrary default values of 640x480
        dim = (width, height)
        
        image1 = cv2.resize(image1, dim)
        image2 = cv2.resize(image2, dim)
    
        return image1, image2
    
    # Works well with images of different dimensions
    def orbSim(self, img1, img2):
      # SIFT is no longer available in cv2 so using ORB
      start_time = time.time()
      orb = cv2.ORB_create()
    
      # detect keypoints and descriptors
      kp_a, desc_a = orb.detectAndCompute(img1, None)
      kp_b, desc_b = orb.detectAndCompute(img2, None)
    
      # define the bruteforce matcher object
      bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
      #perform matches. 
      matches = bf.match(desc_a, desc_b)
      #Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
      similar_regions = [i for i in matches if i.distance < 50]  
      elapsed = time.time() - start_time
      if len(matches) == 0:
        return 0, elapsed
      return (len(similar_regions) / len(matches)) * 100, elapsed
  
    # Compare two images with similarity
    def compareImages(self):
        
        # capture image
        self.captureImage()
        bot = telegramBot.telegramBot()
        
        i = 0
        messages = ""
        flag = False
        
        if len(self.frames) < 2 :
            print('Data is empty')
        else:
            for x in self.frames[:len(self.frames)-1]:
                i+=1
                for y in self.frames[i:]:
            
                    videoId1, videoId2 = x['video_id'], y['video_id']
                    # numpy.ndarra
                    image1, image2 = self.scaleImages(x['frame'] , y['frame'])
                    
                    resized_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                    resized_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            
                    orbSimilarity, elapsed = self.orbSim(resized_image1, resized_image2)  #1.0 means identical. Lower = not similar
                    
                    if orbSimilarity > self.rate:
                        flag = True
                        messages += "⚠️Warning: "+ self.url + str(videoId1)+" | "+ self.url + str(videoId2)+ " Có khả năng giống nhau là " + str(orbSimilarity)[:2] + "% \n"
                        
                    print("Similarity using ORB is: ", orbSimilarity, "\nElapsed:", elapsed)
                    
                    self.exportOutput(videoId1, videoId2, orbSimilarity, elapsed, datetime.datetime.now())
        
        if flag is True:
            self.bot.telegramBotSendText(messages)
                