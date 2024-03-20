from utils.json_utils import Jsoner
from utils.folder_parser import scan_sub_dirs,scan_videofiles
from utils.repository_module import Repository
import metadata.setup
import ffmpeg
import os
import subprocess
import shutil

class Course(Jsoner):
    #directoryPath
    #subModulesList
    #videoList
    #progress
    #totalHours
    #hoursPlayed
    #resumePoint
    #startDate
    #daysPlayed
    def __init__(self, directoryPath=None, dictForm=None):
        if dictForm == None:
            self.directoryPath = directoryPath
            self.subModuleList = self.createModuleList()
            self.moduleIndex = 0
            self.videoIndex = 0
            self.stoppedAtTime = 0
            self.duration = 0
            self.durationPlayed = 0
            for subModule in self.subModuleList:
                self.duration+=subModule.duration
                self.durationPlayed+=subModule.durationPlayed
        else:
            self.directoryPath = dictForm.get("directoryPath")
            self.subModuleList = []
            for subModule in dictForm.get("subModuleList"):
                self.subModuleList.append(SubModule(dictForm=subModule))
            self.moduleIndex = dictForm.get("moduleIndex")
            self.stoppedAtTime = dictForm.get("stoppedAtTime")
            self.videoIndex = dictForm.get("videoIndex")
            self.duration = dictForm.get("duration")
            self.durationPlayed = dictForm.get("durationPlayed")
            

    def createModuleList(self) -> list:
        subModuleList = []
        subDirectoryList = scan_sub_dirs(self.directoryPath)
        for subDirectory in subDirectoryList:
            subModuleTemporary = SubModule(subDirectory["path"],subDirectory["name"])
            if subModuleTemporary.duration != 0:
                subModuleList.append(subModuleTemporary)
        
        if len(subModuleList) == 0:
            dummySubmodule = SubModule(directoryPath=self.directoryPath,name="dummysubmodule")
            
            subModuleList.append(dummySubmodule)
        return subModuleList
    
    # def getCurrentPlayable(self) -> vlc.MediaPlayer:
    #     mediaPlayerInstance = vlc.MediaPlayer(self.subModuleList[self.moduleIndex].videoList[self.videoIndex].path)
    #     mediaPlayerInstance.set_time(self.stoppedAtTime)
    #     return mediaPlayerInstance

    def updatePlaytime(self, moduleIndex, videoIndex, currentTime):

        is_updated = self.subModuleList[moduleIndex].updatePlaytime(videoIndex, currentTime)
        if self.moduleIndex != moduleIndex or self.videoIndex != videoIndex or self.stoppedAtTime!=currentTime:
            self.moduleIndex=moduleIndex
            self.videoIndex=videoIndex
            self.stoppedAtTime=currentTime
            is_updated = True
        if is_updated:
            self.durationPlayed=0
            for subModule in self.subModuleList:
                self.durationPlayed+=subModule.durationPlayed
        
        return is_updated


class SubModule(Jsoner):
    #directoryPath
    #videoList
    def __init__(self,directoryPath=None,name=None,dictForm=None):
        if dictForm == None:
            self.directoryPath = directoryPath
            self.name = name
            self.videoList = []
            if directoryPath != None:
                self.videoList=self.setVideoList(scan_videofiles(directoryPath,metadata.setup.supported_video_formats))
            self.duration = 0
            self.durationPlayed = 0
            for video in self.videoList:
                self.duration+=video.duration
                self.durationPlayed+=video.durationPlayed
        else:
            self.directoryPath = dictForm.get("directoryPath")
            self.name = dictForm.get("name")
            self.videoList = []
            for video in dictForm.get("videoList"):
                self.videoList.append(VideoFile(dictForm=video))
            self.duration = dictForm.get("duration")
            self.durationPlayed = dictForm.get("durationPlayed")
               
    def setVideoList(self, videoFilesList: list) -> list:
        videoList = []
        for videoFile in videoFilesList:
            videoList.append(VideoFile(path=videoFile["path"],name=videoFile["name"]))
        return videoList
    
    def updatePlaytime(self, videoIndex, currentTime):
        
        is_updated = self.videoList[videoIndex].updatePlaytime(currentTime)
        if is_updated:
            self.durationPlayed = 0
            for video in self.videoList:
                self.durationPlayed+=video.durationPlayed

        return is_updated
            




class VideoFile:

    def __init__(self,path=None,name=None,dictForm = None):
        if dictForm == None:
            self.path = path
            self.name = name
            self.duration = self.getDurationMs()
            self.durationPlayed = 0
            # self.thumbNailImage = ""

        else:
            self.path = dictForm.get("path")
            self.name = dictForm.get("name")
            self.duration = dictForm.get("duration")
            self.durationPlayed = dictForm.get("durationPlayed")
            # self.thumbNailImage = dictForm.get("thumbNailImage")

    def getDurationMs(self) -> int:
        durationMs = 0
        try:
            #durationMs = int(float(ffmpeg.probe(self.path)["streams"][0]["duration"]) * 1000)
            print(ffmpeg.probe(self.path)["streams"][0])
            raw_duration = ffmpeg.probe(self.path)["streams"][0].get("duration")
            if raw_duration == None:
                raw_duration = ffmpeg.probe(self.path)["streams"][0].get("tags").get("DURATION")
            durationMs = int(float(raw_duration)*1000)
        except Exception as e:
            print(e)
            raw_duration = raw_duration.split(":")
            durationMs += int(raw_duration[0])*60*60*1000
            durationMs += int(raw_duration[1])*60*1000
            durationMs += int(float(raw_duration[2])*1000)
        finally:
            print(durationMs)
            return durationMs
    
    def getThumbnailImage(self) -> str:
        image_path = str(self.path).replace("\\","_")+".jpeg"
        # %metadata.setup.temporary_thumbnail_name
        subprocess.call([
            "ffmpeg", "-ss", "00:00:00.01","-i", "%s" % self.path, "-vf", "'scale=250:250:force_original_aspect_ratio=decrease'",
              "-vframes", "1", "%s" % image_path
        ])

        shutil.move(image_path, "./static/images")
        self.thumbNailImage = image_path

    def updatePlaytime(self, currentTime):
        if (currentTime>self.durationPlayed):
            if (currentTime>self.duration):
                self.durationPlayed=self.duration
            else:
                self.durationPlayed = currentTime
            return True
        return True
        


class CourseManager(Jsoner,Repository):
    def __init__(self) -> None:
        dictForm = self.loadFromRepo()
        if (dictForm == None):
            self.courseList = []
            self.counter = 0
            self.persistChanges(self.getJson())
        else:
            self.courseList = []
            if dictForm.get("counter")!=None:
                self.counter = dictForm.get("counter")
            else:
                self.counter = 0
            for course in dictForm.get("courseList"):
                self.courseList.append(Course(dictForm=course))

    def searchCourse(self, course) -> bool:
        if isinstance(course, Course):
            isPresent = False
            for courseItem in self.courseList:
                if courseItem.directoryPath == course.directoryPath:
                    isPresent = True
                    break
            return isPresent
        else:
            return False

    def addCourse(self, course):
        if self.searchCourse(course=course) == False:
            if isinstance(course, Course):
                self.courseList.append(course)
                self.persistChanges(self.getJson())

    def listCourses(self):
        courseListTemp = []
        for i in range(len(self.courseList)):
            courseInfoDict = {}
            courseName = self.courseList[i].directoryPath.split(os.sep)[-1]
            courseInfoDict["name"]=courseName
            courseInfoDict["id"] = i
            seconds = int(self.courseList[i].duration)/1000
            hrs = int(seconds / 3600)
            seconds = int(seconds % 3600)
            mins = int(seconds/60)
            seconds = int(seconds%60)
            courseInfoDict["duration"]= ""
            if hrs != 0:
                courseInfoDict["duration"]=courseInfoDict["duration"]+str(hrs)+" h "
            if mins!=0:
                courseInfoDict["duration"]=courseInfoDict["duration"]+str(mins)+" m "
            if seconds!=0:
                courseInfoDict["duration"]=courseInfoDict["duration"]+str(seconds)+" s "
            if self.courseList[i].duration != 0:
                courseInfoDict["progress"] = int((self.courseList[i].durationPlayed/self.courseList[i].duration)*100)
            else:
                courseInfoDict["progress"] = 0
            courseListTemp.append(courseInfoDict)
        return courseListTemp
    
    def updatePlaytime(self, data: dict):
        
        id = data.get('id')
        moduleIndex = data.get("currentModule")
        videoIndex = data.get("currentVideo")
        currentTime = int(data.get("currentTime")*1000) # in ms
        
        result = self.courseList[id].updatePlaytime(moduleIndex, videoIndex, currentTime)
        if self.counter == 0:
            self.persistChanges(self.getJson())
        self.counter = (self.counter + 1)%10

        return result

            

    
        
        