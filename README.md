# PPLX: The Popper Programming Language

The Popper Programming Language is a first experiment to formalize knowledge.

# build process

    python3 -m build
    python3 -m twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pplx==0.2
