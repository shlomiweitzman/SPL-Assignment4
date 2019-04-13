import sqlite3
import os
import sys


def main(args):
    inputfilename=sys.argv[1]
    databaseexisted = os.path.isfile('classes.db')
    database = sqlite3.connect('classes.db')
    with database:
        cursor=database.cursor()
        if not databaseexisted:
            cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL, student TEXT NOT NULL, number_of_students INTEGER NOT NULL, class_id INTEGER REFERENCES classrooms(id),course_length INTEGER NOT NULL)")
            cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL)")
            cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY, location TEXT NOT NULL, current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL)")
            with open(inputfilename) as inputfile:
                for line in inputfile:
                    words=line.split(",")
                    if words[0].strip()=="C":
                        cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)",(int((words[1]).strip())
                                                                                  ,(words[2]).strip()
                                                                                  ,(words[3]).strip()
                                                                                  ,(int((words[4]).strip()))
                                                                                 ,(int((words[5]).strip()))
                                                                                  ,int(words[6].strip())))
                    if words[0].strip() == "S":
                        cursor.execute("INSERT INTO students VALUES(?,?)",((words[1]).strip(),int(words[2].strip())))
                    if words[0].strip() == "R":
                        cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)",(int((words[1]).strip()),words[2].strip(),0,0))
            cursor.execute("SELECT * FROM courses")
            list=cursor.fetchall()
            print("courses" )
            for course in list:
                print(str(course))
            cursor.execute("SELECT * FROM classrooms")
            list = cursor.fetchall()
            print("classrooms")
            for classroom in list:
                print(str(classroom))
            cursor.execute("SELECT * FROM students")
            list = cursor.fetchall()
            print("students")
            for student in list:
                print(str(student))
if __name__== '__main__':
    main(sys.argv)
