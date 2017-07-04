# climate

This repository contains support materials for the JDEV 2017 [t4.a06
workshop](http://devlog.cnrs.fr/jdev2017/t4.a06).

Slides from the workshop are bundled with the repository:
[`slides.md`](./slides.md).

**Pro tip**: you can load the `slides.md` file content in a [Monod](https://monod.lelab.tailordev.fr) slidedeck 😉.

## Getting started

Start this workshop by cloning the project:

```bash
$ git clone path/to/project.git
```

Create a python `virtualenv` and install dependencies:

```bash
$ cd project.git
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements-dev.txt
(venv) $ python setup.py develop
```

## Running the test suite

```bash
(venv) $ pytest
```

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License](http://creativecommons.org/licenses/by-sa/4.0/) (see
[LICENSE](./LICENSE)).

Data from `temperature/fixtures/` are part of the [Climate Change: Earth
Surface Temperature
Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data)
Kaggle dataset, licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License](http://creativecommons.org/licenses/by-sa/4.0/).
