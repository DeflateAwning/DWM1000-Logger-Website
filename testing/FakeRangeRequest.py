#!/usr/bin/env python3

# testing/FakeRangeRequest.py

# Fakes a ranging request to the Flask server, including random ranging data, and all other data

import requests

import time, datetime, json, random


##### Define Constants ######
baseURL = "http://127.0.0.1:5000/postRangeData"
#baseURL = "http://enkuo0k7uky6b.x.pipedream.net/postRangeData"
ucDateFormat = '%Y-%m-%d %H:%M:%S.%f' # date format from the microcontroller
#############################

##### Request Options ########

# Time before current time the request came from
minRandomTimeDelta = 0
maxRandomTimeDelta = 0.3
#timeSep = 0.4

minRange = 0.4
maxRange = 15

maxAnchorNum = 5

minReceivePower = -120
maxReceivePower = -20

minRangingRequestCount = 1
maxRangingRequestCount = 9

numTags = 1

sleepTime = 1 # seconds

def getCurrentTime(deltaSeconds=0.0):
	"""
	Returns the current time, in the format of global ucDateFormat, offset by deltaSeconds seconds
	"""

	return (datetime.datetime.now() + datetime.timedelta(seconds=deltaSeconds)).strftime(ucDateFormat)


def randomUniform(min, max, rounding=6):
	return round(random.uniform(min, max), rounding)

def sendARequest(numberOfRangingRequests=5):
	"""
	Sends a single request, with numberOfRangingRequests in the BufferArray list
	"""

	data = {
		#"Date": getCurrentTime(numberOfRangingRequests*timeSep+maxRandomTimeDelta),
		"AnchorNumber": random.randint(1, maxAnchorNum),
		"AccountNumber": 1,

		"BufferArray": []
	}

	for i in range(numberOfRangingRequests):
		data["BufferArray"].append({
				"Range": randomUniform(minRange, maxRange),
				"Date": getCurrentTime(),
				"Success": True,
				"ReceivePower": randomUniform(minReceivePower, maxReceivePower),
				"TagNumber": random.randint(1, numTags)
			})

		time.sleep(random.uniform(minRandomTimeDelta, maxRandomTimeDelta))

	data["Date"] = getCurrentTime()

	# Make the Request
	r = requests.post(baseURL, json=data)

	print("Response: " + str(r.text))
	#print("Response: " + str(r.json()))

if __name__ == "__main__":
	while 1:
		sendARequest(random.randint(minRangingRequestCount, maxRangingRequestCount))
		time.sleep(sleepTime)

