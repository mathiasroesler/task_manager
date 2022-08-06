#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Class for tasks.


import os
import colorama
from datetime import datetime, timedelta
from colorama import Fore, Style


# Global variables
INFO_BOX_SIZE = 26
TERM_SIZE = os.get_terminal_size()[0]
TASK_BOX_SIZE = TERM_SIZE - INFO_BOX_SIZE - 1
STATUS = ["   late   ", " critical ", "  urgent  ", "  touchy  ", "  normal  "]
COLOR = [Fore.RED, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.GREEN]


class Task:
    ## Init method ##
    def __init__(self, task_items):
        """ Initialise the task with a list of items.

        name -- str, name of the task.
        s_date -- str, start date, format DD-MM-YY.
        e_date -- str, end date, format DD-MM-YY.
        status_id -- int, urgency status_id
            0: late, 1: critical, 2: urgent, 3: important, 4:normal. 
        Arguments:
        task_item -- list[str], list containing the items of
            the task in this order:
            name, start date, end date, status id. 

        Returns:

        """
        self.name = task_items[0]
        self.s_date = datetime.strptime(task_items[1], "%d-%m-%y")
        self.e_date = datetime.strptime(task_items[2], "%d-%m-%y")
        self.status_id = int(task_items[3])

        time_diff = self.e_date - datetime.now()
        self.days_left = time_diff.days + 1 # Task due end of day

        self.update_status_id()

        colorama.init(autoreset=True) # Initialise colorama


    ## Setters ##
    def set_name(self, name):
        self.name = name

    def set_e_date(self, date):
        self.e_date = date

    def set_status_id(self, status_id):
        self.status_id = status_id

    ## Getters ##
    def get_name(self):
        return self.name

    def get_s_date(self):
        return self.s_date

    def get_e_date(self):
        return self.e_date

    def get_status_id(self):
        return self.status_id

    def get_days_left(self):
        return self.days_left

    ## Methods ##
    def log(self, log_file, status_id_flag):
        """ Logs the task to log_file.

        Arguments:
        log_file -- str, path to the log file.
        status_id_flag -- int, indicates if the task is complete or not
            0: task is logged as complete, 1: task is logged as incomplete.

        Returns:
        exit_status_id -- int, exit status_id of the function.
            None: successful log, -1: unsuccessful log.

        """
        try:
            with open(log_file, 'a') as f_handle:
                today = datetime.now().strftime(
                        "%a %d-%m-%y %H:%M:%S")
                
                if status_id_flag == 0:
                    f_handle.write(today + " COMPLETED " + self.get_name() + 
                            ", started on " + self.get_s_date().strftime(
                                "%a %d-%m-%y") + '\n')

                elif status_id_flag == 1:
                    f_handle.write(today + " INCOMPLTED " + self.get_name() +
                            ", started on " + self.get_s_date().strftime(
                                "%a %d-%m-%y") + '\n')

                else:
                    raise Exception("Wrong flag.")

        except:
            exit(-1)


    def task_file_format_str(self):
        """ Creates a string in the task file format.

        Format: name,e_date,s_date,status_id
        e_date and s_date are DD-MM-YY format.
        Arguments:

        Returns:
        formatted_string -- str, formated string for task file.

        """
        s_date = self.s_date.strftime("%d-%m-%y")
        e_date = self.e_date.strftime("%d-%m-%y")

        return ','.join([self.name, s_date, e_date, str(self.status_id)])


    def update_status_id(self):
        """ Resets the status id depending on the number of
        days left.

        late: < 0 days, critical: 0-1 days, urgent: 1-2 days,
        important: 3-4, normal: >= 5.
        Arugments:

        Returns:

        """
        if self.days_left < 0:
            self.status_id = 0

        elif self.days_left <= 1:
            self.status_id = 1

        elif self.days_left <= 2 and self.days_left > 1:
            if self.status_id > 2:
                self.status_id = 2

        elif self.days_left <= 4 and self.days_left > 2:
            if self.status_id > 3:
                self.status_id = 3


    ## Overloaded functions ##
    def __str__(self):
        """ Prints the task.

        Depending on the urgency status, the printing color changes
        0: red, 1: red, 2: yellow, 3: blue, 4: green.
        Arguments:

        Returns:

        """
        task_status_str = "|" + STATUS[self.status_id] + "|"
        days_left_str = 5*" " + str(self.days_left )
        
        if len(self.name) > TASK_BOX_SIZE:
            
            split_name = self.name.split(" ")
            task_name = ""
            tmp_str = ""

            for word in split_name:
                if len(tmp_str) + len(word) < TASK_BOX_SIZE-2:
                    tmp_str +=  word + " "

                else:
                    tmp_str += '\0' + word + " " 
                    task_name += tmp_str
                    tmp_str = ""

            task_name += tmp_str

            split_task_name = task_name.split('\0')
            
            for i in range(len(split_task_name)):
                name_str = " " + split_task_name[i] + (
                        TASK_BOX_SIZE - len(split_task_name[i])) * " "
                name_str = COLOR[self.status_id] + name_str + Fore.RESET

                if i == 0:
                    task_str = name_str + task_status_str + days_left_str + "\n"

                elif i != len(split_task_name) - 1:
                    task_str += name_str + "|" + 10 * " " + "|\n"

            task_str += name_str + "|" + 10 * " " + "|"

        else:
            name_str = " " + self.name + (TASK_BOX_SIZE - len(self.name)) * " "
            name_str = COLOR[self.status_id] + name_str + Fore.RESET
            task_str = name_str + task_status_str + days_left_str


        return Style.BRIGHT + task_str
