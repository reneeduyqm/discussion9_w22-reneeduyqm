from bs4 import BeautifulSoup
import requests
import re
import unittest
import os
import csv

def get_profs(filepath):
    """
    This function accepts a CSV file, filepath, and parses it to return a list of
    lists. Each list should contain the name, title(s), and email addrress of professors
    at UMSI. This should only contain professors, not lecturers or research fellows.
    """
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filepath)
    with open(full_path, 'r') as f:
        reader = csv.reader(f)
        prof = []
        for line in reader:
            if 'professor' in line[1].lower():
                prof.append(line)
    return prof

    

def get_valid_emails(prof_list):
    """
    This function accepts a list of lists and returns a dictionary. The keys should be
    the names of professors with valid email addresses and the values should be the email
    addresses of the professors. A valid email address should just have lowercase alphabetic
    characters and end with @umich.edu.
    Examples of invalid email addresses:
        buisl@umich.edu.com
        mjguz@um1ch.edu
        ajflynn @umich.edu
        vgvinodv@umich_.edu
    """
    search = r"\b[a-z]+@umich\.edu$"
    dict = {}
    for prof in prof_list:
        if re.findall(search, prof[2]):
            dict[prof[0]] = prof[2]

    return dict

def get_lsa_majors():
    """
    This function uses BeautifulSoup to find all of the majors listed on https://admissions.umich.edu/academics-majors/majors-degrees
    and returns a list of strings with the names of all the majors offered through the College of Literature, Science,
    and the Arts.
    """
    page = requests.get("https://admissions.umich.edu/academics-majors/majors-degrees")
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find_all('td', {'class':'views-field w-7/12 hover:text-tappan-red views-field-title'})
    lsa_majors = []
    for match in matches:
        major_url = match.find('a').get('href')
        if 'lsa' in major_url:
            lsa_majors.append(match.find('a').text)

    return lsa_majors
    
class TestDiscussion9(unittest.TestCase):
    def setUp(self):
        self.prof_list = [
            ['Patricia Abbott', 'Adjunct Clinical Associate Professor of Information, School of Information', 'pabbott@umich.edu'],
            ['Mark Ackerman', 'George Herbert Mead Collegiate Professor of Human-Computer Interaction, Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Professor of Learning Health Sciences, Medical School', 'ackerm@umich.edu'],
            ['Eytan Adar', 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'eadar@umich.edu'],
        ]

    def test_get_profs(self):
        profs = get_profs('umsi_faculty.csv')
        self.assertIsInstance(profs, list)
        self.assertIsInstance(profs[0], list)
        self.assertEqual(len(profs), 102)
        self.assertEqual(profs[:3], self.prof_list)

    def test_get_valid_emails(self):
        profs = get_profs('umsi_faculty.csv')
        valid_emails_dict = get_valid_emails(profs)
        self.assertIsInstance(valid_emails_dict, dict)
        self.assertEqual(len(valid_emails_dict), 90)
        for val in valid_emails_dict.values():
            invalid = [' ', '_', '1', '.com', 'edu.']
            if any(x in val for x in invalid):
                print(val)
                self.assertTrue(False, 'One or more characters in this email address were invalid')

    def test_get_lsa_majors(self):
        majors = get_lsa_majors()
        self.assertEqual(len(majors), 84)
        self.assertIsInstance(majors, list)
        self.assertEqual(majors[6], 'Astronomy and Astrophysics')

if __name__ == '__main__':
    unittest.main(verbosity=2)