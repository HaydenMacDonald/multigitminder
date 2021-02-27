// Dependencies
const core = require('@actions/core');
const github = require('@actions/github');
const guid = require('./guid.js');
var beeminder = require('beeminder');

try {
	
	// Get auth_token, goal, and comment input from user
	const auth_token = core.getInput('auth_token');
	const goal = core.getInput('goal');
	const comment = core.getInput('comment');

	// Fail if auth token is not provided.
	if (!auth_token) {
		core.setFailed(`Error: Beeminder auth token not found`);
		return;
	}

	// Return error if no goal provided.
	if (!goal) {
		core.setFailed(`Error: Goal name not found.`)
	}

	// Access API with token
	var bm = beeminder(auth_token);

	// Create a data point for the goal
	bm.createDatapoint(`${goal}`, {	
	  value: 1, // {type: Number, required: true},
	  timestamp: new Date().valueOf() / 1000, // {type: Number, default: now},
	  comment: `${comment}`, // `comment` input defined in action metadata file
	  sendmail: false, // if you want the user to be emailed
	  // requestid allows you to run command again without creating duplicate datapoints
	  requestid: guid.createGuid(),
	}, function (err, result) {
		
		// Output error or result from API
		const data = err || result;
		core.setOutput("data", data);

		// Output timestamp
		const time = (new Date()).toTimeString();
		core.setOutput("time", time);

	});

} catch (error) {
	core.setFailed(error.message);
}