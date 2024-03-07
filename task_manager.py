"""
TASK MANAGER by Patrik Krizek
2024© All rights reserved.

0.1 About the project
This is a project of the task manager created in Python. I wanted to create
something more complex with multiple options in the navigation menu. The
application will request you to log in at the beginning. After successfully
login the menu appears. You can choose from: Registering a user, Adding a
task, View all tasks, View my task, Generate reports (admin only), Display
statistics or Exit the application.

0.2 External libraries
I used the "os" and "datetime" external library for this project.

0.3 Functions used in the project
Please find the function descriptions below.

0.4 Potential improvements
Add new functionalities. Divide the main file into modules.

----------------------------------------
Pseudo code for this project.
----------------------------------------

Follow these steps:
    • Use the task_manager.py file, together with the supporting text files
      user.txt and task.txt for this project. Modify task_manager.py to extend
      its functionality. Working on existing code files to extend them is a
      great practice for working in a developer team on an established code
      base.
    • You will notice that the main body of the code requires functionality for
      registering a user, adding a task viewing all tasks, and viewing the
      current user's tasks. However, because there is so much functionality
      needed to complete this, the main body of the loop becomes difficult to
      read. Using the principle of abstraction, refactor the code to create and
      use the following functions:
        ○ reg_user - a function that is called when the user selects "r" to
          register a user.
        ○ add_task - a function that is called when a user selects "a" to add a
          new task.
        ○ view_all - a function that is called when a user selects "va" to view
          all the tasks listed in "tasks.txt".
        ○ view_mine - a function that is called when a user selects "vm" to
          view all the tasks that have been assigned to them.

    • Modify the function called reg_user to make sure that you don't duplicate
      usernames when you add a new user to user.txt. If a user tries to add a
      username that already exists in user.txt, provide a relevant error
      message and allow them to try to add a user with a different username.

    • Add the following functionality when the user selects "wm" to view all
      the tasks assigned to them:
        ○ Display all tasks in a manner that is easy to read. Make sure that
          each task is displayed with a corresponding number that can be used
          to identify the task.
        ○ Allow the user to select either a specific task (by entering a
          number) or input "-1" to return to the main menu.
        ○ If the user selects a specific task, they should be able to choose
          either mark the task as complete or edit the task.
        ○ If the user chooses to mark a task as completed, the "True/False"
          value that describes whether the task has been completed or not
          should be changed to "True".
        ○ If the user chooses to edit the task, the username of the person to
          whom the task is assigned or the due date of the task can be edited.
          The task can only be edited if it has not yet been completed.
        ○ When a selected task is edited update the task.txt file.

    • Add an option to generate reports to the main menu of the application.
      The menu for the admin user should now look something like this:
        "Please select one of the following options:
        r - register user
        a - add task
        va - view all tasks
        vm - view my tasks
        gr - generate reports
        ds - display statistics
        e - exit"

    • When the user chooses to generate reports, two text files, called
      task_overview.txt and user_overview.txt, should be generated. Both these
      text files should output data in a user-friendly, easy-to-read manner.

        ○ taks_overview.txt should contain:
            - the total number of the tasks
            - the total number of completed tasks
            - the total number of uncompleted tasks
            - the total number of tasks that haven't been completed and that are overdue
            - the percentage of the incomplete tasks
            - the percentage of tasks that are overdue

        ○ user_overview.txt should contain:
            - the total number of users registered
            - the total number of tasks
            - for each user also describe:
                - the total number of tasks assigned to that user
                - the percentage of the total number of tasks that have been
                  assigned to that user
                - the percentage of the tasks assigned to that user that have
                  been completed
                - the percentage of the tasks assigned to that user that must
                  still be completed
                - the percentage of the tasks assigned to that user that have
                  not yet been completed and are overdue
    • Nodify the menu option that allows the admin to display statistics so
      that the reports generated are read from tasks.txt and user.txt and
      displayed on the screen in a user-friendly manner. If these text files
      don't exist (because the user hasn't selected to generate them yet),
      first call the code to generate the text files.
"""

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and passwords from the user.txt file to 
    allow a user to log in.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Register a new user
def reg_user(new_username):
            with open("./user.txt", "r+", encoding="utf-8") as file:
                
                # Upload all user names only into the array
                users = []
                for line in file:
                    
                    semicolon_index = 0
                    for i, character in enumerate(line):
                        if character == ";":
                            semicolon_index += i
                            break
                    
                    user_name = line[:(semicolon_index)]
                    users.append(user_name)
                                
                # Check if the new user is not already included in the "users" array
                if not new_username in users:
                    # - Request input of a new password
                    new_password = input("New Password: ")

                    # - Request input of password confirmation.
                    confirm_password = input("Confirm Password: ")

                    # - Check if the new password and confirmed password are the same.
                    if new_password == confirm_password:
                        # - If they are the same, add them to the user.txt file,
                        print("New user added")
                        username_password[new_username] = new_password
                        
                        with open("user.txt", "w") as out_file:
                            user_data = []
                            for k in username_password:
                                user_data.append(f"{k};{username_password[k]}")
                            out_file.write("\n".join(user_data))

                    # - Otherwise you present a relevant message.
                    else:
                        print("Passwords do no match")

                else:
                    print("Current user name is taken. Please enter a different user name.")

# Add a new task
def add_task():
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Display all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Display all my tasks
def view_mine(task_list):
    print("MY TASKS\n")
    for index, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"ID: \t\t {index}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
    
    task_selection = input("Enter the number of the task you want to select (enter -1 to return to the main menu): ")
    return task_selection

# Mark the selected task as completed
def task_completed(selected_task):
    selected_task['completed'] = True
    print("Task marked as complete.")

# Edit the assignee of the selected task
def edit_task_assignee(selected_task):
    new_assignee = input("Enter the new username for the assignee: ")
    selected_task['username'] = new_assignee
    
    print("Assignee updated.")

# Edit the due date of the selected task            
def edit_task_due_date(selected_task, selected_task_index):
    while True:
        try:
            new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
            selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            print("Due date updated.")

            # Update the tasks.txt file
            update_tasks(task_list, selected_task_index, selected_task)

            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

# Update the tasks.txt file
def update_tasks(task_list, selected_task_index, selected_task):
    # Update the task in the task_list
    task_list[selected_task_index] = selected_task

    # Write the updated task_list back to the task.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Generate reports for the admin user
def generate_reports():   
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())

    # Calculate percentages
    percentage_incomplete = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    percentage_overdue = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    # Write task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of Incomplete Tasks: {percentage_incomplete:.2f}%\n")
        task_overview_file.write(f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%\n")

    # Write user_overview.txt
    total_users = len(username_password.keys())
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total Users: {total_users}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")

        for user in username_password.items():
            user_tasks = [task for task in task_list if task['username'] == user]
            total_user_tasks = len(user_tasks)
            percentage_user_tasks = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            completed_user_tasks = sum(1 for task in user_tasks if task['completed'])
            percentage_completed_user_tasks = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            uncompleted_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())
            percentage_uncompleted_overdue_user_tasks = (overdue_user_tasks / uncompleted_user_tasks) * 100 if uncompleted_user_tasks > 0 else 0

            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Total Tasks Assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of Total Tasks Assigned: {percentage_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {percentage_completed_user_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of Uncompleted Tasks: {(100 - percentage_completed_user_tasks):.2f}%\n")
            user_overview_file.write(f"Percentage of Uncompleted and Overdue Tasks: {percentage_uncompleted_overdue_user_tasks:.2f}%\n")

    print("Reports generated successfully.")

# Display statistics for the admin
def display_statistics(username_password, task_list):
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print(f"""\nSTATISTICS
-----------------------------------
Number of users: \t\t {num_users}
Number of tasks: \t\t {num_tasks}
-----------------------------------
""")

#====Menu====
while True:
    # Presenting the menu to the user and 
    # Make sure that the user input is converted to lowercase.
    print()
    menu = input('''\nTASK MANAGER
r   - Registering a user
a   - Adding a task
va  - View all tasks
vm  - View my task
gr  - Generate reports (admin only)                
ds  - Display statistics
e   - Exit
Select one of the following options above: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")
        reg_user(new_username)

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person to whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.
        '''
        # - Request input of a user name to assign the task
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        add_task()

    elif menu == 'va':
        '''Reads the task from the task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labeling). 
        '''
        view_all()    

    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labeling).
        '''
        if len(task_list) == 0:
            print("Currently, there are no tasks assigned to you.")

        else:
            # Display all my tasks and return a selected task
            task_selection = view_mine(task_list)

            # Return to the main menu
            if task_selection == '-1':
                continue

            elif task_selection.isdigit():
                selected_task_index = int(task_selection)
                
                # Check if the task is in the list and the current username
                if 0 <= selected_task_index < len(task_list) and task_list[selected_task_index]['username'] == curr_user:
                    selected_task = task_list[selected_task_index]
                    
                    # Print the task and sub-menu
                    task_action = input(f"""\nSELECTED TASK:
Title: {selected_task['title']} 
Description: {selected_task['description']} 
Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)} 
Completed: {'Yes' if selected_task['completed'] else 'No'}
                    
1   - Mark as complete
2   - Edit task
-1  - Return to the main menu
Select an action: """)
                                                
                    if task_action == '1' and not selected_task['completed']:
                        # Mark the selected task as completed
                        task_completed(selected_task)    

                    elif task_action == '2' and not selected_task['completed']:
                        edit_field = input(f"""\nEDIT TASK FIELD
1   - Assignee
2   - Due date
Select a field to edit: """)
                        
                        # Update the tasks.txt file
                        update_tasks(task_list, selected_task_index, selected_task)
                            
                        if edit_field == '1':
                            # Edit the assignee of the selected task
                            edit_task_assignee(selected_task)

                        elif edit_field == '2':
                            # Edit the due date of the selected task            
                            edit_task_due_date(selected_task, selected_task_index)

                        else:
                            print("Invalid option.")
                    elif task_action == '-1':
                        # Go back to the main menu
                        continue
                    else:
                        print("Invalid option.")
                else:
                    print("Invalid task selection.")
            else:
                print("Invalid input for task selection.")

    elif menu == "gr" and curr_user== "admin":
            # Generate reports for the admin - task_overview.txt and user_overview.txt
            generate_reports()

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about the number of users
            and tasks.'''
        #Displat statistics for admin        
        display_statistics(username_password, task_list)
        
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")