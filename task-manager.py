#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Programs that allows to manipulate tasks
# from the task file.
# Author: Mathias Roesler
# Last modified: 05/22

import sys
import argparse
from taskFunctions import *


def exec_edit(task_file):
    """ Edits a task in the list of tasks.

    Function called with the -e option.
    Arguments:
    task_file -- str, path to the file containing the tasks.

    Returns:

    """
    task_dict = read_tasks(task_file)
    task_id = ''
    edited = [0, 0, 0] # Bit flag

    # Print header.
    print("Available tasks\n")
    for key, value in task_dict.items():
        print(" " + str(key) + ": " + value.get_name())
    print("\nInstructions: ")
    print(" Select one task number only.")
    print(" Press enter to leave field unchanged.")
    print(" Type q to quit.\n")

    try:
        while task_id == '':
            task_id = input("Select task: ")

        if task_id == 'q':
            exit(0)

        else:
            try:
                task_id = int(task_id)
                task_dict[task_id]

            except (ValueError, KeyError):
                sys.stderr.write("Error: invalid task id.\n")
                exit()

        task_name = input("Enter new task: ")

        if task_name == '':
            task_name = task_dict[task_id].get_name()
            edited[0] = 1

        e_date = input("New deadline (DD-MM-YY): ")

        if e_date == '':
            e_date = task_dict[task_id].get_e_date()
            e_date = e_date.strftime("%d-%m-%y")
            edited[1] = 1

        date_error_handle(e_date)

        status_id = input(
            "New urgency status (1: critical, 2:urgent, 3:important, 4:normal): ")

        if status_id == '':
            status_id = str(task_dict[task_id].get_status_id())
            edited[2] = 1

        status_error_handle(status_id)

        if sum(edited) != 0:
            s_date = task_dict[task_id].get_s_date()
            s_date = s_date.strftime("%d-%m-%y")

            edited_task = Task([task_name, s_date, e_date, status_id])
            task_dict[task_id] = edited_task

            save_tasks(task_dict, task_file)

            print("\n Task edited successfully.")

        else:
            print("\n Task unchanged.")

    except KeyboardInterrupt:
        print("\n Abort.")
        exit()


def exec_process(task_file, log_file, status_id_flag):
    """ Processes one or more tasks form the task file by 
    logging it and then removing it from the list.

    Function called with the -l or -d option.
    Arguments:
    task_file -- str, path to the file containing the tasks.
    log_file -- str, path to the log file.
    status_id_flag -- int, indicates if the task is complete or not
        0: task is logged as complete, 1: task is logged as incomplete.

    Returns:

    """
    task_dict = read_tasks(task_file)
    task_ids = ''

    # Print header.
    print("Available tasks\n")
    for key, value in task_dict.items():
        print(" " + str(key) + ": " + value.get_name())
    print("\nInstructions: ")
    print(" Select task numbers only.")
    print(" Separate tasks with a comma and no space.")
    print(" Type q to quit.\n")

    try:
        while task_ids == '':
            task_ids = input("Select tasks: ")

        if task_ids == 'q':
            exit(0)

        task_ids = [int(value) for value in task_ids.split(',')]

        task_dict = process_tasks(task_ids, task_dict, log_file,
                status_id_flag)
        save_tasks(task_dict, task_file)

        if status_id_flag == 0:
            print("\n Tasks successfully logged as completed.")

        elif status_id_flag == 1:
            print("\n Tasks successfully logged as incompleted.")

    except KeyboardInterrupt:
        print("\n Abort.")
        exit()


def exec_read(task_file):
    """ Prepares the tasks for printing and executes the printing.

    Function called with the -r option.
    Arguments:
    task_file -- str, path to the file containing the tasks.

    Returns:

    """
    task_dict = read_tasks(task_file)
    sorted_tasks = sort_tasks(task_dict)
    print_task(sorted_tasks)


def exec_write(task_file):
    """ Write a new task to the task file.

    Function called with the -w option.
    Arguments:
    task_file -- str, path to the file containing the tasks.

    Returns:

    """
    positive = ['y', "yes"]
    negative = ['n', "no"]

    print("Instructions:\n")
    print(" Task name can be anything, type q to quit.")
    print(" Deadline date must be in the format DD-MM-YY.")
    print(" Urgency status: 1: critical, 2:urgent, 3:important, 4:normal.\n")

    write_task(task_file)

    repeat = input("\nWrite another task? (y/n) ")

    while repeat.lower() not in negative:
        write_task(task_file)
        repeat = input("\nWrite another task? (y/n) ")


## Main program ##
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="task-manager", description=
            "Handles the operations for the stored tasks")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--read-tasks", action="store_true", help=
            "prints the list of stored tasks in the terminal")
    group.add_argument("-w", "--write-task", action="store_true", help=
            "writes a task to the list of stored tasks.")
    group.add_argument("-l", "--log-task", action="store_true", help=
            "logs one or more tasks from the list of stored tasks")
    group.add_argument("-d", "--delete-task", action="store_true", help=
            "deletes one or more tasks from the list of stored tasks")
    group.add_argument("-e", "--edit-task", action="store_true", help=
            "edits one task form the list of stored tasks")
    
    args = parser.parse_args() 
    task_file = os.path.join(os.path.expanduser('~'), ".local/var/tasks")
    log_file = os.path.join(os.path.expanduser('~'), ".local/var/log/tasks.log")

    
    if args.read_tasks:
        exec_read(task_file)

    elif args.write_task:
        exec_write(task_file)
        exec_read(task_file)

    elif args.log_task:
        exec_process(task_file, log_file, 0)

    elif args.delete_task:
        exec_process(task_file, log_file, 1)

    elif args.edit_task:
        exec_edit(task_file)

    else:
        parser.print_help()

