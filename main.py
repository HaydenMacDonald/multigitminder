import os
import time
from datetime import datetime
from pyminder.pyminder import Pyminder

def main():

    user_name = os.getenv('INPUT_USER_NAME')
    auth_token = os.getenv('INPUT_AUTH_TOKEN')
    goal_name = os.getenv('INPUT_GOAL')
    value = os.getenv('INPUT_VALUE')
    comment = os.getenv('INPUT_COMMENT')
    time = datetime.now()

    # Fail if user_name is not provided
    if (user_name is None):
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

    if (comment is None or len(comment) == 0):
        print('Comment not provided. Using default comment.')
        comment = 'via multigitminder API call at ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fail if no value provided.
    if (time is None):
        print('Error: Date time not found.')
        return

    pyminder = Pyminder(user = user_name, token = auth_token)

    goal = pyminder.get_goal(goal_name)

    goal.stage_datapoint(value, time) # TODO add comment value after pull request to pyminder

    goal.commit_datapoints()

if __name__ == "__main__":
    main()