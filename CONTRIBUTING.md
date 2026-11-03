# Contributing

[PPoS Dex](https://github.com/cusma/pposdex) project is open source, community
contributions are welcome!

Found a bug or have an idea? Open an [issue](https://github.com/cusma/pposdex/issues).
Want to fix or improve something? Open a pull request.

If you find PPoS Dex a good and useful tool please consider tipping the PPoS Dex
Oracle account to support transaction fees:

`WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ`

## Development

PPoS Dex uses [`uv`](https://docs.astral.sh/uv/) for Python and dependencies
management.

* Install the dependencies and the pre-commit hooks

```bash
uv sync
uv run pre-commit install
```

* Run the unit tests

```bash
uv run pytest
```

* Run the integration tests (requires [AlgoKit](https://github.com/algorandfoundation/algokit-cli)
LocalNet)

```bash
uvx algokit localnet start
uv run pytest -m integration
```

* If you change the CLI options, update the help included in the docs

```bash
UPDATE_DOCS=1 uv run pytest tests/unit/test_docs.py
```

## Documentation

The documentation is an [`mdBook`](https://rust-lang.github.io/mdBook/) in the
`docs` folder. To preview it locally, install `mdBook` (a [prebuilt binary](https://github.com/rust-lang/mdBook/releases),
`brew install mdbook` or `cargo install mdbook --locked`) and run:

```bash
mdbook serve --open
```

The data plots are rendered when the docs are deployed. To include them in
the preview, render them first:

```bash
uv run pposdex timeseries --save
uv run pposdex snapshot --save
uv run python -m pposdex.insights
```

Each chart is saved as SVG in a light and a dark variant: the docs show the
one matching the selected theme.

## Release

Bump the version in `pyproject.toml` on `main`, then push a matching tag:

```bash
git tag v4.0.0
git push origin v4.0.0
```

The release workflow runs the CI on the tag, checks it matches the version,
and creates a GitHub release with the attested wheel and sdist.

## Contributors

* [manuelmauro](https://github.com/manuelmauro) (for letting me discover `mdBook`)
