# multigitminder

![multigitminder](https://github.com/HaydenMacDonald/multigitminder/actions/workflows/multigitminder.yml/badge.svg)

A GitHub Action for logging data points to Beeminder. Configure workflows to trigger on push, pull requests, closed issues, and [any other event supported by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).

## Rationale

Beeminder's integration with GitHub, `gitminder`, allows Beeminder users to capture their programming activity as data for their Beeminder goals. Though this integration is good, it enforces a 1:1 relationship between repos and goals. `multigitminder` allows Beeminder users to connect any number of repos to any number of active goals.

[ DIAGRAM OF POSSIBLE SETUPS ]

## How it Works

![multigitminder flow](multigitminder diagram.png)

## Installation

Implement this action on any repo you own by creating a workflow file in a `.github/workflows/` directory in your repo (see [examples directory](/examples)), specify your goal parameters in the file (see [Inputs](## Inputs) section), and store your Beeminder authorization token as a secret in the repo.

## Inputs
Required
- `auth_token` - Unique authorization token for Beeminder API, stored as a secret in your repo.
- `goal` - Name of the goal.
- `value` - Numeric value of data point input (default value of 1).

Optional
- `comment` - Optional comment about the data point.

## Outputs
- `data` - Resulting data object returned by the Beeminder API.
- `time` - Datetime the data point request was made to the API.

## Secrets & Environmental Variables

`multigitminder` requires a Beeminder auth token as an input, stored as a secret in your chosen repo(s). For help on how to store a secret in your repo, see the [GitHub Docs](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Example Usage

See [examples directory](/examples).

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

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)

## Contributions

Contributions are welcome! See [Contributor's Guide](docs/contributors.md)
