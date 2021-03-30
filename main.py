import os
import time
import json
from datetime import datetime
from pyminder.pyminder import Pyminder

def main():

    # User variables
    username = os.getenv('INPUT_USERNAME')
    auth_token = os.getenv('INPUT_AUTH_TOKEN')
    goal_name = os.getenv('INPUT_GOAL')
    value = os.getenv('INPUT_VALUE')
    comment = os.getenv('INPUT_COMMENT')
    lang = os.getenv('INPUT_LANG')
    langs = os.getenv('INPUT_LANGS')

    # GitHub variables
    ref = os.getenv('GITHUB_REF')
    hash = os.getenv('GITHUB_SHA')

    # Timestamp
    time = datetime.now()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

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

    # If hash is not provided, else shorten hash to last 7 characters
    if (hash is None or len(hash) == 0):
        hash = ''
    else:
        hash = hash[:7]

    # Shorten reference variable to branch name only
    ref = ref.split('/')[-1]

    # If comment is not provided, use default
    if (comment is None or len(comment) == 0):
        print('Comment not provided. Using default comment.')
        if (len(hash) == 0):
            comment = ref + ' via multigitminder API call at ' + timestamp
        else:
            comment = ref + '@' + hash + ' via multigitminder API call at ' + timestamp

    ## If target language is indicated
    if (lang is not None):
        
        ## Make lang lowercase
        lang = lang.lower()

        ## Parse langs object
        langs = json.load(langs)
        print(lang.keys())
        
        ## For each language in langs, check for target language
        if (lang not in langs.keys()):
            print('Error: repository languages do not match target language')
            return

        
    
    ## Instantiate pyminder
    pyminder = Pyminder(user = username, token = auth_token)

    ## Get goal
    goal = pyminder.get_goal(goal_name)
    
    # TODO Add comment data after submitting a pull request to pyminder
    #  labels: enhancement
    goal.stage_datapoint(value, time)
    
    # Commit datapoints to Beeminder API
    goal.commit_datapoints()

    # Output statement
    if (len(hash) == 0):
        print(ref + ': ' + 'Data point of ' + value + ' added to ' + goal_name + ' at ' + timestamp + " with comment: '" + comment + "'")
    else:
        print(ref + '@' + hash + ': ' + 'Data point of ' + value + ' added to ' + goal_name + ' at ' + timestamp + " with comment: '" + comment + "'")


if __name__ == "__main__":
    main()