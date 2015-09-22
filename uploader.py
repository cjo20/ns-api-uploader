import argparse
import time
import calendar
import requests
import hashlib

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--api_secret', help="API-SECRET for uploading", required=True)
parser.add_argument('--base_url', help="Base URL of site", required=True)
parser.add_argument('--debug', action='store_true')
#parser.add_argument('--data_type', choices=['sgv', 'cal'],default="sgv")
args = parser.parse_args()

hashed_secret = hashlib.sha1(args.api_secret).hexdigest()

url = "%s/api/v1/entries" % args.base_url
print "Uploading information to " + url
print "Enter 'q' to quit"
while (True):
	bg = raw_input("Enter current BG: ")

	if (bg == "q"):
		break

	print("Uploading BG of " + bg)

	current_time = time.time()
	time_struct = time.localtime(current_time)

	payload = """[{\"type\": \"sgv\",
	\"sgv\": %s,
	\"date\": %d,
	\"dateString\": \"%s\"
	}]
	""" % (bg, current_time * 1000, time.asctime(time_struct))

	if args.debug:
		print "%s\n" % payload

	headers = {'API-SECRET' : hashed_secret,
		   'Content-Type': "application/json",
		   'Accept': 'application/json'}
	r = requests.post(url, headers=headers, data=payload)
	
	if (r.status_code == 200):
		print "Uploaded successfully"
	else:
		print "%d" % r.status_code 
		print r.text
