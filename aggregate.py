import sqlite3
import re
import math
import datetime

conn = sqlite3.connect('smithsdb.sqlite')
cur = conn.cursor()

# Reads the latest entries in the Entries DB and uploads them to Aggregate DB
def read_entries():
    cur.execute('''SELECT * FROM Entries''')
    entries = cur.fetchall()
    print('Entries to upload:', len(entries))
    print('/n')

    # Extract info from entries and save to upload into Aggregate
    for row in entries:
        entries_id = row[0]
        members_id = row[1]
        username = row[2]
        start_time = row[3]
        leave_time = datetime.time(0,0)
        date = row[4]
        activity = row[5]
        cur.execute('''INSERT OR IGNORE INTO Aggregate
        (entries_id, members_id, username, start, leave, date, activity) VALUES
        (?, ?, ?, ?, ?, ?, ?)''', (entries_id, members_id, username, str(start_time), str(leave_time), date, activity))
    cur.execute('''SELECT * FROM Aggregate''')
    agg_entries = cur.fetchall()
    conn.commit()
    for row in agg_entries:
        print('id:', row[0])
        print('members_id:', row[1])
        print('username:', row[2])
        print('start:', row[3])
        print('leave:', row[4])
        print('date:', row[5])
        print('activity:', row[6])
        print('Inserted into Aggregate table.')


# Prompt for leave times. If successful, time class leave_time recorded. Need Str class for DB so leave is inputted
def leave_time_entries():
    while True:
        username = input('Enter username: ')
        # Check database for members_id and entries_id
        while True:
            cur.execute('SELECT id FROM Members WHERE username = ?' , (username, ))
            members_id = cur.fetchone()
            if members_id is None:
                username = input('No username found. Please enter a username: ')
            else:
                break

        valid_entry = False
        while valid_entry is False:
            cur.execute('SELECT id FROM Entries WHERE username = ?', (username, ))
            entries_id = cur.fetchone()
            if entries_id is None:
                print('Participant does not have an entry for today.')
                break
            else:
                valid_entry = True
                break
        if valid_entry is False:
            print('Closing program. Please restart aggregate after entering entry data.')
            break

        leave = input('Please enter leaving time (HH:MM format, military time): ')
        correctTime = False
        while correctTime is False:
            leave_split = leave.split(':')
            if len(leave_split) < 2:
                leave = input('Please enter the correct format. Please enter leaving time (HH:MM format, military time): ')
                continue
            try:
                leave_time = datetime.time(int(leave_split[0]), int(leave_split[1]))
                correctTime = True
                leave = str(leave_time)
            except:
                leave = input('Ivalid entry. Please enter leaving time (HH:MM format, military time): ')


        cur.execute('''UPDATE Aggregate SET leave = ? WHERE (members_id, entries_id) = (?, ?)''', (leave, members_id[0], entries_id[0]))
        cur.execute('''SELECT leave FROM Aggregate WHERE (members_id, entries_id) = (?, ?)''', (members_id[0], entries_id[0]))
        cur.execute('''SELECT * FROM Aggregate WHERE (members_id, entries_id) = (?, ?)''', (members_id[0], entries_id[0]))
        new_entries = cur.fetchall()
        conn.commit()
        print('Leave time for', username, 'updated. Updated participant information: ')
        for row in new_entries:
            print('id:', row[0])
            print('members_id:', row[1])
            print('username:', row[2])
            print('start:', row[3])
            print('leave:', row[4])
            print('date:', row[5])
            print('activity:', row[6])
