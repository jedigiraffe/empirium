#!/usr/bin/env python
import re
import os
import sys
import datetime
import optparse
import subprocess
import smtplib

from datetime import datetime
from email.mime.text import MIMEText
from tempfile import NamedTemporaryFile
from templates import INPUT_TEMPLATE, REGEX_TEMPLATE

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
    if not re.match(REGEX_TEMPLATE, contents):
        print("Please follow the correct template!\n",
              "Empirium will now exit, sorry about that...")
        sys.exit(1)

def send_statistics(contents):
    msg = MIMEText(contents)
    msg['Subject'] = None # TODO: Format well
    print(msg)

if __name__ == '__main__':
    # TODO: get editor from command line args
    contents = get_input('subl', INPUT_TEMPLATE.format(mood='',
                                                       phys=''))
    verify_input(contents)
    send_statistics(contents)
