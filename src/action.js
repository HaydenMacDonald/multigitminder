const core = require('@actions/core');
const github = require('@actions/github');
const guid = require('./guid.js');
var beeminder = require('beeminder');
// var auth_token = '';
var bm = beeminder(auth_token);

try {
	
	// Output timestamp
	const time = (new Date()).toTimeString();
	core.setOutput("time", time);
	
	// Get comment input from user
	const auth_token = core.getInput('auth_token');
	const goal = core.getInput('goal');
	const comment = core.getInput('comment');

	bm.createDatapoint('multigitminder', {	
	  value: 1, // {type: Number, required: true},
	  timestamp: new Date().valueOf() / 1000, // {type: Number, default: now},
	  comment: '${comment}', // `comment` input defined in action metadata file
	  sendmail: false, // if you want the user to be emailed
	  // requestid allows you to run command again without creating duplicate datapoints
	  requestid: guid.createGuid(),
	}, function (err, result) {
		
		// Output error or result from API
		console.log(err || result); 
	});

} catch (error) {
	core.setFailed(error.message);
}

// try {
  // // `who-to-greet` input defined in action metadata file
  // const nameToGreet = core.getInput('who-to-greet');
  // console.log(`Hello ${nameToGreet}!`);
  // const time = (new Date()).toTimeString();
  // core.setOutput("time", time);
  // // Get the JSON webhook payload for the event that triggered the workflow
  // const payload = JSON.stringify(github.context.payload, undefined, 2)
  // console.log(`The event payload: ${payload}`);
// } catch (error) {
  // core.setFailed(error.message);
// }