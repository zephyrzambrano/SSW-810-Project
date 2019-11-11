"""
Homework 10 by Zephyr Zambrano

Repository of data for a college or university.
Keeps track of students, instructors, grades, and majors.

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
    def __init__(self, cwid, name, dept): # major_name
        """ Initialize students. """
        self._cwid = cwid
        self._name = name
        self._dept = dept # department the major is in
        self._major = Major(dept) # instance of class Major corresponding to his student's major
        
        self._courses = dict() # _courses[course] = grade
        
        self._finished_required = set()
        self._finished_electives = set()
        
        self._remaining_required = set()
        self._remaining_electives = set()  
        
    def add_course(self, course, grade):
        """ Adds a course to the student's record.
        Only adds the course if the student received a passing grade.
        Passing grades: "A", "A-", "B+", "B", "B-", "C+", and "C"
        Students only need to take one elective in order to graduate.
        """
        passing_grades = ["A", "A-", "B+", "B", "B-", "C+", "C"]
        
        if grade in passing_grades:
            self._courses[course] = grade      
    
    def finished_required(self):
        """ Required courses that the student has completed. """
        for course in self._courses:
            if course in self._major._required:
                self._finished_required.add(course)
    
    def finished_electives(self):
        """ Electives that the student has completed. """
        for course in self._courses:
            if course in self._major._electives:
                self._finished_electives.add(course)   
    
    def remaining_required(self):
        """ Required courses that the student still needs to complete. """
        for course in self._major._required:
            if course not in self._finished_required:
                self._remaining_required.add(course)
    
    def remaining_electives(self):
        """ Elective courses that the student still needs to complete.
        Students are only required to copmlete one elective in order
        to graduate. """
        if self._finished_electives != set():
            self._remaining_electives = None
        else:
            for course in self._major._electives:
                self._remaining_electives.add(course)


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
    
    def add_course(self, course):
        """ Adds a course to the student's record.
        Only adds the course if the student received a passing grade.
        Passing grades: "A", "A-", "B+", "B", "B-", "C+", and "C"
        """
        if course in self._courses:
            self._courses[course] = self._courses[course] + 1
        else:
            self._courses[course] = 1


class Major:
    """ Keeps track of majors. """
    def __init__(self, dept):
        """ Initializes majors. """
        self._dept = dept
        self._required = set() # set of required courses
        self._electives = set() # set of elective courses
    
    def add_course(self, course, flag):
        """ Add course to _required or _electives based on flag. """
        # Flags: R for Required or E for Electives
        if flag == "R":
            self._required.add(course)
        elif flag == "E":
            self._electives.add(course)


class Repository: # holds all of the data for a specific organization
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
        self._majors = dict() # majors(dept) = Major()
        
        # problems with the following os statements:
        # program can't open files
        # empty prettytables (because files cannot be opened)
        # 
        # self._get_majors(os.path.join(path, "majors.txt"))
        # self._get_students(os.path.join(path, "students.txt"))
        # self._get_instructors(os.path.join(path, "instructors.txt"))
        # self._get_grades(os.path.join(path, "grades.txt"))
        
        self._get_majors("majors.txt")
        self._get_students("students.txt")
        self._get_instructors("instructors.txt")
        self._get_grades("grades.txt")
        
        # should add data to Student object, but doesn't
        for cwid in self._students:
            self._students[cwid].finished_required()
            self._students[cwid].finished_electives()
                        
            self._students[cwid].remaining_required()
            self._students[cwid].remaining_electives()
    
    def _get_majors(self, path):
        for dept, flag, course in file_reading_gen(path, 3, sep="\t", header=True):
            try:
                if dept in self._majors:
                    self._majors[dept].add_course(course, flag)
                else:
                    self._majors[dept] = Major(dept)
                    self._majors[dept].add_course(course, flag)
            except FileNotFoundError:
                print("Can't open", path)    
    
    def _get_students(self, path):
        """ Gets the students' information from the "students.txt" file. """
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep=";", header=True):
                self._students[cwid] = Student(cwid, name, dept)
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_instructors(self, path):
        """ Gets the instructors' information from the "instructors.txt" file. """
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep="|", header=True):
                self._instructors[cwid] = Instructor(cwid, name, dept)   
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_grades(self, path):
        """ Gets the grades from the "grades.txt" file. """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep="|", header=True):
                try:
                    self._students[student_cwid].add_course(course, grade) # tell the student about a course
                except KeyError:
                    print(f"Found grade for unknown student {student_cwid}")
                
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade) # tell the student about a course
                else:
                    print(f"Found grade for unknown student {student_cwid}")
                
                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_course(course) # tell the instructor about a course/student
                else:
                    print(f"Found grade for unknown instructor {instructor_cwid}")
        except FileNotFoundError:
            print("Can't open", path)
    
    def major_prettytable(self):
        """ Prints a summary of the required courses for a particular major. """
        pt = PrettyTable(field_names=["Department", "Required Courses", "Electives"])
        
        print("Major Summary")
        
        for major in self._majors.values():
            pt.add_row([major._dept, major._required, major._electives])
        
        print(pt)
        print()
        return(pt)    
    
    def student_prettytable(self):
        """ Prints the student prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"])
        
        print("Student Summary")
        
        for student in self._students.values():
            courses = list()
            for course in student._courses:
                courses.append(course)
            pt.add_row([student._cwid, student._name, student._dept, courses, student._remaining_required, student._remaining_electives])
        
        print(pt)
        print()
        return pt
    
    def instructor_prettytable(self):
        """ Prints the instructor prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])
        
        print("Instructor Summary")
        
        courses = list()
        for course in self._instructors.values():
            courses.append(course)  
        
        for instructor in self._instructors.values():
            for course in instructor._courses:
                pt.add_row([instructor._cwid, instructor._name, instructor._dept, course, instructor._courses[course]])
        
        print(pt)
        print()
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
    Repository.major_prettytable(stevens)
    Repository.student_prettytable(stevens)
    Repository.instructor_prettytable(stevens)


if __name__ == "__main__":
    main()
