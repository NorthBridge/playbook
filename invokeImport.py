#!/usr/bin/env python

import os
import playbook.backlog.ghimport as imp

path = os.path.dirname(__file__)

if path:
    os.chdir(path)
    
imp.start_server()
