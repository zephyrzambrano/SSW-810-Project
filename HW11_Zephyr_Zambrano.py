"""
Homework 11 by Zephyr Zambrano

Repository of data for a college or university.
Keeps track of students, instructors, grades, and majors.

Stores this data in a SQLite database.

"""


from prettytable import PrettyTable
from collections import defaultdict
import os
import sqlite3


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
    def __init__(self, cwid, name, major_name, major): # major_name
        """ Initialize students. """
        self._cwid = cwid
        self._name = name
        self._major_name = major_name
        self._major = major # instance of class Major corresponding to his student's major
        self._courses = dict() # _courses[course] = grade
        # need major name for student but also list of majors in existence
        # self._major_name = major_name
        
    def add_course(self, course, grade):
        """ Adds a course to the student's record.
        Only adds the course if the student received a passing grade.
        Passing grades: "A", "A-", "B+", "B", "B-", "C+", and "C"
        """
        passing_grades = ["A", "A-", "B+", "B", "B-", "C+", "C"]
        
        if grade in passing_grades:
            self._courses[course] = grade

    def pt_row(self):
        """ JRR added definition 
            REturn a list of values to include in the prettytable for this student
        """
        passed = self._major.passed_courses(self._courses)
        rem_required = self._major.remaining_required(passed)
        rem_electives = self._major.remaining_electives(passed)
        return [self._cwid, self._name, self._major_name, sorted(passed), sorted(rem_required), sorted(rem_electives)]


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

    def pt_row(self):
        for course, cnt in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, cnt]


class Major:
    """ Keeps track of majors. """
    PASSING_GRADES = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, dept):
        """ Initializes majors. """
        self._dept = dept
        self._courses = dict() # key: course; value: flag
        self._required = set() # set of required courses
        self._electives = set() # set of elective courses
    
    def add_course(self, course, flag):
        """ Add course to _required or _electives based on flag. """
        # Flags: R for Required or E for Electives
        if flag == "R":
            self._required.add(course)
        else:
            self._electives.add(course)
    
    def passed_courses(self, course_grades):
        """ Shows which courses the student has already passed.
        Passing grade is a C or better. """
        # pass  JRR
        return {course for course, grade in course_grades.items() if grade in Major.PASSING_GRADES}
    
    def remaining_required(self, passed):
        """ Shows which courses the student still needs to
        complete in order to graduate. """
        # JRR pass
        return self._required - passed

    def remaining_electives(self, passed):
        """ Shows which courses the student still needs to
        complete in order to graduate. """
        # JRR pass
        if self._electives.intersection(passed):
            return {}
        else:
            return self._electives


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
        
        self._get_majors(os.path.join(path, "majors.txt")) # JRR - define the majors first so the Students can find them
        self._get_students(os.path.join(path, "students.txt"))  # JRR
        self._get_instructors(os.path.join(path, "instructors.txt")) # JRR
        self._get_grades(os.path.join(path, "grades.txt")) # JRR
        
        self.student_prettytable()
        self.instructor_prettytable()
        self.major_prettytable()
    
    def _get_students(self, path):
        """ Gets the students' information from the "students.txt" file. """
        try:
            for cwid, name, major_name in file_reading_gen(path, 3, sep="\t", header=True):
                if major_name in self._majors:
                    self._students[cwid] = Student(cwid, name, major_name, self._majors[major_name])
                else:
                    print(f"Student {cwid} has an unknown major {major_name}")
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_instructors(self, path):
        """ Gets the instructors' information from the "instructors.txt" file. """
        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep="\t", header=True):
                self._instructors[cwid] = Instructor(cwid, name, dept)   
        except FileNotFoundError:
            print("Can't open", path)
    
    def _get_grades(self, path):
        """ Gets the grades from the "grades.txt" file. """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep="\t", header=True):
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
    
    def _get_majors(self, path):
        try:   # JRR
            for dept, flag, course in file_reading_gen(path, 3, sep="\t", header=True):
                #try: # JRR
                if dept not in self._majors:  # JRR
                    self._majors[dept] = Major(dept)
                self._majors[dept].add_course(course, flag)
        except FileNotFoundError:  # JRR
            print("Can't open", path)
    
    def student_prettytable(self):
        """ Prints the student prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Classes", "Remaining Required", "Remaining Electives"])  # JRR
        # more fields:
        # 
        # Completed Courses, Remaining Required, Remaining Electives
        
        print("Student Summary")
        
        for student in self._students.values():
            # JRR pt.add_row([student._cwid, student._name, student._major, student._courses])
            pt.add_row(student.pt_row())
        
        print(pt)
        return pt
    
    def instructor_prettytable(self):
        """ Prints the instructor prettytable. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])  # JRR
        
        print("Instructor Summary")
        
        for instructor in self._instructors.values():
            for row in instructor.pt_row():
                # JRR pt.add_row([instructor._cwid, instructor._name, instructor._dept])
                pt.add_row(row)
        
        print(pt)
        return pt
    
    def major_prettytable(self):
        """ Prints a summary of the required courses for a particular major. """
        pt = PrettyTable(field_names=["Department", "Required Courses", "Electives"])
        
        print("Major Summary")
        
        for major in self._majors.values():
            pt.add_row([major._dept, major._required, major._electives])
        
        print(pt)
        return(pt)
    
    def instructor_table_db(self, db_path):
        """
        Create a new instructor PrettyTable that retrieves the data for the table
        from the database you created above using 'db_path'
        to specify the path of your SQLite database file.
        Use Python calls to execute the instructor summary query you defined above
        and use the data from executing the query to generate and display a second instructor
        PrettyTable with the results.
        
        """
        DB_FILE = "/Users/Zephyr Zambrano/Documents/GitHub/SSW-810-Project/810_startup.db"
        db = sqlite3.connect(DB_FILE)
        
        print("Instructor Summary")
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])
        
        # for row in db.execute("select"):
        #     pt.add_row(row)
        
        # select CWID, Name, Dept, Course from instructors join grades on CWID = InstructorCWID
        # select Course, count(*) as cnt from grades group by StudentCWID
        
        db.close()


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
    wdir10 = "/Users/Zephyr Zambrano/Documents/GitHub/SSW-810-Project"
    
    # wdir10 = '/Users/jrr/Documents/Stevens/810/Assignments/HW10_Repository_Test'
    # wdir_bad_data = '/Users/jrr/Documents/Stevens/810/Assignments/HW10_Repository_BadData'
    # wdir_bad_fields = '/Users/jrr/Documents/Stevens/810/Assignments/HW10_Repository_BadFields'

    # print("Good data")
    _ = Repository(wdir10)

    # print("\nBad Data")
    # print("--> should report student with unknown major, grade for unknown student, and grade for unknown instructor")
    # _ = Repository(wdir_bad_data)

    # print("\nBad Fields\n")
    # print("should report bad student, grade, instructor feeds")
    # _ = Repository(wdir_bad_fields)

    # print("\nNon-existent Data Directory\n")
    # _ = Repository("Not A Directory")


if __name__ == "__main__":
    main() 
