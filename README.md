# multigitminder

![multigitminder](https://github.com/HaydenMacDonald/multigitminder/actions/workflows/multigitminder.yml/badge.svg)

A GitHub Action for logging data points to Beeminder. Configure workflows to trigger on push, pull requests, closed issues, and [any other event support by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).

## Inputs
Required
- `auth_token` - Unique authorization token for Beeminder API.
- `goal` - Name of the goal.
- `value` - Numeric value of data point input (default 1).

Optional
- `comment` - Optional comment about the data point.

## Outputs
- `data` - the resulting data object returned by the Beeminder API.
- `time` - the time the data point request was made to the API.

## Secrets & Environmental Variables

`multigitminder` requires a Beeminder auth token as an input, stored as a secret in your chosen repo. To store a secret in your repo, see the [GitHub Docs](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Example Usage

See [action.yml](action.yml)

Log data to a Beeminder goal when pushes and pull requests are made to the main branch:
```yaml
name: multigitminder
on:
  # Triggers the workflow on push or pull request events but only for the main branch
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2
      # Use current directory
      - uses: HaydenMacDonald/multigitminder@v1.0.1
        id: multigitminder
        with:
          auth_token: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          goal: YOUR-GOAL-NAME-HERE
      - run: echo ${{ steps.multigitminder.outputs.data }}
```

Log data to a Beeminder goal after closing an issue:
```yaml
name: multigitminder
on:
  # Triggers the workflow on push or pull request events but only for the main branch
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2
      # Use current directory
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