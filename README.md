# multigitminder

![multigitminder](https://github.com/HaydenMacDonald/multigitminder/actions/workflows/multigitminder.yml/badge.svg)

A GitHub Action for logging data points to [Beeminder](https://www.beeminder.com/home). Configure workflows to trigger on push, pull requests, closed issues, and [any other event supported by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).

## Rationale

Beeminder's integration with GitHub, [`gitminder`](https://www.beeminder.com/gitminder), allows Beeminder users to capture their programming activity as data for their Beeminder goals. Unfortunately, `gitminder` only tracks commits and issues closed in a single repo or across your whole GitHub account. Conversely, `multigitminder` allows users to connect any number of repos to any number of Beeminder goals based on [any combination of events supported by GitHub Actions](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).  

## How it Works

After configuring a workflow file in your chosen repo(s), GitHub Actions will run `multigitminder` every time your chosen event type occurs. The action uses a simple python script (via [`pyminder`](https://github.com/narthur/pyminder)) to push data points to Beeminder's API. Your Beeminder username and auth token are kept safe, since they are stored as secrets in your GitHub repo(s) and obscured by GitHub Actions.

<img src="/img/multigitminder-diagram.png" alt="multigitminder flow diagram">


## Installation

Implement this action on any repo you own by:
- Creating a workflow file in a `.github/workflows/` directory (see [examples directory](/examples)).
- Specifying your goal parameters in the file (see [Inputs](#Inputs) section).
- Storing your Beeminder username and authorization token as [secrets in the repo](#secrets--environmental-variables).

## Inputs
Required
- `USERNAME` - Your Beeminder username, stored as a secret in your repo.
- `AUTH_TOKEN` - Your unique authorization token for Beeminder API, stored as a secret in your repo.
- `GOAL` - Name of your goal.
- `VALUE` - Value of data point as string (default value of '1').

Optional
- `COMMENT` - Comment about the data point (default: 'via multigitminder API call at [ timestamp ]').
- `TARGET_LANGS` - List of target languages, formatted as a stringified array/list (e.g. `"['python', 'javascript']"`)
- `REPO_LANGS` - List of languages inputted by [fabasoad/linguist-action](https://github.com/marketplace/actions/linguist-action). 

## Outputs
- Print statement confirming the value, goal, timestamp, and comment of data point sent to Beeminder.

## Secrets & Environmental Variables

`multigitminder` requires a **Beeminder username and auth token** as an input, stored as secrets in your chosen repo(s). For help on how to store a secret in your repo, see the [GitHub Docs](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository).

## Example Usage

See [examples directory](/examples).

Log data to a Beeminder goal when pushing to the main branch:
```yaml:examples/multigitminder-push.yml
name: multigitminder-push
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
```

Log data to a Beeminder goal after pushing or closing an issue:
```yaml:examples/multigitminder-push-issue-closed.yml
name: multigitminder-issue-closed
on:
  issues:
    types: [ closed ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
```



See the [GitHub Actions documentation](https://docs.github.com/en/actions/reference/events-that-trigger-workflows) for more events that can trigger this action.

### What if I want specific commits to trigger multigitminder?

Add a [conditional](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idif) to your workflow file like so:

```yaml:examples/multigitminder-specific-commits.yml
name: multigitminder-specific-commits
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    if: "contains(github.event.head_commit.message, '[multigitminder]')" ## THIS LINE HERE
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
```
and include '[multigitminder]' in the commit message of the commits you want to count towards your Beeminder goal.

### What if I want commits to a repo to contribute to multiple Beeminder goals?

Create a workflow file in your repo's `.github/workflows/` directory for each goal, changing the input parameters accordingly.

### What if I want repositories with specific languages contributing to my Beeminder goal?

Use [actions/checkout@v2](https://github.com/actions/checkout) and [fabasoad/linguist-action](https://github.com/marketplace/actions/linguist-action) in the steps preceding `multigitminder` in your workflow file. Then add `linguist-action`'s output data and a list with your target language(s) as inputs for multigitminder (see below). 

```yaml:examples/multigitminder-linguist.yml
name: multigitminder-linguist
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
        uses: HaydenMacDonald/multigitminder@main
        id: multigitminder
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
          TARGET_LANGS: YOUR_TARGET_LANGUAGES_HERE ## e.g. "['python', 'dockerfile', 'javascript']" or simply Python
          REPO_LANGS: ${{ steps.linguist.outputs.data }}

```

### What if I want my commit messages to be the comment on the Beeminder data point?

Add `${{ github.event.head_commit.message }}` as input for the comment variable.

```yaml:examples/multigitminder-commit-message-comment.yml
name: multigitminder-commit-message-comment
on:
  push:
    branches: [ main ]

jobs:
  multigitminder:
    runs-on: ubuntu-latest
    name: multigitminder
    steps:
      - name: multigitminder
        uses: HaydenMacDonald/multigitminder@main
        with:
          USERNAME: ${{ secrets.BEEMINDER_USERNAME }}
          AUTH_TOKEN: ${{ secrets.BEEMINDER_AUTH_TOKEN }}
          GOAL: YOUR_GOAL_NAME_HERE
          COMMENT: ${{ github.event.head_commit.message }}
```

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)

## Contributions

Contributions are welcome! See our [Code of Conduct](/.github/CODE_OF_CONDUCT.md).
