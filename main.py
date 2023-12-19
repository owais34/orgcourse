from metadata.setup import init
from utils.course_module import Course
from utils.course_module import CourseManager
import sys,time
import vlc

course_manager_master = CourseManager()

course_resumed = None


def main():
    print("*************Course Organiser****************")
    while 1>0 :
      time.sleep(0.5)  
      print("Select one of below options")
      print("1. Add a new course directory")
      print("2. List all courses")
      print("3. Select a course")
      print("4. exit")
      option = input()
      match option:
         case "1":
            addDirectory()
         case "2":
            listAllCourse()
         case "3":
            selectCourseToResume()
         case _ :
            sys.exit("App terminated")
        

      
def addDirectory():
   path_to_course = input("Enter the full path to course directory :\n")
   new_course = Course(directoryPath=path_to_course)
   if course_manager_master.searchCourse(new_course):
      print("Course already added !!")
   else:
      course_manager_master.addCourse(new_course)
      print("Course Added !!!")
   return

def listAllCourse():
   print("************* Available courses **********")
   course_manager_master.listCourses()
   print("******************************************")
   return

def selectCourseToResume():
   course_index = input("Enter the index number of course from courselist : ")
   try:
      course_index = int(course_index)
      if course_index >= len(course_manager_master.courseList):
         print(" Invalid input !!! Try again !!")
         return
      global course_resumed
      course_resumed = course_manager_master.courseList[course_index]
      mediaPlayerInstance = course_resumed.getCurrentPlayable()
      mediaPlayerInstance.play()

   except:
      print(" Invalid input !!! Try again !!")
   return


if __name__ == "__main__":
    
    init()
    main()

