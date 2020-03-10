# Sever Setup Information

## General
* If anything is unclear, try referencing documentation from DotWatch-App-Website

## Web Server Setup Instructions
1. Clone the repos
	1. 
2. Install the reqirements:
	1. From both DotWatch-Modules and DotWatch-App-Website (`sudo pip3 install -r requirements.txt`)
3. Create the user database, at a Python command line, using flask-migrate
	1. Create the database
	```bash
	# This might not be all that important
	flask db init
	```

	```python
	# This step is what actually creates the tables apparently
	from app import db
	db.create_all()
	```

	2. Perform migrations as database columns/settings change
	```bash
	flask db migrate -m "Migration Message (similar to commit message), ex: added reset password table columns"
	flask db upgrade
	```


4. 

## Sources of Documentation
* Initial Website Setup/Authentication Tutorial (deleted): https://scotch.io/tutorials/authentication-and-authorization-with-flask-login
* Site cloned from http://www.patricksoftwareblog.com/flask-tutorial/ and https://gitlab.com/patkennedy79/flask_recipe_app/-/tags (version 2.0)
