import os
import base64
import codecs

import MySQLdb
import UnitTest

# Possible Categories are:
# LAB-0 (INTRO), LAB-1 (IO), LAB-2 (CONDITIONALS), LAB-3 (SERIES), LAB-4 (PATTERN), LAB-5 (ARRAYS), LAB-6 (ARRAY/STRINGS)
# LAB-7 (MATRICES), LAB-8 (RECURSION), LAB-9 (POINTERS), LAB-10 (STRUCTURES), LAB-11 (DS)
# LabExam-1 S1, LabExam-1 S2, LabExam-2 S1, LabExam-2 S2, MockLabExam-1..5

labCategory = 'LAB-2 (CONDITIONALS)'

# Open database connection

db = MySQLdb.connect('localhost', 'root', "l;'", 'its')

# prepare a cursor object using cursor() method

cursor = db.cursor()
ANSWER = 'WRONG_ANSWER'

cursor.execute('SELECT FROM_BASE64(cd.contents), tc.input, tc.output, ev.output FROM `code` AS cd, `evaluation` AS ev, `test_case` AS tc, `assignment` AS asn, `problem` AS pb WHERE pb.category=\"' + labCategory + '\" AND pb.id=asn.problem_id AND asn.id=cd.assignment_id AND cd.id=ev.code_id AND tc.id=ev.testcase_id AND ev.verdict=\"' + ANSWER + '\" LIMIT 13;')
k = cursor.fetchall()
for table in k:
    #table = k[3]
    print table[0], '\n', table[1], '\n',  table[2], '\n', table[3]
    UnitTest.test(table[0], table[1], table[2], table[3])
    print "\n"
