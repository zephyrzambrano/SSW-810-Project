"""
Homework 11 Test by Zephyr Zambrano
Tests that the methods in HW11_Zephyr_Zambrano work properly.

"""


import unittest
from HW11_Zephyr_Zambrano import Repository
from prettytable import PrettyTable
from collections import defaultdict
import os
import sqlite3


class TestRepository(unittest.TestCase):
    """ Tests that the prettytable methods in the Repository class work properly. """

    def test_major_prettytable():
        """ Tests that the major prettytable is correct. """
        pt = PrettyTable(field_names=["Department", "Required Courses", "Electives"])
        
        pt.add_row(["SFEN", {'SSW 810', 'SSW 555', 'SSW 540'}, {'CS 501', 'CS 546'}])
        pt.add_row(["CS", {'CS 570', 'CS 546'}, {'SSW 810', 'SSW 565'}])
        
        stevens = Repository("SSW-810-Project")
        pt2 = Repository.major_prettytable(stevens)
        
        self.assertEqual(pt, pt2)    
    
    def test_student_prettytable(self):
        """ Tests that the student prettytable is correct """       
        pt = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"])
        
        pt.add_row(["10103", "Jobs, S", "SFEN", ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], []])
        pt.add_row(["10115", "Bezos, J", "SFEN", ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546']])
        pt.add_row(["10183", "Musk, E", "SFEN",  ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546']])
        pt.add_row(["11714", "Gates, B", "CS", ['CS 546', 'CS 570', 'SSW 810'], [],[]])
        pt.add_row(["11717", "Kernighan, B", "CS", [], ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']])
        
        stevens = Repository("SSW-810-Project")
        pt2 = Repository.student_prettytable(stevens)
        
        self.assertEqual(pt, pt2)
    
    def test_instructor_prettytable(self):
        """ Tests that the instructor prettytable is correct. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])

        pt.add_row(["98764", "Cohen, R", "SFEN", "CS 546", 1])
        
        pt.add_row(["98763", "Rowland, J", "SFEN", "SSW 810", 4]) 
        pt.add_row(["98763", "Rowland, J", "SFEN", "SSW 555", 1])
        
        pt.add_row(["98764", "Feynman, R", "CS", "CS 501", 1]) 
        pt.add_row(["98764", "Feynman, R", "CS", "CS 546", 1]) 
        pt.add_row(["98764", "Feynman, R", "CS", "CS 570", 1]) 

        stevens = Repository("SSW-810-Project")
        pt2 = Repository.instructor_prettytable(stevens)

        self.assertEqual(pt, pt2)
    
    def test_instructor_table_db(self):
        """ Tests that instructor_table_db works properly. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])
        
        pt.add_row(["98764", "Feynman, R", "CS", "CS 501", 1]) 
        pt.add_row(["98764", "Feynman, R", "CS", "CS 546", 1]) 
        pt.add_row(["98764", "Feynman, R", "CS", "CS 570", 1])         
        
        pt.add_row(["98763", "Rowland, J", "SFEN", "SSW 555", 1])
        pt.add_row(["98763", "Rowland, J", "SFEN", "SSW 810", 4])         
        
        pt.add_row(["98764", "Cohen, R", "SFEN", "CS 546", 1])

        stevens = Repository("SSW-810-Project")
        pt2 = Repository.instructor_table_db("/Users/Zephyr Zambrano/Documents/GitHub/SSW-810-Project/810_startup.db")

        self.assertEqual(pt, pt2)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
