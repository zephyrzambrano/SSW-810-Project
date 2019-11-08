"""
Homework 9 by Zephyr Zambrano

Repository of data for a college or university.
Keeps track of students, instructors, and grades.

"""


from prettytable import PrettyTable
from collections import defaultdict
import os


class Student:
    """
    Requirements:
    - Stores information about a single student with all of the relevant information including:
        - cwid
        - name
        - major
        - Container of courses and grades
    - Allows other classes to add a course and grade to the container of courses and grades
    - Returns the summary data about a single student needed in the pretty table
    
    """
    def __init__(self, cwid, name, major):
        """ Initialize students. """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = dict() # _courses[course] = grade


class Instructor:
    """
    Requirements:
    - Stores information about a single Instructor with all of the relevant information including:
        - cwid
        - name
        - department
        - Container of courses taught and the number of students in each course
    - Allows other classes to specify a course, and updates the container of courses
      taught to increment the number of students by 1
    - Returns information needed by the Instructor prettytable.
      NOTE that the instructor prettytable may have multiple rows for each
      instructor because an instructor may teach multiple courses.
    
    """
    def __init__(self, cwid, name, dept):
        """ Initialize instructors. """
        self._cwid = cwid
        self._name = name
        self._dept = dept        
        self._courses = defaultdict(int) # track _courses[course] = # of students


class Repository: #holds all of the data for a specific organization
    """
    Requirements:
    - Includes a container for all students
    - Includes a container for all instructors
    - __init__(self, dir_path) specifies a directory path where to find the students.txt, instructors.txt, and grades.txt files.   Your solution should allow testing multiple directories with different data files
    - Read the students.txt file, creating a new instance of class Student for each line in the file, and add the new Student to the repository's container with all students.
    - Read the instructors.txt file, creating a new instance of class Instructor for each line in the file, and add the new Instructor to the repository's container with all Instructors.
    - Read the grades.txt file and process each grade:
        - Use the student cwid, course, and grade and ask the instance of class Student associated the student cwid to add the grade to the student information
        - Use the instructor cwid and course to ask the instance of class Instructor to note that the instructor taught another student in the specific course
    - print a student prettytable
    - print an instructor prettytable
    
    """
    def __init__(self, path):
        """ Initializes the repository. """
        self._students = dict() # students(cwid) = Student()
        self._instructors = dict() # instructors(cwid) = Instructor()
        
        self._get_students("students.txt")
        self._get_instructors("instructors.txt")
        self._get_grades("grades.txt")
        
        # the following statements result in empty prettytables
        # 
        # self._get_students(os.path.join(path, "students.txt"))
        # self._get_instructors(os.path.join(path, "instructors.txt"))
        # self._get_grades(os.path.join(path, "grades.txt"))
    
    def _get_students(self, path):
        """ Gets the students' information from the "students.txt" file. """
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=False):
                self._students[cwid] = Student(cwid, name, major)
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_instructors(self, path):
        """ Gets the instructors' information from the "instructors.txt" file. """
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header=False):
                self._instructors[cwid] = Instructor(cwid, name, dept)   
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_grades(self, path):
        """ Gets the grades from the "grades.txt" file. """
        pass
            
    def student_prettytable(self):
        """ Prints the student prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Major"])
        
        for student in self._students.values():
            pt.add_row([student._cwid, student._name, student._major])
        
        print(pt)
        return pt
    
    def instructor_prettytable(self):
        """ Prints the instructor prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department"])
        
        for instructor in self._instructors.values():
            pt.add_row([instructor._cwid, instructor._name, instructor._dept])
        
        print(pt)
        return pt


def file_reading_gen(path, fields, sep=",", header=False):
    """ Generator that reads a file, gets the data from the file,
    and returns the data from the file line by line with each yield.
    Line numnbers start at 0. """
    try:
        fp = open(path, "r")
    except FileNotFoundError:
        print("Can't open", path)
    else:
        with fp:
            line_list = fp.readlines()
            line_num = 0
            
            # check that the header fills the requirements
            if header == True:
                h = line_list.pop(0)
                h = h.strip("\n")
                h_list = h.split(sep)
                
                if len(h_list) != fields:
                    raise ValueError(f"{path} has {len(h_list)} fields on (header) line {line_num} but expected {fields}")                
            
            # process the rest of the lines
            for line in line_list:  
                line = line.strip("\n")
                    
                field_list = line.split(sep)
                
                if len(field_list) != fields:
                    raise ValueError(f"{path} has {len(field_list)} fields on line {line_num} but expected {fields}")
                
                yield(tuple(field_list))


def main():
    stevens = Repository("SSW-810-Project")
    print("Student Summary")
    Repository.student_prettytable(stevens)
    print()
    print("Instructor Summary")
    Repository.instructor_prettytable(stevens)


if __name__ == "__main__":
    main()
