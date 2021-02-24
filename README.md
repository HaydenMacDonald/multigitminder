# multigitminder

(A detailed description of what the action does)


## Inputs
Required input arguments.
Optional input arguments.

## Outputs
Required output arguments.
Optional output arguments.

## Secrets & Environmental Variables
Secrets the action uses.
Environment variables the action uses.

## Example Usage

See [action.yml](action.yml)

Log data to Beeminder goal based on commits:
```yaml
steps:
- uses: actions/checkout@master
- uses: multigitminder/log-commit@v1
- run: 
```

For more examples on events that can trigger this workflow see the [GitHub Actions documentation](https://docs.github.com/en/actions/reference/events-that-trigger-workflows).

## License

The scripts and documentation in this project are released under the [MIT License](LICENSE)

## Contributions

Contributions are welcome! See [Contributor's Guide](docs/contributors.md)