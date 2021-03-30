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
    target_langs = os.getenv('INPUT_TARGET_LANGS')
    repo_langs = os.getenv('INPUT_REPO_LANGS')

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
        comment = ref + '@' + hash + ' via multigitminder API call at ' + timestamp

    # If target languages are provided
    if (target_langs is not None):
        
        try:
            # Extract target_langs from array string
            target_langs = eval(target_langs)
        except:
            # If only one target language provided, create new array
            target_langs = [ target_langs ]
        
        # Make each language in target_langs lowercase
        target_langs = [ lang.lower() for lang in target_langs ]

        # Parse repo_langs object
        repo_langs = json.loads(repo_langs)
        repo_langs = [ key.lower() for key,value in repo_langs.items() ] 

        # Matching languages
        matched_langs = [lang for lang in target_langs if lang in repo_langs]
        
        # If there is not at least one target language in repo_langs, stop and return error message
        if (len(matched_langs) < 1):
            print('Error: repository languages do not match target language')
            return
        else:  
            for i in matched_langs:
                langs_list += i + ", "
            print('Target languages found: ' + langs_list + '\nLogging data to Beeminder.')

    # Instantiate pyminder
    pyminder = Pyminder(user = username, token = auth_token)

    # Get goal
    goal = pyminder.get_goal(goal_name)
    
    # TODO Add comment data after submitting a pull request to pyminder
    #  labels: enhancement
    goal.stage_datapoint(value, time)
    
    # Commit datapoints to Beeminder API
    goal.commit_datapoints()

    # Output statement
    print(ref + '@' + hash + ': ' + 'Data point of ' + value + ' added to ' + goal_name + ' at ' + timestamp + " with comment: '" + comment + "'")


if __name__ == "__main__":
    main()