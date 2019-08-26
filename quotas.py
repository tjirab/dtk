#!/usr/bin/env
# -*- coding: utf-8 -*-

from deciphertools import tools
from decipher.beacon import api

dec = tools()
dec.decipher_login()
survey = dec.read_survey()
datatype = 'quota'
dl = dec.download(survey, datatype)
dec.print_quotas(dl)