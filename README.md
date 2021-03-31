# multigitminder

![multigitminder](https://github.com/HaydenMacDonald/multigitminder/actions/workflows/multigitminder.yml/badge.svg)

A GitHub Action for logging data points to Beeminder. Configure workflows to trigger on push, pull requests, closed issues, and [any other event supported by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).

## Rationale

Beeminder's integration with GitHub, `gitminder`, allows Beeminder users to capture their programming activity as data for their Beeminder goals. Unfortunately, `gitminder` only tracks commits and issues closed in a single repo or across your whole GitHub account. `multigitminder` allows Beeminder users to connect any number of repos to any number of active goals based on [any combination of events supported by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).  

## How it Works

After configuring a workflow file in your chosen repo, GitHub Actions will run `multigitminder` every time your chosen event type occurs. The action uses a simple python script (via [`pyminder`](https://github.com/narthur/pyminder)) to push your data points to Beeminder's API. Your Beeminder username and auth token are kept safe, since they are stored as secrets in your GitHub repo(s) and obscured by GitHub Actions.

![multigitminder flow](/img/multigitminder-diagram.png)

## Installation

Implement this action on any repo you own by:
- Creating a workflow file in a `.github/workflows/` directory (see [examples directory](/examples)).
- Specifying your goal parameters in the file (see [Inputs](#Inputs) section).
- Storing your Beeminder username and authorization token as [secrets in the repo](#secrets--environmental-variables).

## Inputs
Required
- `USERNAME` - your Beeminder username, stored as a secret in your repo.
- `AUTH_TOKEN` - Unique authorization token for Beeminder API, stored as a secret in your repo.
- `GOAL` - Name of the goal.
- `VALUE` - Value of data point as string (default value of '1').

Optional
- `COMMENT` - Comment about the data point (default: 'via multigitminder API call at [ timestamp ]').
- `TARGET_LANGS` - List of languages associated with the goal. Must be formatted as a stringified array/list (e.g. `"['python', 'javascript']"`)
- `REPO_LANGS` - List of languages found by [fabasoad/linguist-action](https://github.com/marketplace/actions/linguist-action). 

## Outputs
- Print statement confirming the value, goal, timestamp, and comment of data point sent to Beeminder.

## Secrets & Environmental Variables

`multigitminder` requires a **Beeminder username and auth token** as an input, stored as secrets in your chosen repo(s). For help on how to store a secret in your repo, see the [GitHub Docs](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Example Usage

See [examples directory](/examples).

Log data to a Beeminder goal when pushing to the main branch:
```yaml
name: multigitminder
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      # Checkout
      - name: Checkout
        uses: actions/checkout@v2
      # multigitminder
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
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
    name: multigitminder
    steps:
      # Checkout
      - name: Checkout
        uses: actions/checkout@v2
      # multigitminder
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
```

See the [GitHub Actions documentation](https://docs.github.com/en/actions/reference/events-that-trigger-workflows) for more events that can trigger this action.

### What if I want specific commits to trigger multigitminder?

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
    name: multigitminder
    steps:
      # Checkout
      - name: Checkout
        uses: actions/checkout@v2
      # multigitminder
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
```
and include '[multigitminder]' in the commit message of the commits you want to count towards your Beeminder goal.

## What if I want my commit messages to be the comment on the Beeminder data point?

Add `${{ github.event.head_commit.message }}` as input for the comment variable.

```yaml
name: multigitminder
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      # Checkout
      - name: Checkout
        uses: actions/checkout@v2
      # multigitminder
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
          VALUE: 1
          COMMENT: ${{ github.event.head_commit.message }}
```

## What if I want repositories with specific languages contributing to my Beeminder goal?

Use [fabasoad/linguist-action](https://github.com/marketplace/actions/linguist-action) in the steps preceding `multigitminder` in your workflow file. Additionally, add linguist's output data and a list with your target language(s) as inputs for multigitminder (see below). 

```yaml
name: multigitminder
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      # Checkout
      - name: Checkout
        uses: actions/checkout@v2
      # linguist
      - name: Linguist Action
        uses: fabasoad/linguist-action@v1.0.2
        id: linguist
        with:
          path: './'
          percentage: true
      # multigitminder
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
          TARGET_LANGS: YOUR_TARGET_LANGUAGES_HERE ## e.g. "['python', 'dockerfile', 'javascript']" or simply 'python'
          REPO_LANGS: ${{ steps.linguist.outputs.data }}
```

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)

## Contributions

Contributions are welcome! See our [Code of Conduct](/.github/CODE_OF_CONDUCT.md).
