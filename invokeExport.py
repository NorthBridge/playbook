#!/usr/bin/env python

import os
import playbook.backlog.export as export

path = os.path.dirname(__file__)

if path:
    os.chdir(path)
    
export.main()
