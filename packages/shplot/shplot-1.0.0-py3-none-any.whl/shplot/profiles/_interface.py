from __future__ import annotations

import contextlib
import typing
from abc import ABC
from collections.abc import Generator
from contextlib import contextmanager
from importlib import reload
from typing import Annotated, Any, Literal, Optional

import matplotlib as mpl
from corgy import Corgy, corgychecker, corgyparser
from cycler import cycler
from matplotlib import pyplot as plt

__all__ = [
    "ProfileBase",
    "ColorProfile",
    "FontProfile",
    "FloatOrStr",
    "PlotScaleProfile",
    "AxesProfile",
    "PlottingProfile",
]


class ProfileBase(Corgy, corgy_make_slots=False):
    """Base class for profiles.

    Profile classes are thin wrappers around subsets of Matplotlib
    parameters. Once instantiated, they can be used to generate a
    dictionary, which can be used to update `matplotlib.rcParams`.

    Profile classes have a dataclass-like interface. All attributes are
    exposed as properties, and can be set either at initialization (as
    keyword arguments) or later. Unless specified otherwise, attributes
    directly correspond to Matplotlib parameters with the same name.

    Examples:
        >>> from shplot.profiles import ColorProfile
        >>> profile = ColorProfile(fg_secondary="gray")
        >>> profile.rc()
        {'grid.color': 'gray', 'legend.edgecolor': 'gray'}

        >>> profile.grid_alpha = 0.5
        >>> profile.rc()  # doctest: +NORMALIZE_WHITESPACE
        {'grid.color': 'gray', 'legend.edgecolor': 'gray',
        'grid.alpha': 0.5}

    """

    def _is_attr_set(self, attr: str) -> bool:
        if attr not in self.attrs():
            raise AttributeError(attr)
        return hasattr(self, attr)

    def rc(self) -> dict[str, Any]:
        """Get profile configuration.

        Returns:
            Dictionary with `rcParams`. Unset attributes are not
            included in the returned dictionary so that different
            profiles can be combined together.
        """
        return self._rc()

    def _rc(self) -> dict[str, Any]:
        raise NotImplementedError

    def config(self, reload_mpl: bool = True) -> None:
        """Update `matplotlib.rcParams` with profile configuration.

        Args:
            reload_mpl: Whether to reload `matplotlib` and `pyplot`
                modules before applying the configuration. Reloading is
                necessary for fonts to be updated.

        Examples:
            >>> import matplotlib as mpl
            >>> print(mpl.rcParams["grid.color"])
            #b0b0b0
            >>> color_prof = ColorProfile(fg_secondary="gray")
            >>> color_prof.config()
            >>> print(mpl.rcParams["grid.color"])
            gray

        """
        self._restore_rc(reload_mpl)
        mpl.rcParams.update(self.rc())

    @contextmanager
    def context(self, reload_mpl: bool = True) -> Generator[None, None, None]:
        """Context manager for `config` method.

        Args:
            reload_mpl: Whether to first reload `matplotlib` and
                `pyplot` modules.

        Examples:
            >>> mpl.rcParams["grid.color"] = 'black'
            >>> print(mpl.rcParams["grid.color"])
            black
            >>> color_prof = ColorProfile(fg_secondary="red")
            >>> with color_prof.context():
            ...     print(mpl.rcParams["grid.color"])
            red
            >>> print(mpl.rcParams["grid.color"])
            black

        """
        current_rc = mpl.rcParams.copy()
        try:
            self.config(reload_mpl)
            yield
        finally:
            self._restore_rc(reload_mpl, current_rc)

    def _restore_rc(
        self, reload_mpl: bool = True, rc: Optional[dict[str, Any]] = None
    ) -> None:
        global mpl, plt  # noqa
        if reload_mpl:
            mpl = reload(mpl)
            plt = reload(plt)
        else:
            mpl.rcParams.clear()
        if rc is None:
            rc = mpl.rcParamsOrig
        mpl.rcParams.update(rc)


class ColorProfile(ProfileBase):
    """Wrapper for color related Matplotlib params."""

    palette: Annotated[list[str], "`axes.prop_cycle` colors."]
    fg: Annotated[
        str, "Primary foreground color, used for text, axes lines, ticks, etc."
    ]
    fg_secondary: Annotated[
        str, "Secondary foreground color, used for grid lines and legend frame."
    ]
    bg: Annotated[str, "Axes and figure face color."]
    grid_alpha: float
    legend_frame_alpha: float
    transparent: Annotated[bool, "Whether to save figures with transparent background."]

    def _rc(self) -> dict[str, Any]:
        rc_dict: dict[str, Any] = {}
        if self._is_attr_set("palette"):
            rc_dict["axes.prop_cycle"] = cycler("color", self.palette)
        if self._is_attr_set("fg"):
            rc_dict["patch.edgecolor"] = self.fg
            rc_dict["hatch.color"] = self.fg
            rc_dict["boxplot.flierprops.color"] = self.fg
            rc_dict["boxplot.flierprops.markeredgecolor"] = self.fg
            rc_dict["boxplot.boxprops.color"] = self.fg
            rc_dict["boxplot.whiskerprops.color"] = self.fg
            rc_dict["boxplot.capprops.color"] = self.fg
            rc_dict["text.color"] = self.fg
            rc_dict["axes.edgecolor"] = self.fg
            rc_dict["axes.labelcolor"] = self.fg
            rc_dict["xtick.color"] = self.fg
            rc_dict["ytick.color"] = self.fg
        if self._is_attr_set("fg_secondary"):
            rc_dict["grid.color"] = self.fg_secondary
            rc_dict["legend.edgecolor"] = self.fg_secondary
        if self._is_attr_set("bg"):
            rc_dict["axes.facecolor"] = self.bg
            rc_dict["figure.facecolor"] = self.bg
            rc_dict["figure.edgecolor"] = self.bg
        if self._is_attr_set("grid_alpha"):
            rc_dict["grid.alpha"] = self.grid_alpha
        if self._is_attr_set("legend_frame_alpha"):
            rc_dict["legend.framealpha"] = self.legend_frame_alpha
        if self._is_attr_set("transparent"):
            rc_dict["savefig.transparent"] = self.transparent
        return rc_dict


class FontProfile(ProfileBase):
    """Wrapper for font related Matplotlib params."""

    family: list[str]
    style: Literal["normal", "italic", "oblique"]
    variant: Literal["normal", "small-caps"]
    weight: Literal[
        "normal", "bold", "100", "200", "300", "400", "500", "600", "700", "800", "900"
    ]
    stretch: Literal[
        "ultra-condensed",
        "extra-condensed",
        "condensed",
        "semi-condensed",
        "normal",
        "semi-expanded",
        "expanded",
        "extra-expanded",
        "ultra-expanded",
        "wider",
        "narrower",
    ]
    serif: list[str]
    sans_serif: list[str]
    monospace: list[str]
    cursive: list[str]
    fantasy: list[str]
    text_usetex: bool
    latex_preamble: list[str]
    math_fontset: Literal[
        "dejavusans", "dejavuserif", "cm", "stix", "stixsans", "custom"
    ]
    custom_math_rm: str
    custom_math_sf: str
    custom_math_tt: str
    custom_math_it: str
    custom_math_bf: str
    custom_math_cal: str
    math_fallback: Literal["cm", "stix", "stixsans", "None"]
    math_default: Literal[
        "rm", "cal", "it", "tt", "sf", "bf", "default", "bb", "frak", "scr", "regular"
    ]
    pgf_rcfonts: bool
    set_pgf_preamble: Annotated[
        bool, "Whether to set `pgf.preamble` using `latex_preamble`."
    ] = True

    def _rc(self) -> dict[str, Any]:
        rc_dict: dict[str, Any] = {}
        if self._is_attr_set("family"):
            rc_dict["font.family"] = self.family
        if self._is_attr_set("style"):
            rc_dict["font.style"] = self.style
        if self._is_attr_set("variant"):
            rc_dict["font.variant"] = self.variant
        if self._is_attr_set("weight"):
            rc_dict["font.weight"] = self.weight
        if self._is_attr_set("stretch"):
            rc_dict["font.stretch"] = self.stretch
        if self._is_attr_set("serif"):
            rc_dict["font.serif"] = self.serif
        if self._is_attr_set("sans_serif"):
            rc_dict["font.sans-serif"] = self.sans_serif
        if self._is_attr_set("monospace"):
            rc_dict["font.monospace"] = self.monospace
        if self._is_attr_set("cursive"):
            rc_dict["font.cursive"] = self.cursive
        if self._is_attr_set("fantasy"):
            rc_dict["font.fantasy"] = self.fantasy
        if self._is_attr_set("text_usetex"):
            rc_dict["text.usetex"] = self.text_usetex
        if self._is_attr_set("latex_preamble"):
            rc_dict["text.latex.preamble"] = "\n".join(self.latex_preamble)
            if self.set_pgf_preamble:
                rc_dict["pgf.preamble"] = rc_dict["text.latex.preamble"]
        if self._is_attr_set("math_fontset"):
            rc_dict["mathtext.fontset"] = self.math_fontset
        if self._is_attr_set("custom_math_rm"):
            rc_dict["mathtext.rm"] = self.custom_math_rm
        if self._is_attr_set("custom_math_sf"):
            rc_dict["mathtext.sf"] = self.custom_math_sf
        if self._is_attr_set("custom_math_tt"):
            rc_dict["mathtext.tt"] = self.custom_math_tt
        if self._is_attr_set("custom_math_bf"):
            rc_dict["mathtext.bf"] = self.custom_math_bf
        if self._is_attr_set("custom_math_it"):
            rc_dict["mathtext.it"] = self.custom_math_it
        if self._is_attr_set("custom_math_cal"):
            rc_dict["mathtext.cal"] = self.custom_math_cal
        if self._is_attr_set("math_fallback"):
            rc_dict["mathtext.fallback"] = self.math_fallback
        if self._is_attr_set("math_default"):
            rc_dict["mathtext.default"] = self.math_default
        if self._is_attr_set("pgf_rcfonts"):
            rc_dict["pgf.rcfonts"] = self.pgf_rcfonts
        return rc_dict


class FloatOrStr(ABC):  # noqa: B024
    """Float or string type."""

    __metavar__ = "float|str"


FloatOrStr.register(float)
FloatOrStr.register(str)


class PlotScaleProfile(ProfileBase):
    """Wrapper for scale related Matplotlib params."""

    font_size: float
    axes_title_size: FloatOrStr
    axes_label_size: FloatOrStr
    xtick_label_size: FloatOrStr
    ytick_label_size: FloatOrStr
    legend_font_size: FloatOrStr
    legend_title_size: FloatOrStr
    figure_title_size: FloatOrStr
    figure_label_size: FloatOrStr
    marker_size: float
    line_width: float
    full_width_in: Annotated[float, "Default figure width in inches."]
    default_aspect_wh: Annotated[float, "Default figure aspect ratio (width/height)."]
    legend_marker_scale: float
    subplot_left: float
    subplot_right: float
    subplot_bottom: float
    subplot_top: float
    subplot_hspace: float
    subplot_wspace: float
    autolayout: bool
    constrained_layout: bool
    constrained_layout_hspace: float
    constrained_layout_wspace: float

    @corgychecker("axes_title_size")
    @corgychecker("axes_label_size")
    @corgychecker("xtick_label_size")
    @corgychecker("ytick_label_size")
    @corgychecker("legend_font_size")
    @corgychecker("legend_title_size")
    @corgychecker("figure_title_size")
    @corgychecker("figure_label_size")
    @staticmethod
    def _check_maybe_relative_size(val: FloatOrStr) -> None:
        if isinstance(val, float):
            return
        if val in (
            "xx-small",
            "x-small",
            "small",
            "medium",
            "large",
            "x-large",
            "xx-large",
        ):
            return
        raise ValueError(f"invalid value for size: {val!r}")

    @corgyparser("axes_title_size")
    @corgyparser("axes_label_size")
    @corgyparser("xtick_label_size")
    @corgyparser("ytick_label_size")
    @corgyparser("legend_font_size")
    @corgyparser("legend_title_size")
    @corgyparser("figure_title_size")
    @corgyparser("figure_label_size")
    @staticmethod
    def _parse_float_or_str(val: str) -> FloatOrStr:
        retval: FloatOrStr = typing.cast(FloatOrStr, val)
        with contextlib.suppress(ValueError):
            retval = typing.cast(FloatOrStr, float(val))
        PlotScaleProfile._check_maybe_relative_size(retval)
        return retval

    def _rc(self) -> dict[str, Any]:
        rc_dict: dict[str, Any] = {}
        if self._is_attr_set("font_size"):
            small_font_size = self.font_size * 3 / 5
            smaller_font_size = self.font_size * 2 / 5
            smallest_font_size = self.font_size * 1 / 5
            rc_dict["font.size"] = self.font_size
            rc_dict["axes.titlepad"] = small_font_size
            rc_dict["axes.labelpad"] = smaller_font_size
            rc_dict["xtick.major.size"] = smaller_font_size
            rc_dict["ytick.major.size"] = smaller_font_size
            rc_dict["xtick.minor.size"] = smallest_font_size
            rc_dict["ytick.minor.size"] = smallest_font_size
            rc_dict["xtick.major.pad"] = smaller_font_size
            rc_dict["ytick.major.pad"] = smaller_font_size
            rc_dict["xtick.minor.pad"] = smaller_font_size
            rc_dict["ytick.minor.pad"] = smaller_font_size
            rc_dict["figure.constrained_layout.h_pad"] = smaller_font_size / 72  # in pt
            rc_dict["figure.constrained_layout.w_pad"] = smaller_font_size / 72
        if self._is_attr_set("axes_title_size"):
            rc_dict["axes.titlesize"] = self.axes_title_size
        if self._is_attr_set("axes_label_size"):
            rc_dict["axes.labelsize"] = self.axes_label_size
        if self._is_attr_set("xtick_label_size"):
            rc_dict["xtick.labelsize"] = self.xtick_label_size
        if self._is_attr_set("ytick_label_size"):
            rc_dict["ytick.labelsize"] = self.ytick_label_size
        if self._is_attr_set("legend_font_size"):
            rc_dict["legend.fontsize"] = self.legend_font_size
        if self._is_attr_set("legend_title_size"):
            rc_dict["legend.title_fontsize"] = self.legend_title_size
        if self._is_attr_set("figure_title_size"):
            rc_dict["figure.titlesize"] = self.figure_title_size
        if self._is_attr_set("figure_label_size"):
            rc_dict["figure.labelsize"] = self.figure_label_size
        if self._is_attr_set("marker_size"):
            rc_dict["lines.markersize"] = self.marker_size
            rc_dict["boxplot.flierprops.markersize"] = self.marker_size
            rc_dict["boxplot.meanprops.markersize"] = self.marker_size
        if self._is_attr_set("line_width"):
            thin_line_width = self.line_width * 2 / 3
            thinner_line_width = self.line_width * 2 / 4
            thinnest_line_width = self.line_width * 2 / 5
            rc_dict["lines.linewidth"] = self.line_width
            rc_dict["lines.markeredgewidth"] = thin_line_width
            rc_dict["patch.linewidth"] = thin_line_width
            rc_dict["hatch.linewidth"] = thin_line_width
            rc_dict["boxplot.whiskers"] = self.line_width
            rc_dict["boxplot.flierprops.markeredgewidth"] = thin_line_width
            rc_dict["boxplot.flierprops.linewidth"] = thin_line_width
            rc_dict["boxplot.boxprops.linewidth"] = thin_line_width
            rc_dict["boxplot.whiskerprops.linewidth"] = thin_line_width
            rc_dict["boxplot.capprops.linewidth"] = thin_line_width
            rc_dict["boxplot.medianprops.linewidth"] = thin_line_width
            rc_dict["boxplot.meanprops.linewidth"] = thin_line_width
            rc_dict["axes.linewidth"] = thinner_line_width
            rc_dict["xtick.major.width"] = thinner_line_width
            rc_dict["ytick.major.width"] = thinner_line_width
            rc_dict["xtick.minor.width"] = thinnest_line_width
            rc_dict["ytick.minor.width"] = thinnest_line_width
            rc_dict["grid.linewidth"] = thinner_line_width
        if self._is_attr_set("full_width_in") or self._is_attr_set("default_aspect_wh"):
            orig_figsize = mpl.rcParamsOrig["figure.figsize"]
            try:
                default_width = self.full_width_in
            except AttributeError:
                default_width = orig_figsize[0]
            try:
                default_aspect = self.default_aspect_wh
            except AttributeError:
                default_aspect = orig_figsize[0] / orig_figsize[1]
            rc_dict["figure.figsize"] = (default_width, default_width / default_aspect)
        if self._is_attr_set("legend_marker_scale"):
            rc_dict["legend.markerscale"] = self.legend_marker_scale
        if self._is_attr_set("subplot_left"):
            rc_dict["figure.subplot.left"] = self.subplot_left
        if self._is_attr_set("subplot_right"):
            rc_dict["figure.subplot.right"] = self.subplot_right
        if self._is_attr_set("subplot_bottom"):
            rc_dict["figure.subplot.bottom"] = self.subplot_bottom
        if self._is_attr_set("subplot_top"):
            rc_dict["figure.subplot.top"] = self.subplot_top
        if self._is_attr_set("subplot_hspace"):
            rc_dict["figure.subplot.hspace"] = self.subplot_hspace
        if self._is_attr_set("subplot_wspace"):
            rc_dict["figure.subplot.wspace"] = self.subplot_wspace
        if self._is_attr_set("autolayout"):
            rc_dict["figure.autolayout"] = self.autolayout
        if self._is_attr_set("constrained_layout"):
            rc_dict["figure.constrained_layout.use"] = self.constrained_layout
        if self._is_attr_set("constrained_layout_hspace"):
            rc_dict["figure.constrained_layout.hspace"] = self.constrained_layout_hspace
        if self._is_attr_set("constrained_layout_wspace"):
            rc_dict["figure.constrained_layout.wspace"] = self.constrained_layout_wspace

        return rc_dict


class AxesProfile(ProfileBase):
    """Wrapper for axes related Matplotlib params."""

    grid_axes: Annotated[
        Literal["x", "y", "both", "none"], "Which axes to draw grid lines on."
    ]
    grid_lines: Annotated[
        Literal["major", "minor", "both"], "Which grid lines to draw."
    ]

    spines: Annotated[
        set[Literal["left", "right", "bottom", "top"]], "Which sides to draw spines on."
    ]
    axis_below: Annotated[
        Literal["all", "line", "none"], "Where to draw axis grid lines and ticks."
    ]

    xticks_top: Annotated[
        Literal["none", "major", "both"], "Which tick lines to draw on the top x-axis."
    ]
    xticks_bottom: Annotated[
        Literal["none", "major", "both"],
        "Which tick lines to draw on the bottom x-axis.",
    ]
    xlabels_top: Annotated[bool, "Whether to show labels on the top x-axis."]
    xlabels_bottom: Annotated[bool, "Whether to show labels on the bottom x-axis."]
    xtick_direction: Annotated[
        Literal["in", "out", "inout"], "Direction of x-axis ticks."
    ]
    xtick_alignment: Annotated[
        Literal["left", "center", "right"], "Alignment of x-axis tick labels."
    ]
    xlabel_position: Annotated[
        Literal["left", "center", "right"], "Position of x-axis label."
    ]

    yticks_left: Annotated[
        Literal["none", "major", "both"], "Which tick lines to draw on the left y-axis."
    ]
    yticks_right: Annotated[
        Literal["none", "major", "both"],
        "Which tick lines to draw on the right y-axis.",
    ]
    ylabels_left: Annotated[bool, "Whether to show labels on the left y-axis."]
    ylabels_right: Annotated[bool, "Whether to show labels on the right y-axis."]
    ytick_direction: Annotated[
        Literal["in", "out", "inout"], "Direction of y-axis ticks."
    ]
    ytick_alignment: Annotated[
        Literal["bottom", "center", "top", "baseline", "center_baseline"],
        "Alignment of y-axis tick labels.",
    ]
    ylabel_position: Annotated[
        Literal["bottom", "center", "top"], "Position of y-axis labels."
    ]

    def _rc(self) -> dict[str, Any]:
        rc_dict: dict[str, Any] = {}

        if self._is_attr_set("grid_axes") and self.grid_axes == "none":
            rc_dict["axes.grid"] = False
        elif self._is_attr_set("grid_axes"):
            rc_dict["axes.grid"] = True
            rc_dict["axes.grid.axis"] = self.grid_axes
        if self._is_attr_set("grid_lines"):
            rc_dict["axes.grid.which"] = self.grid_lines
            if self.grid_lines != "major":
                rc_dict["xtick.minor.visible"] = True
                rc_dict["ytick.minor.visible"] = True

        if self._is_attr_set("spines"):
            rc_dict["axes.spines.left"] = "left" in self.spines
            rc_dict["axes.spines.right"] = "right" in self.spines
            rc_dict["axes.spines.bottom"] = "bottom" in self.spines
            rc_dict["axes.spines.top"] = "top" in self.spines

        if self._is_attr_set("axis_below"):
            if self.axis_below == "all":
                rc_dict["axes.axisbelow"] = True
            elif self.axis_below == "line":
                rc_dict["axes.axisbelow"] = "line"
            elif self.axis_below == "none":
                rc_dict["axes.axisbelow"] = False

        for tb in ("top", "bottom"):
            if self._is_attr_set(f"xticks_{tb}"):
                attr = getattr(self, f"xticks_{tb}")
                if attr == "none":
                    rc_dict[f"xtick.{tb}"] = False
                else:
                    rc_dict[f"xtick.{tb}"] = True
                    rc_dict[f"xtick.major.{tb}"] = True
                    rc_dict[f"xtick.minor.{tb}"] = attr == "both"
            if self._is_attr_set(f"xlabels_{tb}"):
                if getattr(self, f"xlabels_{tb}"):
                    rc_dict[f"xtick.label{tb}"] = True
                    rc_dict[f"xtick.major.{tb}"] = True
                else:
                    rc_dict[f"xtick.label{tb}"] = False

        for lr in ("left", "right"):
            if self._is_attr_set(f"yticks_{lr}"):
                attr = getattr(self, f"yticks_{lr}")
                if attr == "none":
                    rc_dict[f"ytick.{lr}"] = False
                else:
                    rc_dict[f"ytick.{lr}"] = True
                    rc_dict[f"ytick.major.{lr}"] = True
                    rc_dict[f"ytick.minor.{lr}"] = attr == "both"
            if self._is_attr_set(f"ylabels_{lr}"):
                if getattr(self, f"ylabels_{lr}"):
                    rc_dict[f"ytick.label{lr}"] = True
                    rc_dict[f"ytick.major.{lr}"] = True
                else:
                    rc_dict[f"ytick.label{lr}"] = False

        for xy in ("x", "y"):
            if self._is_attr_set(f"{xy}tick_direction"):
                rc_dict[f"{xy}tick.direction"] = getattr(self, f"{xy}tick_direction")
            if self._is_attr_set(f"{xy}tick_alignment"):
                rc_dict[f"{xy}tick.alignment"] = getattr(self, f"{xy}tick_alignment")
            if self._is_attr_set("xlabel_position"):
                rc_dict["xaxis.labellocation"] = self.xlabel_position

        return rc_dict


class PlottingProfile(ProfileBase):
    """Wrapper for color, font, scale, and axes profiles.

    All arguments for initialization are optional, and must be passed as
    keyword arguments. Arguments other than `color`, `font`, `scale`,
    and `axes` are used to update `matplotlib.rcParams` directly, and
    will override any values set by the profile.

    Examples:
        >>> from shplot.profiles import PlottingProfile, ColorProfile
        >>> color_profile = ColorProfile(fg_secondary="gray")
        >>> rc_extra = {"backend": "Agg", "legend.edgecolor": "black"}
        >>> profile = PlottingProfile(color=color_profile, **rc_extra)
        >>> profile.rc()  # doctest: +NORMALIZE_WHITESPACE
        {'grid.color': 'gray', 'legend.edgecolor': 'black',
        'backend': 'Agg'}

    """

    color: ColorProfile
    font: FontProfile
    scale: PlotScaleProfile
    axes: AxesProfile

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        for attr in self.attrs():
            with contextlib.suppress(KeyError):
                del kwargs[attr]
        self._rc_extra = kwargs

    def _rc(self) -> dict[str, Any]:
        rc_dict: dict[str, Any] = {}
        if self._is_attr_set("color"):
            rc_dict.update(self.color.rc())
        if self._is_attr_set("font"):
            rc_dict.update(self.font.rc())
        if self._is_attr_set("scale"):
            rc_dict.update(self.scale.rc())
        if self._is_attr_set("axes"):
            rc_dict.update(self.axes.rc())

        rc_dict.update(self._rc_extra)
        return rc_dict
