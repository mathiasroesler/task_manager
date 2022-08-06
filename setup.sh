#!/bin/bash

PACKAGES=("pyfiglet" "colorama")
SCRIPTS=("taskFunctions.py" "task-manager.py" "task.py" "task-manager")
TASK_DEST="$HOME/.local/var"
EXEC_DEST="$HOME/.local/bin"
LOG_DEST="$HOME/.local/var/log"
TASK_FILE="$TASK_DEST/tasks"
LOG_FILE="$LOG_DEST/tasks.log"

echo "Server program setup"


# Install any required packages
for PACKAGE in "${PACKAGES[@]}"
do
	PRESENT=$(pip3 list | grep $PACKAGE)

	if [[ -z $PRESENT ]]; then
		echo "Required package $PACKAGE missing."
		echo "Installing package."
		pip3 install $PACKAGE
	fi
done


# Check if directory exists and move scripts to destination
if [[ ! -d $EXEC_DEST ]]; then
	echo "Creating directory $EXEC_DEST"
	mkdir $EXEC_DEST
fi

echo "Copying scripts to $EXEC_DEST"

for SCRIPT in "${SCRIPTS[@]}"
do
	cp $SCRIPT $EXEC_DEST
done

# Add executable rights to scripts that need it
chmod +x "$EXEC_DEST/task-manager" 
chmod +x "$EXEC_DEST/task-manager.py"


# Check if directory exists and create task file if needed
if [[ ! -d $TASK_DEST ]]; then
	echo "Creating directory $TASK_DEST"
	mkdir $TASK_DEST
fi

if [[ ! -f $TASK_FILE ]]; then
	echo "Creating task file at $TASK_DEST"
       	touch $TASK_FILE	
fi

# Check if directory exists and create log file if needed
if [[ ! -d $LOG_DEST ]]; then
	echo "Creating directory $LOG_DEST"
	mkdir $LOG_DEST
fi

if [[ ! -f $LOG_FILE ]]; then
	echo "Creating log file at $LOG_DEST"
       	touch $LOG_FILE	
fi

PATH_VAR = echo $PATH | grep "$HOME/.local/bin"

if [[ -z $PATH_VAR ]]; then
	echo "PATH=$PATH:$HOME/.local/bin" >> $HOME/.bashrc
fi

echo "Setup done"
