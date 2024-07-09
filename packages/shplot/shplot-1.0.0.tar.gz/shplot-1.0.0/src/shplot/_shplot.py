from __future__ import annotations

from collections.abc import Iterator, Hashable
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, TypeVar, Union

import matplotlib as mpl
from corgy import Corgy, corgychecker, corgyparser
from corgy.types import KeyValuePairs
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.typing import HashableList

from .profiles.builtin import SH_BUILTIN_PROFILES

__all__ = ["ShPlot"]

_T = TypeVar("_T")
MosaicType = Union[str, list[HashableList[_T]], list[HashableList[Hashable]], None]


class ShPlot(Corgy):
    """Wrapper around a Matplotlib figure.

    `ShPlot` represents a single figure, optionally associated with a
    built-in profile from
    [`SH_BUILTIN_PROFILES`][shplot.profiles.builtin.SH_BUILTIN_PROFILES].

    `ShPlot` inherits from `Corgy`, which provides a dataclass like
    interface. Public attributes are exposed as properties, and can also
    be set during initialization as keyword-only arguments. All
    attributes are optional; refer to their descriptions for details.
    Refer to the [Corgy docs][corgy.Corgy] for details on the interface.

    Examples:
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
        ... )  # doctest: +NORMALIZE_WHITESPACE
        usage:
        <BLANKLINE>
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

    """

    file: Annotated[str, "Plot save file (extension will be added if not provided)."]
    builtin_profile_name: Annotated[
        Literal["paper", "book", "web_light", "web_dark", "presentation"],
        "Name of a built-in profile.",
        ["--shprofile"],
    ]
    profile_args: Annotated[
        KeyValuePairs,
        "Arguments for the builtin-profile. Refer to the individual "
        "profiles for details.",
    ]
    width: Annotated[
        float,
        "Plot width, in inches (if greater than 1), or as a "
        "fraction of the configured plot width (if less than or equal to 1).",
    ]
    aspect: Annotated[
        float,
        "Plot aspect ratio, width/height. When provided as a command line "
        "argument, can be passed as a single number or a ratio in the form "
        "`<WIDTH>;<HEIGHT>`.",
    ]

    __slots__ = ("_fig", "_ax", "_profile", "_profile_ctx")

    def __init__(self, **kwargs: Any) -> None:
        if "profile_args" in kwargs and not isinstance(
            kwargs["profile_args"], KeyValuePairs
        ):
            kwargs["profile_args"] = KeyValuePairs(kwargs["profile_args"])
        super().__init__(**kwargs)
        self._fig: Optional[Figure] = None
        self._ax: Any = None
        self._profile_ctx: Any = None
        if not hasattr(self, "builtin_profile_name"):
            self._profile = None
            return

        profile_args = getattr(self, "profile_args", {})
        self._profile = SH_BUILTIN_PROFILES[self.builtin_profile_name](**profile_args)

    @corgyparser("aspect", metavar="float[;float]")
    @staticmethod
    def _parse_aspect(s: str) -> float:
        _s_parts = s.split(";")
        if len(_s_parts) == 1:
            return float(_s_parts[0])
        if len(_s_parts) == 2:
            return float(_s_parts[0]) / float(_s_parts[1])
        raise ValueError("expected one or two values")

    @corgychecker("width", "aspect")
    @staticmethod
    def _ensure_non_negative(val: float) -> None:
        if val <= 0:
            raise ValueError("expected positive value")

    def get_plot_size(self) -> tuple[float, float]:
        """Get computed plot size.

        Returns:
            Tuple with (width, height) in inches.

        Examples:
            >>> from shplot import ShPlot
            >>> plot = ShPlot(width=3.0, aspect=3/2)
            >>> plot.get_plot_size()
            (3.0, 2.0)

        """
        cfg_width, cfg_height = mpl.rcParams["figure.figsize"]

        plot_width: float
        try:
            plot_width = self.width if self.width > 1 else cfg_width * self.width
        except AttributeError:
            plot_width = cfg_width

        plot_aspect: float
        try:
            plot_aspect = self.aspect
        except AttributeError:
            plot_aspect = cfg_width / cfg_height

        plot_height = plot_width / plot_aspect
        return (plot_width, plot_height)

    def get_plot_path(self) -> Optional[Path]:
        """Get the plot save path.

        Returns:
            Plot save file (`pathlib.Path` instance) with added
            extension, or `None` if not configured.

        Note:
            The path extension depends on the matplotlib backend,
            so this method's return value might change after opening
            the plot.

        Examples:
            >>> import matplotlib as mpl
            >>> from shplot import ShPlot
            >>> mpl.use("agg")

            >>> plot = ShPlot(file="foo", builtin_profile_name="paper")
            >>> str(plot.get_plot_path())
            'foo.png'
            >>> _ = plot.open()
            >>> str(plot.get_plot_path())
            'foo.pdf'

            >>> plot = ShPlot()
            >>> plot.get_plot_path()  # returns `None`

            >>> plot = ShPlot(file="foo.eps")
            >>> str(plot.get_plot_path())
            'foo.eps'

        """
        try:
            plot_path = Path(self.file)
            if plot_path.suffix:
                return plot_path
            ext = "." + mpl.rcParams["savefig.format"]
            return plot_path.with_suffix(ext)
        except AttributeError:
            return None

    def open(self, mosaic: MosaicType = None, **kwargs: Any) -> tuple[Figure, Any]:
        """Open the plot, and activate its profile if present.

        The plot is opened by calling `matplotlib.pyplot.subplots`, or
        `matplotlib.pyplot.subplot_mosaic` if the mosaic argument is
        provided. All other arguments are passed to the underlying
        functions. Refer to the Matplotlib docs for details.

        Note:
            It is an error to call this function on an open plot.

        Args:
            mosaic: If not `None`, plot is opened using
                `subplot_mosaic` instead of `subplots`.
            **kwargs: Passed to `subplots` or `subplot_mosaic`.

        Returns:
            (Figure, Axes) tuple, as returned by the underlying
            Matplotlib function. The first value is always an instance
            of `matplotlib.figure.Figure`. The second value depends on
            the arguments; it can be a single `matplotlib.axes.Axes`, or
            an array, or a dictionary.
        """
        if self._fig is not None:
            raise TypeError("plot already open")
        if self._profile is not None:
            self._profile_ctx = self._profile.context()
            self._profile_ctx.__enter__()
        if mosaic is not None:
            self._fig, self._ax = plt.subplot_mosaic(mosaic, **kwargs)
        else:
            self._fig, self._ax = plt.subplots(**kwargs)
        self._fig.set_size_inches(self.get_plot_size())
        return (self._fig, self._ax)

    def close(self) -> None:
        """Close the plot.

        Note:
            It is an error to call this function on an unopened plot.
        """
        if self._fig is None:
            raise TypeError("plot not open")
        if (plot_path := self.get_plot_path()) is not None:
            self._fig.savefig(plot_path)
        plt.close(self._fig)
        if self._profile is not None:
            self._profile_ctx.__exit__(None, None, None)
            self._profile_ctx = None
        self._fig = self._ax = None

    @contextmanager
    def context(
        self, mosaic: MosaicType = None, **kwargs: Any
    ) -> Iterator[tuple[Figure, Any]]:
        """Context manager wrapper which opens and closes the plot.

        This function allows `ShPlot` instances to be used in a
        `with` statement; the plot is opened on entering the `with`
        block, and is closed on exiting. Arguments are passed directly
        to `ShPlot.open`.

        Examples:
            >>> from shplot import ShPlot
            >>> shplot = ShPlot()
            >>> with shplot.context() as (fig, ax):
            ...     pass

        Args:
            mosaic: If not `None`, plot is opened using
                `subplot_mosaic` instead of `subplots`.
            **kwargs: Passed to `subplots` or `subplot_mosaic`.

        Returns:
            Generator context with return value from `ShPlot.open`.

        Note:
            It is an error to call this function on an opened plot,
            or to call `open` while the context is active.
        """
        self.open(mosaic, **kwargs)
        try:
            assert self._fig is not None
            yield (self._fig, self._ax)
        finally:
            self.close()
