#!/usr/bin/env python
from socket import gethostname
if "_" in gethostname():
    print "Error: your username/workspace name has an underscore, which is not allowed in django"
    print "See https://code.djangoproject.com/ticket/20264"
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amazon_api.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
