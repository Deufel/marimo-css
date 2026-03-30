# marimo-dev
![PyPI version](https://img.shields.io/pypi/v/marimo-css)


> [!WARNING]
> This side-project is under active development and is not an official marimo tool - May 2026


Write CSS in Marimo

```bash
css extract                        # ./notebooks/*.py → ./notebooks/<name>.css
css extract ./src                  # custom input dir
css extract ./src ./dist           # custom input + output dir

css lint                           # lint all .css in project
css lint style.css                 # lint one file

css check                          # extract ./notebooks/*.py → temp → lint → cleanup
css check ./src                    # custom notebook dir
```