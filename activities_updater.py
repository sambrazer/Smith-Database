import sqlite3
import datetime
import math
import re

conn = sqlite3.connect('smithsdb.sqlite')
cur = conn.cursor()

# Used to add new activities to Activities table
def add_activities():
    while True:
        num_str = input('Enter the number of activities you want to add. Press enter to end: ')
        if num_str == '':
            break
        # Check Entry
        while True:
            try:
                num = int(num_str)
                break
            except:
                num = -1
            if num == -1:
                num_str = input('Please enter a valid number Press enter to end: ')
            if num_str == '':
                break
        if num_str == '':
            break

        # Add activities to database
        for x in range(num):
            activity = input('Activity ' + str(x + 1) + ': ')
            cur.execute('INSERT OR IGNORE INTO Activities (activity_name, status) VALUES (?, ?)', (activity, 1))
            conn.commit()

        # Continue script. Token = -1 is an invalid answer. Token = 0 is n. Token = 1 is yes. valid is false unless answer is valid
        valid = False
        token = 0
        answer = input('Add more (y/n)? ')
        while True:
            if answer == 'n':
                token = 0
                valid = True
                break
            elif answer == 'y':
                token = 1
                valid = True
                break
            while valid is False:
                    answer = input('Please type a valid answer. Add more (y/n)? ')
                    if answer == 'n':
                        token = 0
                        valid = True
                    elif answer == 'y':
                        token = 1
                        valid = True

        if token == 0 and valid is True:
            break
        elif token == 1 and valid is True:
            continue

# Used to edit the activities table (including active/inactive)
def update_activities():
    while True:
        # Query user for activity and print info
        activity = input('Enter activity you wish to edit. Press enter to end: ')
        print(activity)
        if activity == '':
            break
        cur.execute('SELECT id FROM Activities WHERE activity_name = ?' , (activity, ))
        activity_id = cur.fetchone()
        #Check to see if activity was valid
        while activity_id is None:
            activity = input('Activity not found. Enter activity you wish to edit. Press enter to end: ')
            if activity == '':
                break
            cur.execute('SELECT  FROM Activities WHERE activity_name = ?' , (activity, ))
            activity_id = cur.fetchone()
            if activity == '':
                break

        cur.execute('SELECT status FROM Activities WHERE activity_name = ?', (activity,))
        activity_status = cur.fetchone()
        print('Activity name:', activity)
        print('Activity status: ', activity_status[0])
        print('Activity id (non-editable):', activity_id[0])

        # Write base script for answer. Error checking script later
        while True:
            edit = input('What field would you like to edit (name / status): ')
            if edit == 'name':
                new_name = input('Enter a new activity name: ')
                # Need to write code to make sure new name is not already in existence
                cur.execute('UPDATE Activities SET activity_name = ? WHERE id = ?', (new_name, activity_id[0]))
            if edit == 'status':
                if activity_status[0] == 1:
                    cur.execute('UPDATE Activities SET status = ? WHERE id = ?', (0, activity_id[0]))
                else:
                    cur.execute('UPDATE Activities SET status = ? WHERE id = ?', (1, activity_id[0]))
                cur.execute('SELECT status FROM Activities WHERE id = ?', (activity_id[0],))
                activity_status = cur.fetchone()
                print('New status: ', activity_status[0])

            # Continue script. Token = -1 is an invalid answer. Token = 0 is n. Token = 1 is yes. valid is false unless answer is valid
            valid = False
            answer = input('Edit more (y/n)? ')
            while valid is False:
                if answer == 'n':
                    token = 0
                    valid = True
                elif answer == 'y':
                    token = 1
                    valid = True
                while valid is False:
                        answer = input('Please type a valid answer. Edit more (y/n)? ')
                        if answer == 'n':
                            token = 0
                            valid = True
                        elif answer == 'y':
                            token = 1
                            valid = True
            if token == 0 and valid is True:
                break
            elif token == 1 and valid is True:
                continue
