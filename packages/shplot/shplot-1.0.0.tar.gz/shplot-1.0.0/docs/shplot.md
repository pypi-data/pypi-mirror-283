# shplot package

### *class* shplot.ShPlot(\*\*kwargs)

Bases: `Corgy`

Wrapper around a Matplotlib figure.

`ShPlot` represents a single figure, optionally associated with a
built-in profile from
[`SH_BUILTIN_PROFILES`][shplot.profiles.builtin.SH_BUILTIN_PROFILES].

`ShPlot` inherits from `Corgy`, which provides a dataclass like
interface. Public attributes are exposed as properties, and can also
be set during initialization as keyword-only arguments. All
attributes are optional; refer to their descriptions for details.
Refer to the [Corgy docs][corgy.Corgy] for details on the interface.

### Examples

```pycon
>>> from tempfile import NamedTemporaryFile
>>> from shplot import ShPlot
>>> with NamedTemporaryFile() as save_file:
...     shplot = ShPlot(
...         file=save_file.name,
...         builtin_profile_name="paper",
...         width=3.0,
...         aspect=3/2,
...     )
...     fig, ax = shplot.open()  # also activates paper profile
...     _ = ax.scatter([1, 2, 3], [3, 2, 1])
...     shplot.close()  # saves plot and restores `rcParams`
...     # `ShPlot` can also be used as a context manager.
...     with shplot.context() as (fig, ax):
...         pass
...     # `shplot.close` will be called automatically.
```

```pycon
>>> from argparse import ArgumentParser
>>> argparser = ArgumentParser(add_help=False, usage="")
>>> ShPlot.add_args_to_parser(argparser)
>>> print(
...     argparser.format_help().replace(
...         # This is to prevent the doctest from failing
...         # in Python 3.9, where the 'options' section
...         # has a different name.
...         "optional arguments:", "options:"
...     )
... )
usage:

options:
  --file FILE           Plot save file (extension will be
                        added if not provided).
  --shprofile {paper,book,web_light,web_dark,presentation}
                        Name of a built-in profile.
  --profile-args key=val,...
                        Arguments for the builtin-profile.
                        Refer to the individual profiles for
                        details.
  --width WIDTH         Plot width, in inches (if greater than
                        1), or as a fraction of the configured
                        plot width (if less than or equal to 1).
  --aspect float[;float]
                        Plot aspect ratio, width/height. When
                        provided as a command line argument,
                        can be passed as a single number or a
                        ratio in the form `<WIDTH>;<HEIGHT>`.
>>> args = argparser.parse_args(
...     ["--width", "3", "--aspect", "3;2"]
... )
>>> shplot = ShPlot.from_dict(vars(args))
>>> shplot
ShPlot(width=3.0, aspect=1.5)
```

* **Parameters:**
  **kwargs** (*Any*)

#### *property* file *: str*

Plot save file (extension will be added if not provided).

#### *property* builtin_profile_name *: Literal['paper', 'book', 'web_light', 'web_dark', 'presentation']*

Name of a built-in profile.

#### *property* profile_args *: KeyValuePairs*

Arguments for the builtin-profile. Refer to the individual profiles for details.

#### *property* width *: float*

Plot width, in inches (if greater than 1), or as a fraction of the configured plot width (if less than or equal to 1).

#### *property* aspect *: float*

Plot aspect ratio, width/height. When provided as a command line argument, can be passed as a single number or a ratio in the form `<WIDTH>;<HEIGHT>`.

#### get_plot_size()

Get computed plot size.

* **Returns:**
  Tuple with (width, height) in inches.
* **Return type:**
  tuple[float, float]

### Examples

```pycon
>>> from shplot import ShPlot
>>> plot = ShPlot(width=3.0, aspect=3/2)
>>> plot.get_plot_size()
(3.0, 2.0)
```

#### get_plot_path()

Get the plot save path.

* **Returns:**
  Plot save file (`pathlib.Path` instance) with added
  extension, or `None` if not configured.
* **Return type:**
  *Path* | None

#### NOTE
The path extension depends on the matplotlib backend,
so this method’s return value might change after opening
the plot.

### Examples

```pycon
>>> import matplotlib as mpl
>>> from shplot import ShPlot
>>> mpl.use("agg")
```

```pycon
>>> plot = ShPlot(file="foo", builtin_profile_name="paper")
>>> str(plot.get_plot_path())
'foo.png'
>>> _ = plot.open()
>>> str(plot.get_plot_path())
'foo.pdf'
```

```pycon
>>> plot = ShPlot()
>>> plot.get_plot_path()  # returns `None`
```

```pycon
>>> plot = ShPlot(file="foo.eps")
>>> str(plot.get_plot_path())
'foo.eps'
```

#### open(mosaic=None, \*\*kwargs)

Open the plot, and activate its profile if present.

The plot is opened by calling `matplotlib.pyplot.subplots`, or
`matplotlib.pyplot.subplot_mosaic` if the mosaic argument is
provided. All other arguments are passed to the underlying
functions. Refer to the Matplotlib docs for details.

#### NOTE
It is an error to call this function on an open plot.

* **Parameters:**
  * **mosaic** (*MosaicType*) – If not `None`, plot is opened using
    `subplot_mosaic` instead of `subplots`.
  * **\*\*kwargs** (*Any*) – Passed to `subplots` or `subplot_mosaic`.
* **Returns:**
  (Figure, Axes) tuple, as returned by the underlying
  Matplotlib function. The first value is always an instance
  of `matplotlib.figure.Figure`. The second value depends on
  the arguments; it can be a single `matplotlib.axes.Axes`, or
  an array, or a dictionary.
* **Return type:**
  tuple[Figure, Any]

#### close()

Close the plot.

#### NOTE
It is an error to call this function on an unopened plot.

* **Return type:**
  None

#### context(mosaic=None, \*\*kwargs)

Context manager wrapper which opens and closes the plot.

This function allows `ShPlot` instances to be used in a
`with` statement; the plot is opened on entering the `with`
block, and is closed on exiting. Arguments are passed directly
to `ShPlot.open`.

### Examples

```pycon
>>> from shplot import ShPlot
>>> shplot = ShPlot()
>>> with shplot.context() as (fig, ax):
...     pass
```

* **Parameters:**
  * **mosaic** (*MosaicType*) – If not `None`, plot is opened using
    `subplot_mosaic` instead of `subplots`.
  * **\*\*kwargs** (*Any*) – Passed to `subplots` or `subplot_mosaic`.
* **Returns:**
  Generator context with return value from `ShPlot.open`.
* **Return type:**
  Iterator[tuple[Figure, Any]]

#### NOTE
It is an error to call this function on an opened plot,
or to call `open` while the context is active.

## Subpackages

* [shplot.profiles package](shplot.profiles.md)
