from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv,find_dotenv
from googleapiclient.discovery import build

load_dotenv(find_dotenv())


api_key=os.getenv("GOOGLE_API_KEY")

youtube=build('youtube','v3',developerKey=api_key)

@csrf_exempt
def get_video_id(link:str)->str:
    i=link.find("watch?v=")
    link=link[i:]
    return link[8:]
@csrf_exempt
def get_data_1(videoid:str,pagetoken=None):
    request=youtube.commentThreads().list(part='snippet',videoId=videoid,maxResults=100,pageToken=pagetoken,textFormat='plainText')
    response=request.execute()
    return response
@csrf_exempt
def process_response(response:dict)->tuple:
    items=response['items']
    
    data=[]
    for i in items:
        data.append((i['snippet']['topLevelComment']['snippet']['authorDisplayName'],i['snippet']['topLevelComment']['snippet']['textDisplay']))
    try:
       next_token=response['nextPageToken']
    except:
        return
    return(next_token,data)

@csrf_exempt
def get_data(video_link:str,ans:list,pagetoken=None):
    try:
        videoid=get_video_id(video_link)
        res=get_data_1(videoid,pagetoken)
        data=process_response(res)
        pagetoken=data[0]
        for comment in data[1]:
            if len(ans)>1000: return
            ans.append((comment[0],comment[1]))
        get_data(video_link,ans,pagetoken)
    except Exception as e:
        return