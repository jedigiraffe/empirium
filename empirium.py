#!/usr/bin/env python
import re
import os
import sys
import argparse
import datetime
import subprocess
import smtplib

from datetime import date
from email.mime.text import MIMEText
from tempfile import NamedTemporaryFile
from templates import TEMPLATES, REGEX_TEMPLATES

def get_input(editor, initial=''):
    with NamedTemporaryFile(delete=False) as tf:
        tf_name = tf.name
        tf.write(initial)

    if subprocess.call([editor, tf_name, '-w']) != 0: # Wait for file to close
        raise Exception("Sorry my friendo, the editor est muerte!")

    with open(tf_name) as tf:
        contents = tf.read()
        os.remove(tf_name)
        return contents

def verify_input(contents):
    if not re.match(REGEX_TEMPLATES['midday'], contents):
        print("Please follow the correct template!\n" + # Python 2 compatibility
              "Empirium will now exit, sorry about that...")
        sys.exit(1)

def send_statistics(contents, time_of_day):
    msg = MIMEText(contents)
    msg['Subject'] = "{} of {}".format(time_of_day, datetime.date.today()) # TODO: Format well
    print(msg)

if __name__ == '__main__':
    # TODO: get editor from command line args
    contents = get_input('subl', re.sub(r'\{[a-z]+\}', '',
                                        TEMPLATES['midday']))
    verify_input(contents)
    send_statistics(contents, "Morning")
