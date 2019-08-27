#!/usr/bin/env
# -*- coding: utf-8 -*-

from decipher.beacon import api
from halo import Halo
import csv, sys, re, datetime, dateutil.parser, os, getpass
import importlib
debug=0

# importlib.reload(sys)
# sys.setdefaultencoding('utf8')

class tools:

	def __init__(self):
		print("")

	# Validate availability modules
	def validate_modules(self):
		spinner = Halo(text='Validating availability modules', spinner='dots')
		spinner.start()
		modules = ['halo', 'cursor', 'decipher', 'simplejson', 'requests']
		try:
			for m in modules:
				try:
					import m
				except ImportError:
					import subprocess
					if sys.version_info.major == 2:
						subprocess.call(['pip2', 'install', m])
					else:
						subprocess.call(['pip3', 'install', m])
			spinner.succeed('Required modules available')
		except:
			spinner.fail('One ore more modules failed to load')
			print('If installation did not work for you, try: pip install --user <module> in the command line')


	# Cleaning pattern / modules
	def clean_string(self, string_in):
		if type(string_in) is str:
			if len(string_in) == 0 or string_in.lower() == 'none':
				return ''
			else:
				repl = re.compile('(\n|\t|\|)') # removes enters, tabs and pipes
				string_out = repl.sub('', string_in)
				return string_out
		elif string_in is None:
			return ''
		else:
			return string_in

	# Search pattern
	def search_string(self):
		if debug == 1:
			print('[DEBUG] Capturing search string')
		search_str_raw = ''
		while len(search_str_raw) < 1:
			search_str_raw = input('> Enter search string: ')
		search_str = re.compile(''.join(['.*', search_str_raw, '.*']).lower())
		return search_str

	# Read API token
	def read_api_token(self):
		if debug == 1:
			print('[DEBUG] Reading API token (read_api_token())')
		try:
			config = open('/Users/' + getpass.getuser() + '/.decipher/config', 'r')
			api_token = [s.rstrip() for s in config.readlines() if "APITOKEN" in s]
			config.close()
			if len(api_token) == 0:
				print("[ERROR] No api token was found, make sure to run decipher-install.sh first")
			if debug == 1:
				print('[DEBUG] API token OK')
			return api_token[0][9:]
		except:
			print(("[ERROR] ", sys.exc_info()[0]))
			raise

	# Decipher login
	def decipher_login(self):
		if debug == 1:
			print('[DEBUG] Logging into Decipher (decipher_login())')
		try:
			api.login(self.read_api_token(), "https://v2.decipherinc.com")
			if debug == 1:
				print('[DEBUG] Logged in')
		except:
			print(("[ERROR] ", sys.exc_info()[0]))
			raise

	# Read survey
	def read_survey(self):
		survey = ''
		while len(survey) < 1:
			survey = input("> Enter survey ID: ")
		return survey

	# Download datamap/survey
	def download(self, survey, datatype):
		spinner = Halo(text='Downloading ' + datatype + ' for ' + survey, spinner='dots')
		spinner.start()
		try:
			url_base = "surveys/selfserve/bb5/" + survey + "/" + datatype
			
			result = api.get(url_base, format="json")
			spinner.succeed('Download complete')
			return result
		except:
			# print("[ERROR] ", sys.exc_info()[0])
			spinner.fail('An error occured')
			raise

	# Flatten datamap
	def qmapflatten(self, dl):
		spinner = Halo(text='Flattening the survey datamap...', spinner='dots')
		try:
			out = "\t".join(['question_group', 'question_label', 'question_title', 'col_title', 'row_title', 'question_type', 'val_key', 'val_title']) + "\n"
			for a in dl['variables']:
				out_tmp = ''
				question_group = self.clean_string(a['vgroup'])
				question_label = self.clean_string(a['label'])
				question_title = self.clean_string(a['qtitle'])
				col_title = self.clean_string(a['colTitle'])
				row_title = self.clean_string(a['rowTitle'])
				question_type = self.clean_string(a['type'])
				default = ''
				question_values = self.clean_string(a.get('values', default))
				val_key = ''
				val_title = ''
				if len(question_values) >= 1:
					for b in question_values:
						val_key = self.clean_string(str(b['value']))
						val_title = self.clean_string(str(b['title']))
						out += '\t'.join([question_group, question_label, question_title, col_title, row_title, question_type, val_key, val_title]) + '\n'
				else:
					out += '\t'.join([question_group, question_label, question_title, col_title, row_title, question_type, val_key, val_title]) + '\n'
			spinner.succeed('Completed flattening data')
			return out
		except:
			spinner.fail('An error occured')

	# Get users
	def get_users(self):
		spinner = Halo(text='Downloading user data...', spinner='dots')
		spinner.start()
		try:
			result = api.get('rh/users', sort="-last_login", limit="10", select="login,last_login,active")
			spinner.succeed('User data downloaded')
			return result
		except:
			spinner.fail('User data download failure')

	# Flatten users
	def user_flatten(self, dl):
		spinner = Halo(text='Flattening user data..."', spinner='dots')
		spinner.start()
		try:
			out = '\t'.join(['login', 'last_login', 'active']) + "\n"
			for i in dl:
				out += '\t'.join([str(i['login']), str(i['last_login']), str(i['active'])]) + "\n"
			spinner.succeed('User data flattened')
			return out
		except:
			spinner.fail('Failed to flatten user data')


	# Get survyes
	# Feature request: get_surveys() could check if a list w/ surveys is present on disk (and its date?) prior to attempt to download to shorten waiting time.
	def get_surveys(self):
		spinner = Halo(text='Downloading survey list...', spinner='dots')
		spinner.start()
		try:
			result = api.get('rh/companies/all/surveys')
			spinner.succeed('Survey list downloaded')
			return result
		except:
			spinner.fail('An error occured')

	# Flatten surveys
	def survey_flatten(self, dl):
		spinner = Halo(text='Flattening survey data...', spinner='dots')
		spinner.start()
		try:
			surveys = {}
			for i in range(0, len(dl)):
				path_complete = dl[i]['path']
				path_index = path_complete.rfind("/")
				path = path_complete[path_index+1:]
				title = dl[i]['title']
				surveys.update({title : path})
			spinner.succeed('Data flattened')
			return surveys
		except:
			spinner.fail('An error occured')

	# Search surveys
	def survey_search(self, dl, search_str):
		for i, j in dl.items():
			match = re.match(search_str, i.lower())
			try:
				match_grp = match.group()
				print("{:<50} {:<20}".format(i, j))
			except:
				continue

	def survey_to_str(self, dl):
		spinner = Halo(text='Converting survey dict to str...', spinner='dots')
		spinner.start()
		try:
			out = 'title\tpath_trimmed\n'
			for i, j in dl.items():
				out += "\t".join([i, j]) + "\n"
			spinner.succeed('Conversion complete')
			return out
		except:
			spinner.fail('Conversion failed')

	# Print all surveys
	def survey_print_all(self, dl):
		try:
			for i, j in dl.items():
				print("{:<50} {:<20}".format(i, j))
		except:
			print(("[ERROR] ", sys.exc_info()[0]))
			raise

	# Print quotas
	def print_quotas(self, dl):
		for i in sorted(dl['markers']):
			print("Group: " + str(i))
			limit = dl['markers'][i]['limit']
			pending = dl['markers'][i]['pending']
			oq = dl['markers'][i]['oq']
			complete = dl['markers'][i]['complete']
			pct_complete = "{:.2f}".format((complete / limit)*100)
			print(("\tComplete: {} ({}%)\n\tLimit:\t  {}\n").format(complete, pct_complete, limit))
			if oq > 0:
				print(("\t[WARNING] Overquota: {})").format(oq))

	# Write
	def store(self, output, survey, datatype=''):
		file_name = 'dec'
		if len(survey) > 0:
			file_name += '-' + survey
		if len(datatype) > 0:
			file_name += '-' + datatype
		spinner = Halo(text='Storing data to /Users/' + getpass.getuser() + '/Desktop/' + file_name, spinner='dots')
		spinner.start()
		try:
			f = open('/Users/' + getpass.getuser() + '/Desktop/' + file_name + '.tsv', 'w')
			f.write(output)
			f.close()
			spinner.succeed('Success! Written {} to desktop.\n'.format(file_name))
		except:
			spinner.fail('Error')
			print(("[ERROR] ", sys.exc_info()[0]))
			raise