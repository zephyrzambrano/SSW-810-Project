"""
Homework 10 Test by Zephyr Zambrano

Tests that the methods in HW10_Zephyr_Zambrano work properly.

"""


import unittest
from HW10_Zephyr_Zambrano import Repository
from prettytable import PrettyTable
from collections import defaultdict
import os


class TestRepository(unittest.TestCase):
    """ Tests that the prettytable methods in the Repository class work properly. """

    def test_major_prettytable():
        """ Tests that the major prettytable is correct. """
        pt = PrettyTable(field_names=["Department", "Required Courses", "Electives"])
        
        pt.add_row(["SFEN", {'SSW 564', 'SSW 567', 'SSW 555', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}])
        pt.add_row(["SFEN", {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 810', 'SSW 565', 'SSW 540'}])
        
        stevens = Repository("SSW-810-Project")
        pt2 = Repository.major_prettytable(stevens)
        
        self.assertEqual(pt, pt2)    
    
    def test_student_prettytable(self):
        """ Tests that the student prettytable is correct """       
        pt = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"])
        
        pt.add_row(["10103", "Baldwin, C", "SFEN", ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'], {'SSW 540', 'SSW 555'} , None])
        pt.add_row(["10115", "Wyatt, X", "SFEN", ['SSW 567', 'SSW 564', 'SSW 687', 'CS 545'], {'SSW 540', 'SSW 555'} , None])
        pt.add_row(["10172", "Forbes, I", "SFEN", ['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'}, {'CS 501', 'CS 545', 'CS 513'}])
        pt.add_row(["10175", "Erickson, D", "SFEN", ['SSW 567', 'SSW 564', 'SSW 687'], {'SSW 540', 'SSW 555'} , {'CS 501', 'CS 545', 'CS 513'}])
        pt.add_row(["10183", "Chapman, O", "SFEN", ['SSW 689'], {'SSW 567', 'SSW 564', 'SSW 555', 'SSW 540'}, {'CS 501', 'CS 545', 'CS 513'}])
        pt.add_row(["11399", "Cordova, I", "SYEN", ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'} , None])
        pt.add_row(["11461", "Wright, U", "SYEN", ['SYS 800', 'SYS 750', 'SYS 611'], {'SYS 612', 'SYS 671'} , {'SSW 540', 'SSW 565', 'SSW 810'}])
        pt.add_row(["11658", "Kelly, P", "SYEN", [], {'SYS 612', 'SYS 671', 'SYS 800'} , {'SSW 540', 'SSW 565', 'SSW 810'}])
        pt.add_row(["11714", "Morton, A", "SYEN", ['SYS 611', 'SYS 645'], {'SYS 612', 'SYS 671', 'SYS 800'} , {'SSW 540', 'SSW 565', 'SSW 810'}])
        pt.add_row(["11788", "Fuller, E", "SYEN", ['SSW 540'], {'SYS 612', 'SYS 671', 'SYS 800'} , None])
        
        stevens = Repository("SSW-810-Project")
        pt2 = Repository.student_prettytable(stevens)
        
        self.assertEqual(pt, pt2)
    
    def test_instructor_prettytable(self):
        """ Tests that the instructor prettytable is correct. """
        pt = PrettyTable(field_names=["CWID", "Name", "Department", "Course", "Students"])

        pt.add_row(["98765", "Einstein, A", "SFEN", "SSW 567", 4])
        pt.add_row(["98765", "Einstein, A", "SFEN", "SSW 540", 3]) 
        
        pt.add_row(["98764", "Feynman, R", "SFEN", "SSW 564", 3])
        pt.add_row(["98764", "Feynman, R", "SFEN", "SSW 687", 3]) 
        pt.add_row(["98764", "Feynman, R", "SFEN", "CS 501 ", 1]) 
        pt.add_row(["98764", "Feynman, R", "SFEN", "CS 545", 1]) 
        
        pt.add_row(["98763", "Newton, I", "SFEN", "SSW 555", 1])
        pt.add_row(["98763", "Newton, I", "SFEN", "SSW 689", 1])
        
        pt.add_row(["98760", "Darwin, C", "SYEN", "SYS 800", 1])
        pt.add_row(["98760", "Darwin, C", "SYEN", "SYS 750", 1])
        pt.add_row(["98760", "Darwin, C", "SYEN", "SYS 611", 2])
        pt.add_row(["98760", "Darwin, C", "SYEN", "SYS 645", 1])

        stevens = Repository("SSW-810-Project")
        pt2 = Repository.instructor_prettytable(stevens)

        self.assertEqual(pt, pt2)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
