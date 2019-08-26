#!/usr/bin/env

from deciphertools import tools
from decipher.beacon import api
debug=0

dec = tools()
dec.decipher_login()
dl = dec.get_surveys()
output = dec.survey_flatten(dl)

# print all or search
def survey_action():
	survey_action = -9
	while survey_action not in range(0,4):
		print """\n> Choose next action:
1: print all survey data to screen
2: export survey data to file
3: search for a study
0: exit
		"""
		survey_action = raw_input()
		try:
			survey_action = int(survey_action)
			if survey_action == 0:
				if debug == 1:
					print "[DEBUG] survey_action == 0"
				exit = 1
				return exit
			if survey_action == 1:
				dec.survey_print_all(output)
				return exit
			elif survey_action == 2:
				# need validation
				dec.store(dec.survey_to_str(output), 'surveys')
				return exit
			elif survey_action == 3:
				# Feature request: add search by project ID
				search_str = dec.search_string()
				dec.survey_search(output, search_str)
				return exit
		except:
			pass

exit = 0
while exit != 1:
	exit = survey_action()

print "Bye"