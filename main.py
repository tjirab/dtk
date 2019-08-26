#!/usr/bin/env

# Import libs
from decipher.beacon import api
from deciphertools import tools
import csv, sys, re, datetime, dateutil.parser, os, getpass
debug=0

# Set utilities
# reload(sys)
# sys.setdefaultencoding('utf-8')

dec = tools()
dec.validate_modules()

# Tool select
def tool_action():
	exit = 0
	tool_action = -9
	while tool_action not in range(0,5):
		print("""> Choose an action:
  (1) retrieve datamaps
  (2) review Decipher usage
  (3) get quota info
  (4) search or export surveys
  (0) exit""")
		tool_action = input()
		if debug == 1:
			print("[DEBUG] tool_action: {}".format(tool_action))
		try:
			try:
				tool_action = int(tool_action)
			except:
				if debug == 1:
					print("[ERROR] Invalid input")
				break
			if tool_action == 0:
				if debug == 1:
					print("[DEBUG] tool_action: {}".format(tool_action))
				exit = 1
				if debug == 1:
					print("[DEBUG] exit value: {}".format(exit))
				return exit
			if tool_action == 1:
				"""Data map"""
				if debug == 1:
					print("[DEBUG] tool_action: {}".format(tool_action))
				import datamap
				return exit
			elif tool_action == 2:
				"""Decipher Usage"""
				if debug == 1:
					print("[DEBUG] tool_action: {}".format(tool_action))
				import usage
				return exit
			elif tool_action == 3:
				"""Quota"""
				if debug == 1:
					print("[DEBUG] tool_action: {}".format(tool_action))
				import quotas
				return exit
			elif tool_action == 4:
				"""Search / export survey overview"""
				if debug == 1:
					print("[DEBUG] tool_action: {}".format(tool_action))
				import surveys
				return exit
			else:
				print("[ERROR] Invalid input")
				pass	
		except:
			print("[ERROR] {}".format(sys.exc_info()[0]))
			raise

exit = 0
while exit != 1:
	if debug == 1:
		print("[DEBUG] exit value: {}".format(exit))
	exit = tool_action()

print("Bye")