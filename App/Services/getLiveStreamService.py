from ..Constants import LiveStreamConstant
import requests
import json
import os

class getLiveStream():
    
    def __init__(self):
        self.__url = str(os.environ['DOMAIN_API']) + '/livestreaming/v3/videos/live'
        
    def getInfo(self):
        print(self.__url)
        infoArr = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(self.__url, headers=headers)
        data = json.loads(response.text).get('data')
        
        for d in data:
            
            video_dict = {
                'video_id': d['id'],
                'output_url_hls': d['output_url_hls']
            }
            
            infoArr.append(video_dict)
            
        return infoArr
