# CLI task manager

This project is a python based CLI for managing daily tasks. 

## General information

The list of tasks is stored locally in $HOME/.local/var, the folder is created if it does not exist.
The python scripts were written using Python v3.8.10
The bash scripts were written using Bash v5.0.17(1)-release

## Required packages

This list contains the names of the packages that are required to run the scripts. The scripts have been tested using the packages with the specified versions.

   * pyfiglet 0.8.post1
   * colorama 0.4.4

## Installation

The setup.sh script should be run to set everything up. The necessary packages will be installed if they are missing. The scripts will be moved to $HOME/.local/bin, a file to contain the list of tasks will be created at $HOME/.local/var, and a log file will be created at $HOME/.lcoal/var/log. The directories are created if they do not exist.

To setup enter the following commands:

    $ git clone git@github.com:mathiasroesler/task_manager.git
    $ cd task_manager
    $ chmod +x setup.sh
    $ ./setup.sh

The folder can then be removed if needed:

    $ cd ../
    $ rm -rf task_manager

## Usage
###  Commands	

There are five available commands for: reading tasks, writing tasks, logging tasks, deleting tasks and editing tasks.
usage: task-manager [OPTION]
Options:
	-h, --help         show the help message and exit
  	-r, --read-tasks   prints the list of stored tasks in the terminal
  	-w, --write-task   writes a task to the list of stored tasks.
  	-l, --log-task     logs one or more tasks from the list of stored tasks
  	-d, --delete-task  deletes one or more tasks from the list of stored tasks
  	-e, --edit-task    edits one task form the list of stored tasks

### Examples

Begin with adding a task to the list of tasks:

    $ task-manager -w
	
The script will prompt you for the required information: the name of the task, the deadline, and the urgency status. 

You can then view the available tasks:

    $  task-manager -r
	
If you want to update a task and change one of the fields:

    $ task-manager -e
	
When a task is completed you can either log it or delete to remove it from the list of tasks:

    $ task-manager -l
    $ task-manager -d

Logging the task will mark it as COMPLETED in the log file, whereas deleting will mark is as INCOMPLETED.
