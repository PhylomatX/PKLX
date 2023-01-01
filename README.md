# PPLX: The Popper Programming Language

The Popper Programming Language is a first experiment to formalize knowledge.

# build process

    python3 -m build
    python3 -m twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pplx==0.2

When you are ready to upload a real package to the Python Package Index you can do much the same as you did in this tutorial, but with these important differences:

Choose a memorable and unique name for your package. You don’t have to append your username as you did in the tutorial, but you can’t use an existing name.

Register an account on https://pypi.org - note that these are two separate servers and the login details from the test server are not shared with the main server.

Use twine upload dist/* to upload your package and enter your credentials for the account you registered on the real PyPI. Now that you’re uploading the package in production, you don’t need to specify --repository; the package will upload to https://pypi.org/ by default.

Install your package from the real PyPI using python3 -m pip install [your-package].