"""
Homework 9 Test by Zephyr Zambrano

Tests that the methods in HW09_Zephyr_Zambrano work properly.

"""


import unittest
from HW09_Zephyr_Zambrano import Repository
from prettytable import PrettyTable
from collections import defaultdict
import os


class TestRepository(unittest.TestCase):
        def test_student_prettytable(self):
                """ Tests that the student prettytable is correct """
                pt = PrettyTable(field_names=["CWID", "Name", "Major"])
                
                pt.add_row(["10103", "Baldwin, C", "SFEN"])
                pt.add_row(["10115", "Wyatt, X", "SFEN"])
                pt.add_row(["10172", "Forbes, I", "SFEN"])
                pt.add_row(["10175", "Erickson, D", "SFEN"])
                pt.add_row(["10183", "Chapman, O", "SFEN"])
                pt.add_row(["11399", "Cordova, I", "SYEN"])
                pt.add_row(["11461", "Wright, U", "SYEN"])
                pt.add_row(["11658", "Kelly, P", "SYEN"])
                pt.add_row(["11714", "Morton, A", "SYEN"])
                pt.add_row(["11788", "Fuller, E", "SYEN"])          
                
                stevens = Repository("810-HW09")
                pt2 = Repository.student_prettytable(stevens)
                
                self.assertEqual(pt, pt2)
            
        def test_instructor_prettytable(self):
                """ Prints the instructor prettytable. """
                pt = PrettyTable(field_names=["CWID", "Name", "Department"])
                
                pt.add_row(["98765", "Einstein, A", "SFEN"]) 
                pt.add_row(["98764", "Feynman, R", "SFEN"]) 
                pt.add_row(["98763", "Newton, I", "SFEN"]) 
                pt.add_row(["98762", "Hawking, S", "SYEN"]) 
                pt.add_row(["98761", "Edison, A", "SYEN"]) 
                pt.add_row(["98760", "Darwin, C", "SYEN" ]) 
                
                stevens = Repository("810-HW09")
                pt2 = Repository.student_prettytable(stevens)
                
                self.assertEqual(pt, pt2)        


if __name__ == "__main__":
        unittest.main(exit=False, verbosity=2)
