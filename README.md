# vitals
--> Contains 2 Files 
1. vitals.sh (Shell script) 
2. Flask_notify.py (Python)

How to Execute? [First run python file, followed by bash]

python Flask_notify.py
1. Runs server and all routes are active
2. Can be linked to models.py and other add-ons.
[Note: Contains Rule Engine as a function; This can be modularized by building a new .py script for the same]


bash vitals.sh 
1. This will execute the file; ie generate random health-vitals data (every second) and make an API call to the localhost.
2. After 10[can be varied] iterations, the SOS will be triggered (plainly done as a POC). 


