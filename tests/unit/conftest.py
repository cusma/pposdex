from hypothesis import settings

# Same examples on every run: property tests explore widely but never flake
settings.register_profile("pposdex", derandomize=True, database=None)
settings.load_profile("pposdex")
