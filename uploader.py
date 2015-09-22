import argparse
import time
from datetime import datetime
from dateutil.tz import gettz
from dateutil.parser import parse
import calendar
import requests
import json
import hashlib


def isANumber(string):
  try:
    i = int(string)
  except (ValueError, TypeError):
    try:
      i = float(string)
    except (ValueError, TypeError):
      return False

  return True

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--api_secret', help="API-SECRET for uploading", required=True)
parser.add_argument('--base_url', help="Base URL of site", required=True)
parser.add_argument('--noninteractive', default=False, action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--timezone', default=gettz( ), type=gettz, help="Timezone to use.")
parser.add_argument('--mmol', help="Data entered as mmol", action='store_true')
#parser.add_argument('--data_type', choices=['sgv', 'cal'],default="sgv")
args = parser.parse_args()

hashed_secret = hashlib.sha1(args.api_secret).hexdigest()

url = "%s/api/v1/entries" % args.base_url
print "Uploading information to " + url
print "Enter 'q' to quit"

prompt = ""
if args.mmol:
  prompt = "Enter current BG (mmol/L): "
else:
  prompt = "Enter current BG (mg/dL): "

while (True):

  bg = raw_input(prompt)

  if (bg == "q"):
    break

  print("Uploading BG " + bg)

  if ( isANumber(bg) == False):
    print "Invalid value entered: %s" % bg
    continue

  if (args.mmol):
    bg = float(bg)
    bg *= 18.018018
    bg = int(bg)
    
  current_time = time.time( )
  now = datetime.fromtimestamp(current_time).replace(tzinfo=args.timezone)

  payload = dict(type='sgv', sgv=bg, date=int(current_time * 1000), dateString=now.isoformat( ))

  if args.debug:
    print "%s\n" % payload

  headers = {'API-SECRET' : hashed_secret,
       'Content-Type': "application/json",
       'Accept': 'application/json'}
  r = requests.post(url, headers=headers, data=json.dumps(payload))
  
  if (r.status_code == 200):
    print "Uploaded successfully"
  else:
    print "%d" % r.status_code 
    print r.text

  if args.noninteractive:
    break
