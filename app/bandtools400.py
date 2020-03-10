# app/bandtools400.py

# Basic band tools to be used

def convertMetersToSteps(meters):
	"""
	Converts a number of meters to a number of steps

	22.5 inches is an 8-to-5 step exactly, and 22.5 inches = 0.5715 meters
	"""

	if meters is None:
		return 0

	return 0.5715 * meters

def convertStepsToMeters(steps):
	if steps is None:
		return 0 
		
	return steps/0.5715