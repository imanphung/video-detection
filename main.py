from App.Services.imageComparisonService import *
from App.Services.getLiveStreamService import *
from App.Constants import LiveStreamConstant
import os
         
if __name__ == "__main__":

    #init objects
    getLiveStream = getLiveStream()
    imageComparison = imageComparison(LiveStreamConstant.__OUTPUT__)

    while bool(os.environ['RUN_DETECTION']) == True:  
        # get livestream info
        liveStreamInfo = getLiveStream.getInfo()
        
        # initialize image comparison
        imageComparison.setData(liveStreamInfo)
        
        # run compare all images
        imageComparison.compareImages()

        time.sleep(int(os.environ['DETECTION_TIME']))

    #### For Debug ####
        
    # while LiveStreamConstant.__RUN_DETECTION__ == True:
    #     liveStreamInfo = getLiveStream.getInfo()
        
    #     # initialize image comparison
    #     imageComparison.setData(liveStreamInfo)
        
    #     # run compare all images
    #     imageComparison.compareImages()
        
    #     time.sleep(900)
        