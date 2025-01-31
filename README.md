# pyins

`pyins` is short of `Python Install Scripts`.

## about

For those Python packages that are in development, installing is a problem.

Creating a new virtual environment is unnecessary, installing into
a shared environment is not a good idea, using a script launcher is
not convenient.

Considering these problems, `pyins` is created.

`pyins` requires a `pyproject.toml` file that defines `project.scripts`
segment, and installed into a virtual environment, it is recommended
to install in editable mode: `pip install -e .`.

How `pyins` works is that it will create hardlinks or copy the scripts to a specified directory.

## cli

For more functions, `pyins` provides a command line interface including
3 sub-commands: `install`, `uninstall`, and `list`.

There is a manifest file to record the installed scripts, from which
the `list` and `uninstall` sub-commands can read.

...
