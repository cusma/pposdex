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

## Contributors

* [manuelmauro](https://github.com/manuelmauro) (for letting me discover `mdBook`)
