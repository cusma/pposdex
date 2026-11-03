# PPoS Dex

PPoS Dex documentation is built with [`mdBook`](https://rust-lang.github.io/mdBook/).

You can read it [remotely](https://cusma.github.io/pposdex/) or locally.

To read it locally you need to clone this repo and:

* Install Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

* Install `mdBook`

```bash
cargo install mdbook
```

* Serve the repo on [localhost:3000](http://localhost:3000)

```bash
mdbook serve
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
