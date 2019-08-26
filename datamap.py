#!/usr/bin/env
# -*- coding: utf-8 -*-
# Downloading survey question maps

from deciphertools import tools
dec = tools()
dec.decipher_login()
survey = dec.read_survey()
datatype = 'datamap'
dl = dec.download(survey, datatype)
output = dec.qmapflatten(dl)
dec.store(output, survey, datatype)