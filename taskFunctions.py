#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File that contains the functions for
# the task-manager program
# Author: Mathias Roesler
# Last modified: 05/22

import os
import sys
import pyfiglet

from task import Task, TASK_BOX_SIZE, INFO_BOX_SIZE, TERM_SIZE, STATUS
from colorama import Style
from datetime import datetime, timedelta


def print_task(sorted_tasks):
    """ Prints a header and the tasks.
    
    Arguments:
    sorted_tasks -- list[list[Task]], list of Task lists where the index
        of the list represents the urgency status.

    Returns:
    """
    today = datetime.now()
    header_str = "Weekly tasks\n" + today.strftime("%d-%m-%y")

    pyfiglet.print_figlet(header_str, justify='center', width=TERM_SIZE)

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_info = "Week " + today.strftime("%W") + " " + week_start.strftime(
            "%a %d-%m-%y") + " to " + week_end.strftime("%a %d-%m-%y")

    print(Style.BRIGHT + week_info.center(TERM_SIZE) + '\n')
    print(Style.BRIGHT + "Tasks".center(TASK_BOX_SIZE) + 
            " |  Status  | Day(s) left")
    print(Style.BRIGHT + "*-" * (TERM_SIZE // 2) + Style.RESET_ALL)

    for i in range(len(sorted_tasks)):
        for j in range(len(sorted_tasks[i])):
            print(sorted_tasks[i][j])
        
        if len(sorted_tasks[i]) != 0:
            print(Style.BRIGHT + "-" * (TERM_SIZE) + Style.RESET_ALL)


def process_tasks(task_ids, task_dict, task_log_file, status_flag):
    """ Processes the selected tasks in task_dict and removes it. 

    The status flag selects the status for logging the task.
    Arguments:
    task_ids -- list[int], ids of the tasks to log.
    task_dict -- dict[Tasj], dictionnary of Task objects.
    task_log_file -- str, path to the log file.
    status_flag -- int, indicates if the task is complete or not
        0: task is logged as complete, 1: task is logged as incomplete.

    Returns:
    task_dict -- dict[Task], task dictionnary without logged tasks.

    """
    present_ids = []

    for key in task_dict.keys():
        if key in task_ids:
            # Remove the selected task.
            exit_status = task_dict[key].log(task_log_file, status_flag)
            present_ids.append(key)

            if exit_status:
                exit(exit_status)

    # Remove the tasks that have been logged.
    for value in present_ids:
        task_dict.pop(value)

    return task_dict


def read_tasks(task_file):
    """ Reads the tasks from the task file and creates
    Task objects that are placed in a dictionnary.

    Arguments:
    task_file -- str, path to the task file.

    Returns:
    task_dict -- dict[Task], dictionnary containing the Tasks.

    """
    task_dict = dict()
    task_id = 1

    with open(task_file, 'r') as f_handle:
        for line in f_handle.readlines():
            task = Task(line.split(','))
            task_dict[task_id] = task
            task_id += 1
    
    return task_dict


def save_tasks(task_dict, task_file):
    """ Saves the tasks to the task file.

    Arugments:
    task_dict -- dict[Task], dictionnary containing the Tasks.
    task_file -- str, path to the file containing the tasks.

    Returns:

    """
    with open(task_file, 'w') as f_handle:
        for task in task_dict.values():
            f_handle.write(task.task_file_format_str())
            f_handle.write('\n')
    

def sort_by_days(task_list):
    """ Sorts the tasks by the numbers of days left.
    
    The tasks are sorted by increasing number of days left.
    Argument:
    task_list -- list[Task], list of Tasks.

    Return:
    sorted_list -- list[Task], sorted list.

    """
    for n in range(len(task_list)-1):
        is_sorted = True

        for i in range(len(task_list)-1):
            if task_list[i].get_days_left() >  task_list[i+1].get_days_left():
                is_sorted = False
                tmp_value = task_list[i]
                task_list[i] = task_list[i+1]
                task_list[i+1] = tmp_value

        if is_sorted:
            # Exit early if no values have been swapped.
            break

    return task_list


def sort_tasks(task_dict):
    """ Sorts tasks into arrays depending on urgency status.

    The tasks in each array are then sorted by increasing
    numbers of days left.
    Arguments:
    task_dict -- dict[Task], dictionnary containing the Tasks.

    Returns:
    sorted_tasks -- list[list[Task]], list of Task lists where the index
        of the list represents the urgency status.

    """
    sorted_tasks = [[] for i in range(len(STATUS))]

    for task in task_dict.values():
        sorted_tasks[task.get_status_id()].append(task)
    
    for i in range(len(sorted_tasks)):
        sorted_tasks[i] = sort_by_days(sorted_tasks[i])

    return sorted_tasks


def write_task(task_file):
    """ Recuperates the task information from the user and
    writes it to the task file.

    Arguments:
    task_file -- str, path to the file containing the tasks.

    Returns:
    exit_status_id -- int, exit status_id of the function.
        0: successful write, -1: unsuccessful write.
    """
    try:
        task_name = input("Task name: ")

        if task_name.lower() == 'q':
            exit()

        e_date = input("Deadline: ")

        if e_date == '':
            # If no end date assume it is today.
            today = datetime.now()
            e_date = today.strftime("%d-%m-%y")

        date_error_handle(e_date)

        status_id = input("Urgency status: ")

        if status_id == '':
            # If no urgency status assume lowest.
            status_id = '4'

        status_error_handle(status_id)

        s_date = datetime.now()

        if not os.path.exists(task_file):
            open(task_file, 'x')

        with open(task_file, 'a') as f_handle:
            f_handle.write(','.join([task_name, s_date.strftime(
                "%d-%m-%y"), e_date, status_id]))
            f_handle.write('\n')

    except KeyboardInterrupt:
        print("\n Abort.")
        exit()

    print("\nTask written successfully.")


def status_error_handle(status_id):
    """ Handles an urgency status id error.

    Input:
    status_id -- str, user inputed urgency status id value.

    Return:

    """
    try:
        int_status = int(status_id)
        if int_status < 1 or int_status > 5:
            raise ValueError

    except ValueError:
        sys.stderr.write("Error: invalid urgency status.\n")
        exit()


def date_error_handle(e_date):
    """ Handles a deadline error.

    Input:
    e_date -- str, user inputed deadline value.

    Return:

    """
    try:
        datetime.strptime(e_date, "%d-%m-%y")

    except ValueError:
        sys.stderr.write("Error: invalid deadline format.\n")
        exit()
