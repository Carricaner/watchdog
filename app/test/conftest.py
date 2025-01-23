import pytest


@pytest.fixture(scope="module")
def setup_module():
    print("\nSetup in module scope begins 🐸... ")
    yield {}
    print("\nSetup in module scope finishes 🐸...")


@pytest.fixture(scope="function")
def setup_func():
    print("\nSetup in function scope begins 🦑...")
    yield []
    print("\nSetup in function scope finishes 🦑...")