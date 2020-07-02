import sqlite3
import datetime
import math
import re
import prime_db
import collection as collect
import aggregate as agg
import activities_updater as act_up
import table_data as td


conn = sqlite3.connect('smithdb.sqlite')
cur = conn.cursor()

def obtain_answer(question_script, answers, func_to_run):
    question_script_1 = question_script + ' ' + answers + '? '
    question_script_2 = 'Invalid answer. ' + question_script_1
    answer = input(question_script_1)
    answer_choice = answers.split('/')
    answer_1 = answer_choice[0]
    answer_2 = answer_choice[1]
    print(answers, answer, answer_1, answer_2, answer_choice)
    valid_answer = False
    while valid_answer is False:
        if answer == answer_1:
            func_to_run
            valid_answer = True
            break
        elif answer == answer_2:
            valid_answer = True
            break
        else:
            answer = input(question_script_2)
            continue

def obtain_answer_2(question_script, answers, func_to_run_1, func_to_run_2):
    question_script_1 = question_script + ' ' + answers + '? '
    question_script_2 = 'Invalid answer. ' + question_script_1
    answer = input(question_script_1)
    answer_choice = answers.split('/')
    answer_1 = answer_choice[0]
    answer_2 = answer_choice[1]
    valid_answer = False
    while valid_answer is False:
        if answer == answer_1:
            func_to_run_1
            valid_answer = True
            break
        elif answer == answer_2:
            valid_answer = True
            func_to_run_2
            break
        else:
            answer = input(question_script_2)
            continue

# Asks user if they want to initialize database for first time. If y, runs initial_tables from table_data and then prompts for new user info
obtain_answer('Initialize DB.', 'y/n', td.initial_tables())
obtain_answer('Add new users.', 'y/n', prime_db.new_visitor())

# Asks user if they want to add activities. If y, runs add_activities in activities_updater
obtain_answer('Add a new activity.', 'y/n', act_up.add_activities())

# Asks user if they want to update any of the activities, after allowing them to add new ones
obtain_answer('Update an activity.', 'y/n', act_up.update_activities())

# Asks users if they want to start running daily entries. If answer is yes, allows user to
# continue running the daily entries until nothing is returned for username
obtain_answer('Input daily entries.','y/n', collect.collection())

# Asks users if they want to push the daily entries to the aggregate database
obtain_answer('Push data to database.', 'y/n', collect.add_entries())

# Asks users if they want to enter new leave times for the collected data in the aggregate database or view aggregate database
obtain_answer_2('Enter leave data or view Aggregate database.', 'enter data/view data', agg.leave_time_entries(), agg.view_entries())
