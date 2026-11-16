# Build Status for Lumen

Shows how the last build or test went in the tab title, like
`✓ cargo test · 12s`. A plugin for the
[Lumen](https://github.com/lumenshell/lumen) terminal.

When a build or test (`cargo test`, `make`, `npm test`, `pytest`, …)
finishes, the tab title shows whether it passed and how long it took, until
the next command. Tabs you've named yourself are left alone.

It needs Lumen's [shell integration](https://github.com/lumenshell/lumen/blob/main/docs/shell-integration.md)
to know when a command finishes.

## Install

Open **Plugins** in Lumen's palette, find it under Browse and press `i`, or:

```sh
lumen plugins install sn/build-status
```

It asks for `screen`, to see which command finished, and `panes`, to set the
tab title.

## Development

```sh
PYTHONPATH="$(lumen python-path)" python3 -m unittest discover -s tests
lumen plugins check .
```

It used to come with Lumen as the built-in `build-status`. A `config.toml`
that still lists `build-status` means this plugin.

## License

MIT
