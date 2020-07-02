import sqlite3
import math
import datetime
import re

conn = sqlite3.connect('smithsdb.sqlite')
cur = conn.cursor()

def sql_updater(first_name, last_name, b_day, email, phone, username):
    cur.execute('''INSERT OR IGNORE INTO Members (first_name, last_name, b_day, email, phone, username)
    VALUES (? , ?, ?, ?, ?, ?)''', (first_name, last_name, b_day, email, phone, username))
    conn.commit()


# Ask for a new user input. Continues running unless first name is null
def new_visitor():
    while True:
        f_name = input('Enter first name. Press enter to end: ')
        if len(f_name) < 1:
            break
        l_name = input('Enter last name: ')


        b_day = input('Enter birthday (MM/DD/YYYY). Press enter to skip: ')
        # Check format
        correctDate = False
        while False:
            b_day_split =  b_day.split('/')
            if b_day == '':
                break
            elif len(b_day_split) < 2:
                 b_day = input('Incorrect format. Enter birthday (MM/DD/YYYY). Press enter to skip: ')
                 continue
            try:
                b_day = datetime.date(int(b_day_split[2]), int(b_day_split[0]), int(b_day_split[1]))
                correctDate = True
            except:
                b_day = input('Ivalid entry. Enter birthday (MM/DD/YYYY). Press enter to skip: ')


        email = input('Enter email. Press enter to skip: ')
        # Check format
        test = email.split('@')

        while True:
            test =  email.split('@')
            if b_day == '':
                break
            elif len(test) < 2:
                 email = input('Incorrect format. Enter email. Press enter to skip: ')
            else:
                break

        phone = input('Enter phone (XXX-XXX-XXXX): ')
        correctPhone = False
        # Check format
        while correctPhone is False:
            #Split phone given to check format
            try:
                phone_split = phone.split('-')
            except:
                phone_split = -1
            if len(phone_split) < 2:
                phone = input('Incorrect format. Enter phone (XXX-XXX-XXXX): ')
                continue

            # Check the number of values inputted
            phone_check = re.findall('[0-9]+', phone)
            if len(phone_check) != 3:
                phone = input('Incorrect format. Enter phone (XXX-XXX-XXXX): ')
                continue
            phone_test = phone_check[0] + phone_check[1] + phone_check[2]
            if len(phone_test) != 10:
                phone = input('Incorrect format. Enter phone (XXX-XXX-XXXX): ')
                continue
            correctPhone = True

        phone_str = ''
        for item in phone_check:
            phone_str = phone_str + item
        if len(f_name) < 3:
            username = phone_str + f_name
        username = phone_str + f_name[0:3]

        sql_updater(f_name, l_name, b_day, email, phone, username)

# Continue script. Token = -1 is an invalid answer. Token = 0 is n. Token = 1 is yes. valid is false unless answer is valid
        valid = False
        answer = input('Add more users (y/n)? ')
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
                    answer = input('Please type a valid answer. Add more users (y/n)? ')
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
