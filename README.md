# PPoS Dex

Algorand Pure Proof of Stake Decentralization Index.

Read the documentation [online](https://cusma.github.io/pposdex/).

## Documentation

The documentation is an [`mdBook`](https://rust-lang.github.io/mdBook/) in the
`docs` folder. To preview it locally, install `mdBook` (a [prebuilt binary](https://github.com/rust-lang/mdBook/releases),
`brew install mdbook` or `cargo install mdbook --locked`) and run:

```bash
mdbook serve --open
```

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
uv run pytest -m "not integration"
```

* Run the integration tests (requires [AlgoKit](https://github.com/algorandfoundation/algokit-cli)
LocalNet)

```bash
uvx algokit localnet start
uv run pytest -m integration
```
