## Example Workflow Files

All workflow files must be put in the `.github/workflows/` directory of your repo(s).

Log data to a Beeminder goal when pushes and pull requests are made to the main branch:
```yaml
name: multigitminder
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: HaydenMacDonald/multigitminder@v1.0.1
        id: multigitminder
        with:
          auth_token: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          goal: YOUR-GOAL-NAME-HERE
      - run: echo ${{ steps.multigitminder.outputs.data }}
```

Log data to a Beeminder goal after pushing to main branch or closing an issue:
```yaml
name: multigitminder
on:
  push:
    branches: [ main ]
  issues:
    types: [ closed ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: HaydenMacDonald/multigitminder@v1.0.1
        id: multigitminder
        with:
          auth_token: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          goal: YOUR-GOAL-NAME-HERE
      - run: echo ${{ steps.multigitminder.outputs.data }}
```

See the [GitHub Actions documentation](https://docs.github.com/en/actions/reference/events-that-trigger-workflows) for more events that can trigger this action.

### What if I only want specific changes to trigger multigitminder?

Add a [conditional](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idif) to your workflow file like so:

```yaml
name: multigitminder
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  multigitminder:
    if: "contains(github.event.head_commit.message, '[multigitminder]')" ## THIS LINE HERE
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: HaydenMacDonald/multigitminder@v1.0.1
        id: multigitminder
        with:
          auth_token: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          goal: YOUR-GOAL-NAME-HERE
      - run: echo ${{ steps.multigitminder.outputs.data }}
```
and include '[multigitminder]' in the commit message of your chosen commits you want to count towards your Beeminder goal.