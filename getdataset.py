!pip install youtube_dl
!pip install ffmpeg-python 
!pip install moviepy --upgrade

import os
from sys import stdout
import moviepy.editor as mp
import pandas as pd
import time
import youtube_dl
import ffmpeg
import time
from PIL import Image

class GetDataset:

  Dataset = ""
  AudioFolder = ""
  PhotoFolder = ""
  VideoFolder = "videos"
  Batch=1
    
  def extractAudio(self,vid_path): #extract audio from a video
    try:
      clip=mp.VideoFileClip(vid_path)
      frameName=vid_path[vid_path.find("/")+1:-4]
      audioName=vid_path[vid_path.find("/")+1:-4]
      outputPath = self.AudioFolder+"/"+audioName+".wav"   
      clip.audio.write_audiofile(outputPath, logger=None)
      clip.close()
    except Exception as e:
      print(e)
      clip.close()
      with open ("errorAudios.txt","a+") as err:
        err.write("Vid: " + frameName + " Error Extracting Audio \n")
      

  def extractFrame(self,vid_path):
    try:
      clip=mp.VideoFileClip(vid_path)
      frameName=vid_path[vid_path.find("/")+1:-4]
      imgarray = clip.get_frame(1)
      data = Image.fromarray(imgarray) 
      data.save(self.PhotoFolder+"/"+frameName+".png")
      clip.close()
    except :
      clip.close()
      with open ("errorFrames.txt","a+") as err:
        err.write("Vid: " + frameName + " Error Extracting Frame \n")

  def setDatasetCSV(self,filename):
    self.Dataset = filename

  def setAudioOutputFolder(self,foldername):
    self.AudioFolder = foldername
    try:
      if not os.path.exists(self.AudioFolder):
         os.mkdir(self.AudioFolder)
    except:
     stdout.write("\r[!]Couldn't Make New Folder For Audios")
     pass     
         

  def setPhotoOutputFolder(self,foldername):
    self.PhotoFolder = foldername
    try:
      if not os.path.exists(self.PhotoFolder):
        os.mkdir(self.PhotoFolder)
    except:
     stdout.write("\r[!]Couldn't Make New Folder For Photos")
     pass
    
  def isAlreadyConverted(self,vidName):
    audioname=vidName[:-4]+".wav"
    photoname=vidName[:-4]+".png"
    try:
      if (audioname in os.listdir(self.AudioFolder)):
         if (vidName in os.listdir(self.PhotoFolder)):
             return 1
      return 0
    except:
      return 0
    
  

  def convertVideos(self):
    
      vids_dir = "videos"
      if not os.path.exists(vids_dir):    
             os.mkdir(vids_dir)

      train_set = pd.read_csv(self.Dataset,names=["video_ID", "start_t", "end_t","x","y"]) 
        
      
      if('stopPos.txt' in os.listdir() ):
        with open ('stopPos.txt','r') as stop:
           startpos=int(stop.read()[0])+1
      else:
           startpos=0
        
      endpos=self.Batch
      numberconverted=0
      startpos=0
      
      #for i in range(len(train_set)):
      for i in range(startpos,endpos):
        
        numberconverted += 1
        video_ID= train_set.iloc[i]['video_ID']
        start_t,end_t  = train_set.iloc[i]['start_t'],train_set.iloc[i]['end_t']
        video_name=video_ID+".mp4"


       # if(self.isAlreadyConverted(video_name) == 0): #avoid downloading same video again

        #Download Video:
        try:
            stdout.write("\n[+]Downloading video: %s" % video_ID)
            start_t_f = time.strftime("%H:%M:%S", time.gmtime(start_t))  #hh:mm:ss
            end_t_f   = time.strftime("%H:%M:%S", time.gmtime(end_t))  #hh:mm:ss        
            duration = end_t -start_t
            #print(duration)    
            downloadstate=Youtube.downloadvideo(video_ID,start_t_f,duration)
            print(downloadstate)
        except Exception as e:
            print(e)
            stdout.write("\r[!]Couldn't Download: %s" % video_ID)
            with open ('error.txt','a+') as err:
              err.write(video_ID + " Download Failed \n")
            continue

        if (downloadstate[-5:]!="DONE!"):
          with open ('error.txt','a+') as err:
              err.write(video_ID + " Download Failed \n")
          continue
        
        stdout.write("\b\r[+]Converting video: %s" % video_ID)
                
        vid_path = vids_dir + "/" + video_ID + ".mp4"  # Video Location 
        
        # extract audio and frame :
        try:
           self.extractAudio(vid_path)
           self.extractFrame(vid_path)
           stdout.write("\t[!]Video %s converted " % video_ID)
        except Exception as e:
           print(e)
           stdout.write("\t[!]Video %s not found " % video_ID)

        try:   
          os.remove(os.path.join("videos", video_ID +'.mp4'))
        except:
          pass

        
        if (numberconverted == 5):  # number of videos to download and convert every single run
          with open ('stopPos.txt','w') as stop:
              stop.write(str(startpos+numberconverted))
              break   

          
 
class Youtube:
  
 def downloadvideo(video_ID,start_t,end_t):

    yt_base_url = 'https://www.youtube.com/watch?v='
    
    
    yt_url = yt_base_url + video_ID
    
    
    outputfile= os.path.join("videos", video_ID +'.mp4')

    ydl_opts = {
        'format': '22/18',
        'quiet': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            download_url = ydl.extract_info(url=yt_url, download=False)['url']
    except:
        return_msg = '{}, ERROR (youtube)!'.format(video_ID)
        return return_msg
    try:
      (
        ffmpeg
        .input(download_url, ss=start_t, t=end_t)
        .output(outputfile, format='mp4', r=25, vcodec='libx264',crf=18, preset='veryfast', pix_fmt='yuv420p', acodec='aac', audio_bitrate=128000,strict='experimental')
        .global_args('-y')
        .global_args('-loglevel', 'trace')
        .run(capture_stdout=True, capture_stderr=True)
      )
    except:
        return_msg = '{}, ERROR (ffmpeg)!'.format(video_ID)
        return return_msg

    return '{}, DONE!'.format(video_ID)
    

#print(downloadvideo("307DK9nGQhw","00:01:30","00:01:33"))

                      
x= GetDataset()
x.Batch=5
x.setDatasetCSV("avspeech_train.csv")
x.setAudioOutputFolder("audios")
x.setPhotoOutputFolder("photos")
x.convertVideos()


