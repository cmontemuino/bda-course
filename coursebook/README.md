# Coursebook

This repository uses [jupyter-book](https://jupyterbook.org/intro.html).

Course file structure:

```
coursebook/
    - figures/
    - modules/
        - m1/
            - files ...
        - m2/
            - files ...
        ...
    - _config.yml
    - _toc.yml
    requirements.txt
```

## Updating a module

- Add a markdown or jupyter notebook file to the corresponding module. It must contain one
  top-level header, which will be the page link text in the book.

```

coursebook/
    - figures/
    - modules/
        - m1/
            - a_new_resource_file.md
```

- Add the file to the table of contents `_toc.yml`. **Do not include the file extension.**

```
format: jb-book
root: welcome
parts:
  - caption: "Module 1: Introduction"
    chapters:
    - file: modules/m1/a_new_resource_file
  ...
```

- Test the build locally.
    - Run `make init` to update any dependencies, if required.
    - Install `jupyter-book`. If you are using [Poetry](https://python-poetry.org), then running
      `make init` followed by `poetry shell` will be enough. Otherwise, you will need to use `pip` or anotehr solution.
    - Build the book with `make html`. This will generate html files in `coursebook/.build/html`.
    - Inspect the book by opening `coursebook/.build/html/index.html` in a browser.
    - If you want to rebuild after changes, then use `make clean`
- Commiting the HTML files to GitHub is not required. Everything is automatically done with GitHub
  actions.
- Run `make requirements` to update the `requirements.txt` file. You must commit that file in case
  of any changes.

