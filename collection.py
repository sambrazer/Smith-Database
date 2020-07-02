import sqlite3
import datetime
import math
import re

conn = sqlite3.connect('smithsdb.sqlite')
cur = conn.cursor()


def collection():
    # Prompt for username and pull the db members_id from Members db
    while True:
        username = input('Enter username: ')

        # Check database
        while True:
            cur.execute('SELECT id FROM Members WHERE username = ?' , (username, ))
            members_id = cur.fetchone()
            if members_id is None:
                username = input('No username found. Please enter a username: ')
            else:
                break

        # Prompt for arrival time and check format. If successful, start_time is time class but start is str which is used for DB
        start = input('Please enter an arrival time (HH:MM format, military time): ')
        correctTime = False
        while correctTime is False:
            start_test = start.split(':')
            if len(start_test) < 2:
                    start = input('Please enter the correct format. Please enter an arrival time (HH:MM format, military time): ')
                    continue
            try:
                start_time = datetime.time(int(start_test[0]), int(start_test[1]))
                correctTime = True
                start = str(start_time)
            except:
                start = input('Ivalid entry. Please enter an arrival time (HH:MM format, military time): ')

        # Prompt for arrival date and check format
        date = input('Enter current date (MM/DD/YYYY): ')
        correctDate = False
        while correctDate is False:
            date_split =  date.split('/')
            if len(date_split) < 2:
                 date = input('Incorrect format. Enter current date (MM/DD/YYYY): ')
                 continue
            try:
                date = datetime.date(int(date_split[2]), int(date_split[0]), int(date_split[1]))
                correctDate = True
            except:
                date = input('Ivalid entry. Incorrect format. Enter current date (MM/DD/YYYY): ')

        # Check to see if activity exists
        activity = input('Enter anticipated activity. Press enter to skip: ')
        while True:
            #Check to see if activity was valid
            cur.execute('SELECT id FROM Activities WHERE activity_name = ?', (activity, ))
            activity_id = cur.fetchone()
            while activity_id is None:
                activity = input('Activity not found. Enter activity you wish to edit. Press enter to skip: ')
                if activity == '':
                    break
                cur.execute('SELECT id FROM Activities WHERE activity_name = ?' , (activity, ))
                activity_id = cur.fetchone()
                if activity == '':
                    break
            break
        cur.execute('SELECT status FROM Activities WHERE activity_name = ?', (activity, ))
        activity_status = cur.fetchone()
        print(username, members_id[0], start, date, activity, activity_id[0], activity_status[0])

        # Insert information collected into Entries db --> Placeholder DB for current data
        cur.execute('''INSERT OR IGNORE INTO Entries (members_id, username, start, date, activity)
        VALUES (?,?,?,?,?)''', (members_id[0], username, start, date, activity))
        cur.execute('SELECT * FROM Entries')
        conn.commit()

        # Print out information for current entry
        entries = cur.fetchall()
        print(entries)
        print('Entries recorded:', len(entries))
        for row in entries:
            print('id:', row[0])
            print('members_id:', row[1])
            print('username:', row[2])
            print('start:', row[3])
            print('date:', row[4])
            print('activity:', row[5])
            print('Inserted into Entries table.')


# Prints entry info)

        #Insert information obtained into Aggregate DB. I STOPPED BECAUSE I FORGOT TO WRITE THE INITIAL DB ENTRIES FOR DAILY COLLECTION
        #cur.execute('''INSERT OR IGNORE INTO
        #Aggregate (members_id, entries_id, username, start, leave, activity)
        #VALUES (?, ?, ?, ?, ?, ?))''', (members_id, ))
def add_entries():
    #Allows a user to input daily information. Asks user if they want to input more after each entry
    while True:
        collection()
    # Continue script. Token = -1 is an invalid answer. Token = 0 is n. Token = 1 is yes. valid is false unless answer is valid
        valid = False
        answer = input('Add more (y/n)? ')
        while valid is False:
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
    print('Entries complete.')
    cur.close()

def view_entries():
    # View Entries script. Token = -1 is an invalid answer. Token = 0 is n. Token = 1 is yes. valid is false unless answer is valid
    while True:
        valid = False
        answer = input('View entires (y/n)? ')
        while valid is False:
            if answer == 'n':
                token = 0
                valid = True
            elif answer == 'y':
                token = 1
                valid = True
            while valid is False:
                    answer = input('Please type a valid answer. View entires (y/n)? ')
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
        # Print out entries
        cur.execute('SELECT * FROM Entries')
        entries = cur.fetchall()
        print(entries)
        print('Entries recorded:', len(entries))
        for row in entries:
            print('id:', row[0])
            print('members_id:', row[1])
            print('username:', row[2])
            print('start:', row[3])
            print('date:', row[4])
            print('activity:', row[5])
            print('/n')


    cur.close()
