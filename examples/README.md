## Example Workflow Files

All workflow files must be put in the `.github/workflows/` directory of your repo(s).

See [GitHub Actions docs](https://docs.github.com/en/actions/reference/events-that-trigger-workflows) for more info on supported events.

Commit workflows

- [push](/examples/multigitminder-push.yml) - A simple workflow that triggers on every push to a specified branch.
- [specific-commits](/examples/multigitminder-specific-commits.yml) - Same workflow as above but with a conditional that prevents `multigitminder` from running if it doesn't contain the target string in the commit message.
- [commit-message-comment](/examples/multigitminder-commit-message-comment.yml) - Adds your commit message as the data point's comment.

Issue workflows

- [issue-closed](/examples/multigitminder-issue-closed.yml) - A simple workflow that triggers on every closed issue. 

Pull Request workflows

- [pull-request](/examples/multigitminder-push.yml) - A simple workflow that triggers on every pull request opened or closed.