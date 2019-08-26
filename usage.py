#!/usr/bin/env
# -*- coding: utf-8 -*-

from deciphertools import tools
from decipher.beacon import api
dec = tools()
dec.decipher_login()
dl = dec.get_users()
output = dec.user_flatten(dl)
dec.store(output, 'users')