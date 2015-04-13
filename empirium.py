#!/usr/bin/env python
import re
import os
import sys
import argparse
import datetime
import subprocess
import smtplib

from getpass import getpass
from datetime import datetime, time
from email.mime.text import MIMEText
from tempfile import NamedTemporaryFile
from templates import TEMPLATES, REGEX_TEMPLATES

def get_time_of_day(now):
    if time(5) < now < time(12):
        return 'morning'
    elif time(12) < now < time(18):
        return 'midday'
    else:
        return 'evening'

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

def verify_input(contents, template):
    if not re.match(template, contents, re.S):
        print("Please follow the correct template!\n" + # Python 2 compatibility
              "Empirium will now exit, sorry about that...")
        sys.exit(1)

def send_statistics(contents, time_of_day, simulate):
    msg = MIMEText(contents)
    msg['Subject'] = "{} of {}".format(time_of_day, datetime.now().date())
    msg['From'] = 'empirium.stat@gmail.com'
    msg['To'] = 'empirium.stat@gmail.com'
    if simulate:
        print(msg)
    else:
        try:
            # Use Gmail smtp server
            s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            print("Submitting from user empirium.stat.")
            s.login('empirium.stat', getpass())
            s.sendmail(msg['From'],
                       [msg['To']],
                       msg.as_string())
            print("The deed is done!")
        finally:
            s.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Obtain important statistical data!")
    parser.add_argument('-t', '--time-of-day',
                        type=str,
                        dest='time_of_day',
                        choices=('morning', 'midday', 'evening'))
    parser.add_argument('-e', '--editor',
                        type=str)
    parser.add_argument('--simulate',
                        action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    editor = args.editor or 'subl'
    time_of_day = args.time_of_day or get_time_of_day(datetime.now().time())
    contents = get_input(editor, re.sub(r'\{[a-z]+\}', '',
                                        TEMPLATES[time_of_day]))
    verify_input(contents, REGEX_TEMPLATES[time_of_day])
    send_statistics(contents, time_of_day.capitalize(), args.simulate)
