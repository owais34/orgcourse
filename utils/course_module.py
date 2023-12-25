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
            self.subModuleList = self.createModule()
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
            

    def createModule(self) -> list:
        subModuleList = []
        subModuleDirectoryList = scan_sub_dirs(self.directoryPath)
        if subModuleList.__len__ == 0:
            dummySubmodule = SubModule(directoryPath=None,name="dummysubmodule")
            subModuleList.append(dummySubmodule)
        else:
            for subModuleDirectory in subModuleDirectoryList:
                subModuleList.append(SubModule(subModuleDirectory["path"],subModuleDirectory["name"]))
        
        return subModuleList
    
    # def getCurrentPlayable(self) -> vlc.MediaPlayer:
    #     mediaPlayerInstance = vlc.MediaPlayer(self.subModuleList[self.moduleIndex].videoList[self.videoIndex].path)
    #     mediaPlayerInstance.set_time(self.stoppedAtTime)
    #     return mediaPlayerInstance



class SubModule:
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
            




class VideoFile:

    def __init__(self,path=None,name=None,dictForm = None):
        if dictForm == None:
            self.path = path
            self.name = name
            self.duration = self.getDurationMs()
            self.durationPlayed = 0

        else:
            self.path = dictForm.get("path")
            self.name = dictForm.get("name")
            self.duration = dictForm.get("duration")
            self.durationPlayed = dictForm.get("durationPlayed")

    def getDurationMs(self) -> int:
        durationMs = int(float(ffmpeg.probe(self.path)["streams"][0]["duration"]) * 1000)
        return durationMs
    
    def getThumbnailImage(self) -> str:
        subprocess.call([
            "ffmpeg", "-ss", "00:00:00.01","-i", "%s" % self.path, "-vf", "'scale=250:250:force_original_aspect_ratio=decrease'",
              "-vframes", "1", "%s" %metadata.setup.temporary_thumbnail_name
        ])




class CourseManager(Jsoner,Repository):
    def __init__(self) -> None:
        dictForm = self.loadFromRepo()
        if (dictForm == None):
            self.courseList = []
            self.persistChanges(self.getJson())
        else:
            self.courseList = []
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
            courseInfoDict["duration"]= ""
            if hrs != 0:
                courseInfoDict["duration"]=courseInfoDict["duration"]+str(hrs)+" hrs"
            if seconds!=0:
                courseInfoDict["duration"]=courseInfoDict["duration"]+str(seconds)+" seconds"
            courseInfoDict["progress"] = int(self.courseList[i].durationPlayed/self.courseList[i].duration)
            courseListTemp.append(courseInfoDict)
        return courseListTemp

            

    
        
        