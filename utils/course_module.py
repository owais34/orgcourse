from utils.json_utils import Jsoner
from utils.folder_parser import scan_sub_dirs,scan_videofiles
from utils.repository_module import Repository
import vlc 
import metadata.setup
import ffmpeg
import os

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
        else:
            self.directoryPath = dictForm.get("directoryPath")
            self.subModuleList = []
            for subModule in dictForm.get("subModuleList"):
                self.subModuleList.append(SubModule(dictForm=subModule))
            self.moduleIndex = dictForm.get("moduleIndex")
            self.stoppedAtTime = dictForm.get("stoppedAtTime")
            self.videoIndex = dictForm.get("videoIndex")
            

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
    
    def getCurrentPlayable(self) -> vlc.MediaPlayer:
        mediaPlayerInstance = vlc.MediaPlayer(self.subModuleList[self.moduleIndex].videoList[self.videoIndex].path)
        mediaPlayerInstance.set_time(self.stoppedAtTime)
        return mediaPlayerInstance



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
        else:
            self.directoryPath = dictForm.get("directoryPath")
            self.name = dictForm.get("name")
            self.videoList = []
            for video in dictForm.get("videoList"):
                self.videoList.append(VideoFile(dictForm=video))
               
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
        for i in range(len(self.courseList)):
            courseName = self.courseList[i].directoryPath.split(os.sep)[-1]

            print("  "+str(i)+": "+courseName)

    
        
        