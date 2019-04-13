import sqlite3
import os

def printtable(cursor):
    cursor.execute("SELECT * FROM courses")
    list = cursor.fetchall()
    print("courses")
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

def schedule(db,classr,iternum):
    with db:
        cursor = db.cursor()
        if classr[3] == 0:
            cursor.execute("SELECT * FROM courses WHERE class_id=(?)", (classr[0],))
            course = cursor.fetchone();
            if course is not None:
                print('(' + str(iternum) + ') ' + classr[1] + ': ' + course[1] + ' is schedule to start')
                cursor.execute("UPDATE classrooms SET current_course_id=(?),current_course_time_left=(?) WHERE id=(?)",
                               (course[0], course[5], classr[0],))
                db.commit()
                cursor.execute("SELECT * FROM students WHERE grade=(?)", (course[2],))
                students = cursor.fetchone()
                if students[1] > course[3]:
                    cursor.execute("UPDATE students SET count=(?) WHERE grade=(?)", (students[1] - course[3],course[2],))
                    db.commit()
                else:
                    cursor.execute("UPDATE students SET count=(?) WHERE grade=(?)", (0,course[2],))
                    db.commit()
        else:
            cursor.execute("SELECT * FROM courses WHERE id=(?)",(classr[2],))
            course=cursor.fetchone()
            cursor.execute("UPDATE classrooms SET current_course_time_left=(?) WHERE id=(?)",
                           (classr[3] - 1, classr[0],))
            db.commit()
            if (classr[3] - 1) > 0:
                print('(' + str(iternum) + ') ' + classr[1] + ': occupied by ' + course[1])
            else:
                cursor.execute("UPDATE classrooms SET current_course_id=(?) WHERE id=(?)",
                              (0, classr[0],))
                print('(' + str(iternum) + ') ' + classr[1] + ': ' + course[1] + ' is done')
                cursor.execute("DELETE FROM courses WHERE id = (?)", (course[0],))
                db.commit()
                cursor.execute("SELECT * FROM classrooms WHERE id=(?)",(classr[0],))
                newclassr=cursor.fetchone()
                schedule(db,newclassr,iternum)


def main():
    iternum = 0
    databaseexisted = os.path.isfile('classes.db')
    database = sqlite3.connect('classes.db')
    if databaseexisted:
        with database:
            cursor = database.cursor()
            cursor.execute("SELECT * FROM courses")
            course = cursor.fetchone()
            while course is not None:
                cursor.execute("SELECT * FROM classrooms ")
                classrooms = cursor.fetchall()
                for classr in classrooms:
                    schedule( database, classr, iternum)
                iternum = iternum + 1
                printtable(cursor)
                cursor.execute("SELECT * FROM courses")
                course = cursor.fetchone()
main()