import os
import time
from datetime import datetime
from pyminder.pyminder import Pyminder

def main():

    username = os.getenv('INPUT_USERNAME')
    auth_token = os.getenv('INPUT_AUTH_TOKEN')
    goal_name = os.getenv('INPUT_GOAL')
    value = os.getenv('INPUT_VALUE')
    comment = os.getenv('INPUT_COMMENT')
    time = datetime.now()

    # Fail if username is not provided
    if (username is None):
        print('Error: Beeminder user name required')
        return

    # Fail if auth token is not provided.
    if (auth_token is None):
        print('Error: Beeminder auth token not found')
        return

	# Fail if no goal provided.
    if (goal_name is None):
        print('Error: Goal name not found.')
        return

	# Fail if no value provided.
    if (value is None):
        print('Error: Data value not found.')
        return

    # Fail if no value provided.
    if (time is None):
        print('Error: Date time not found.')
        return

    # If comment is not provided, use default
    if (comment is None or len(comment) == 0):
        print('Comment not provided. Using default comment.')
        comment = 'via multigitminder API call at ' + time.strftime("%Y-%m-%d %H:%M:%S")

    pyminder = Pyminder(user = username, token = auth_token)

    goal = pyminder.get_goal(goal_name)
    
    # TODO Add comment data after submitting a pull request to pyminder
    #  labels: enhancement
    goal.stage_datapoint(value, time)
    
    goal.commit_datapoints()

    # Output statement
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print('Data point of ' + value + ' added to ' + goal_name + ' at ' + timestamp + ' with comment: ' + comment)


if __name__ == "__main__":
    main()