from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, Optional, Union

from ._interface import (
    AxesProfile,
    ColorProfile,
    FontProfile,
    PlotScaleProfile,
    PlottingProfile,
)

__all__ = [
    "SH_BUILTIN_PROFILES",
    "ShPaperProfile",
    "ShBookProfile",
    "ShWebProfile",
    "ShPresentationProfile",
    "CUD_PALETTE",
    "ShLightCUDProfile",
    "BSLightCUDProfile",
    "BSDarkCUDProfile",
    "ShScaleProfile",
    "ShPaperScaleProfile",
    "ShBookScaleProfile",
    "ShWebScaleProfile",
    "ShPresentationScaleProfile",
    "ShFontsetupFontProfile",
    "ShPGFRcFontsFontProfile",
]

############################################################
# COLOR PROFILES

CUD_PALETTE = [
    "#000000",
    "#e69f00",
    "#56b4e9",
    "#009e73",
    "#f0e442",
    "#0072b2",
    "#d55e00",
    "#cc79a7",
]
"""Color Universal Design (CUD) palette.

This is a palette that is unambiguous to both colorblind and
non-colorblind people. See <https://jfly.uni-koeln.de/color/> for
details."""


class ShLightCUDProfile(ColorProfile):
    """Black on white color profile with CUD palette."""

    def __init__(self) -> None:
        super().__init__(
            palette=CUD_PALETTE, fg="#000000", bg="#ffffff", fg_secondary="#a9a9a9"
        )


class BSLightCUDProfile(ColorProfile):
    """Bootstrap light theme color profile with CUD palette."""

    def __init__(self) -> None:
        super().__init__(
            palette=CUD_PALETTE, fg="#212529", bg="#ffffff", fg_secondary="#adb5bd"
        )


class BSDarkCUDProfile(ColorProfile):
    """Bootstrap dark theme color profile with CUD palette."""

    def __init__(self) -> None:
        palette = ["#adb5bd"] + CUD_PALETTE[1:]
        super().__init__(
            palette=palette, fg="#adb5bd", bg="#212529", fg_secondary="#495057"
        )


############################################################
# SCALE PROFILES


class ShScaleProfile(PlotScaleProfile):
    """Builder for scale profiles.

    Args:
        fs: Base font size (in points).
        fs_small: Small font size (in points).
        fs_smaller: Smaller font size (in points).
        fs_large: Large font size (in points).
        marker_size: Default marker size (in points).
        line_width: Default line width (in points).
        full_width_in: Default figure width (in inches).
    """

    def __init__(
        self,
        fs: float,
        fs_small: float,
        fs_smaller: float,
        fs_large: float,
        marker_size: float,
        line_width: float,
        full_width_in: float,
    ) -> None:
        super().__init__(
            font_size=fs,
            axes_title_size=fs,
            axes_label_size=fs_small,
            xtick_label_size=fs_smaller,
            ytick_label_size=fs_smaller,
            legend_font_size=fs_smaller,
            legend_title_size=fs_small,
            figure_title_size=fs_large,
            figure_label_size=fs,
            marker_size=marker_size,
            line_width=line_width,
            full_width_in=full_width_in,
            legend_marker_scale=2.0,
            constrained_layout=True,
            constrained_layout_hspace=0.1,
            constrained_layout_wspace=0.02,
        )


class ShPaperScaleProfile(ShScaleProfile):
    r"""Scale profile for a 10pt document.

    Font sizes correspond to relative LaTeX font sizes for 10pt
    documents:

    - \normalsize: 10pt
    - \small: 9pt
    - \footnotesize: 8pt
    - \large: 12pt
    """

    def __init__(self) -> None:
        super().__init__(
            fs=10.0,  # normalsize
            fs_small=9.0,  # small
            fs_smaller=8.0,  # footnotesize
            fs_large=12.0,  # large
            marker_size=2.0,
            line_width=1.5,
            full_width_in=6.5,
        )


class ShBookScaleProfile(ShScaleProfile):
    r"""Scale profile for a 12pt document.

    Font sizes correspond to relative LaTeX font sizes for 12pt
    documents:

    - \normalsize: 12pt
    - \small: 10.95pt
    - \footnotesize: 10pt
    - \large: 14.4pt
    """

    def __init__(self) -> None:
        super().__init__(
            fs=12.0,  # normalsize
            fs_small=10.95,  # small
            fs_smaller=10.0,  # footnotesize
            fs_large=14.4,  # large
            marker_size=3.0,
            line_width=2.0,
            full_width_in=6.0,
        )


class _ShWebScaleProfile(ShScaleProfile):
    def __init__(
        self, fs_px: float, ms_px: float, lw_px: float, fw_px: float, dpi: float
    ) -> None:
        pt_per_px = 72.0 / dpi
        fs = fs_px * pt_per_px
        super().__init__(
            fs=fs,  # medium
            fs_small=fs * 0.8125,  # small
            fs_smaller=fs * 0.625,  # x-small
            fs_large=fs * 1.125,  # large
            marker_size=ms_px * pt_per_px,
            line_width=lw_px * pt_per_px,
            full_width_in=fw_px / dpi,
        )


class ShWebScaleProfile(_ShWebScaleProfile):
    """Scale profile for display on the web.

    Sizes are for a 16px font size at 96dpi (CSS reference px).
    """

    def __init__(self) -> None:
        # CSS reference px is based on 96dpi.
        super().__init__(fs_px=16.0, ms_px=3.0, lw_px=2.0, fw_px=675.0, dpi=96.0)


class ShPresentationScaleProfile(_ShWebScaleProfile):
    """Scale profile for presentations.

    Sizes are based on 48px font size, and will be scaled based on dpi.

    Args:
        dpi: Scale for converting pixel sizes to points.
    """

    def __init__(self, dpi: float) -> None:
        super().__init__(fs_px=48.0, ms_px=9.0, lw_px=6.0, fw_px=1600.0, dpi=dpi)


############################################################
# FONT PROFILES


class ShFontsetupFontProfile(FontProfile):
    """LaTeX font profile using the fontsetup package.

    See <https://www.ctan.org/pkg/fontsetup> for details on the package.
    This profile simply sets the latex preamble to load the package with
    the given font.

    Args:
        font: One of the fonts supported by fontsetup. This value is
            passed as the sole argument to the package.
    """

    FontType = Literal[
        "default",
        "olddefault",
        "cambria",
        "concrete",
        "ebgaramond",
        "erewhon",
        "euler",
        "fira",
        "gfsartemisia",
        "gfsdidotclassic",
        "gfsdidot",
        "kekris",
        "libertinus",
        "lucida",
        "minion",
        "msgaramond",
        "neoeuler",
        "oldstandard",
        "palatino",
        "stixtwo",
        "talos",
        "times",
        "xcharter",
    ]

    def __init__(self, font: FontType = "default") -> None:
        valid_fonts = self.FontType.__args__  # type: ignore[attr-defined]
        if font not in valid_fonts:
            raise ValueError(
                f"unknown 'fontsetup' font: {font}: available choices: {valid_fonts}"
            )
        super().__init__(
            family=["serif"],
            latex_preamble=[r"\usepackage[%s]{fontsetup}" % font],
            pgf_rcfonts=False,
        )


class ShPGFRcFontsFontProfile(FontProfile):
    """LaTeX font profile combining fontsetup with system fonts.

    This profile loads the fontsetup package with the given font as in
    `ShFontsetupFontProfile`, but also sets `pgf.rcfonts` to `True`,
    so that Matplotlib will insert `fontspec` commands into
    the LaTeX preamble to set serif/sans-serif/monospace fonts.

    Args:
        family: Default font family.
        base_font: One of the fonts supported by fontsetup. This value
            is passed as the sole argument to the package.
        serif: Override for serif font. If `None`, `font.serif` from
            `rcParams` will be used.
        sans_serif: Override for sans-serif font. If `None`,
            `font.sans-serif` from `rcParams` will be used.
        monospace: Override for monospace font. If `None`,
            `font.monospace` from `rcParams` will be used.
    """

    def __init__(
        self,
        family: Literal["serif", "sans-serif", "monospace"] = "serif",
        base_font: ShFontsetupFontProfile.FontType = "default",
        serif: Optional[str] = None,
        sans_serif: Optional[str] = None,
        monospace: Optional[str] = None,
    ) -> None:
        super().__init__(
            family=[family],
            latex_preamble=[r"\usepackage[%s]{fontsetup}" % base_font],
            pgf_rcfonts=True,
        )
        if serif is not None:
            self.serif = [serif]
        if sans_serif is not None:
            self.sans_serif = [sans_serif]
        if monospace is not None:
            self.monospace = [monospace]


############################################################
# AXES PROFILES


class ShPrintAxesProfile(AxesProfile):
    """Axes profile for print."""

    def __init__(self) -> None:
        super().__init__(
            grid_axes="none",
            spines={"left", "bottom"},
            axis_below="all",
            xticks_top="none",
            xticks_bottom="major",
            xlabels_top=False,
            xlabels_bottom=True,
            xtick_direction="inout",
            xtick_alignment="center",
            xlabel_position="center",
            yticks_left="major",
            yticks_right="none",
            ylabels_left=True,
            ylabels_right=False,
            ytick_direction="inout",
            ytick_alignment="center_baseline",
            ylabel_position="center",
        )


class ShWebAxesProfile(AxesProfile):
    """Axes profile for web."""

    def __init__(self) -> None:
        super().__init__(
            grid_axes="both",
            grid_lines="major",
            spines=set(),
            axis_below="all",
            xticks_top="none",
            xticks_bottom="none",
            xlabels_top=False,
            xlabels_bottom=True,
            xtick_direction="in",
            xtick_alignment="center",
            xlabel_position="center",
            yticks_left="none",
            yticks_right="none",
            ylabels_left=True,
            ylabels_right=False,
            ytick_direction="in",
            ytick_alignment="center_baseline",
            ylabel_position="center",
        )


class ShPresentationAxesProfile(AxesProfile):
    """Axes profile for presentation."""

    def __init__(self) -> None:
        super().__init__(
            grid_axes="y",
            grid_lines="major",
            spines={"bottom"},
            axis_below="all",
            xticks_top="none",
            xticks_bottom="major",
            xlabels_top=False,
            xlabels_bottom=True,
            xtick_direction="out",
            xtick_alignment="center",
            xlabel_position="center",
            yticks_left="none",
            yticks_right="none",
            ylabels_left=True,
            ylabels_right=False,
            ytick_direction="inout",
            ytick_alignment="center_baseline",
            ylabel_position="center",
        )


############################################################
# FULL PROFILES


sh_rc_overrides = {"figure.titleweight": "bold"}


class _ShFontsetupProfile(PlottingProfile):
    def __init__(
        self, fontname: ShFontsetupFontProfile.FontType, **kwargs: Any
    ) -> None:
        super().__init__(
            font=ShFontsetupFontProfile(fontname),
            **{
                "backend": "pgf",
                "savefig.format": "pdf",
                "pdf.fonttype": 42,
                **sh_rc_overrides,
                **kwargs,
            },
        )


class ShPaperProfile(_ShFontsetupProfile):
    """Profile for generating figures for a paper (10pt).

    Args:
        fontname: Name of the font to use--see `ShFontsetupFontProfile`.
        **rc_extra: `rcParams` overrides.
    """

    def __init__(
        self, fontname: ShFontsetupFontProfile.FontType = "default", **rc_extra: Any
    ) -> None:
        super().__init__(
            fontname,
            color=ShLightCUDProfile(),
            scale=ShPaperScaleProfile(),
            axes=ShPrintAxesProfile(),
            **rc_extra,
        )


class ShBookProfile(_ShFontsetupProfile):
    """Profile for generating figures for a book (12pt).

    Args:
        fontname: Name of the font to use--see `ShFontsetupFontProfile`.
        **rc_extra: `rcParams` overrides.
    """

    def __init__(
        self, fontname: ShFontsetupFontProfile.FontType = "default", **rc_extra: Any
    ) -> None:
        super().__init__(
            fontname,
            color=ShLightCUDProfile(),
            scale=ShBookScaleProfile(),
            axes=ShPrintAxesProfile(),
            **rc_extra,
        )


class ShWebProfile(PlottingProfile):
    """Profile for generating figures for the web.

    Args:
        theme: Color theme--'light' will generate figures on a light
            background, and 'dark' will generate figures on a dark
            background.
        font_family: Default font family.
        sans_serif_font: Optional override for default sans-serif font.
        serif_font: Optional override for default serif font.
        monospace_font: Optional override for default monospace font.
        cursive_font: Optional override for default cursive font.
        fantasy_font: Optional override for default fantasy font.
        math_font: Optional override for default math font.
        **rc_extra: `rcParams` overrides.
    """

    def __init__(
        self,
        theme: Literal["light", "dark"],
        font_family: Literal[
            "serif", "sans-serif", "monospace", "fantasy", "cursive"
        ] = "sans-serif",
        sans_serif_font: Optional[str] = None,
        serif_font: Optional[str] = None,
        monospace_font: Optional[str] = None,
        cursive_font: Optional[str] = None,
        fantasy_font: Optional[str] = None,
        math_font: Optional[
            Literal["dejavusans", "dejavuserif", "cm", "stix", "stixsans"]
        ] = None,
        **rc_extra: Any,
    ) -> None:
        if theme == "light":
            color_profile: ColorProfile = BSLightCUDProfile()
        elif theme == "dark":
            color_profile = BSDarkCUDProfile()
        else:
            raise ValueError(f"invalid value for theme: {theme!r}")

        font_profile = FontProfile(family=[font_family])
        if sans_serif_font is not None:
            font_profile.sans_serif = [sans_serif_font]
        if serif_font is not None:
            font_profile.serif = [serif_font]
        if monospace_font is not None:
            font_profile.monospace = [monospace_font]
        if cursive_font is not None:
            font_profile.cursive = [cursive_font]
        if fantasy_font is not None:
            font_profile.fantasy = [fantasy_font]
        if math_font is not None:
            font_profile.math_fontset = math_font

        super().__init__(
            color=color_profile,
            font=font_profile,
            scale=ShWebScaleProfile(),
            axes=ShWebAxesProfile(),
            **{
                "backend": "svg",
                "svg.fonttype": "path",
                "savefig.format": "svg",
                **sh_rc_overrides,
                **rc_extra,
            },
        )


class ShPresentationProfile(PlottingProfile):
    """Profile for generating figures for presentations.

    Args:
        font_family: Default font family.
        base_font: See `ShPGFRcFontsFontProfile`.
        serif_font: See `ShPGFRcFontsFontProfile`.
        sans_serif_font: See `ShPGFRcFontsFontProfile`.
        monospace_font: See `ShPGFRcFontsFontProfile`.
        dpi: See `ShPresentationScaleProfile`.
        **rc_extra: `rcParams` overrides.
    """

    def __init__(
        self,
        font_family: Literal["serif", "sans-serif", "monospace"] = "sans-serif",
        base_font: ShFontsetupFontProfile.FontType = "default",
        serif_font: Optional[str] = None,
        sans_serif_font: Optional[str] = None,
        monospace_font: Optional[str] = None,
        dpi: Union[float, str] = 200.0,
        **rc_extra: Any,
    ) -> None:
        super().__init__(
            color=ShLightCUDProfile(),
            font=ShPGFRcFontsFontProfile(
                font_family, base_font, serif_font, sans_serif_font, monospace_font
            ),
            scale=ShPresentationScaleProfile(float(dpi)),
            axes=ShPresentationAxesProfile(),
            **{
                "backend": "pgf",
                "savefig.format": "png",
                "figure.dpi": float(dpi),
                **sh_rc_overrides,
                **rc_extra,
            },
        )


def make_builtin_profile_builder(
    profile_cls: type[PlottingProfile], **base_kwargs: Any
) -> Callable[..., PlottingProfile]:
    def profile_builder(**kwargs: Any) -> PlottingProfile:
        return profile_cls(**base_kwargs, **kwargs)

    return profile_builder


SH_BUILTIN_PROFILES: dict[str, Callable[..., PlottingProfile]] = {
    "paper": make_builtin_profile_builder(ShPaperProfile),
    "book": make_builtin_profile_builder(ShBookProfile),
    "web_light": make_builtin_profile_builder(ShWebProfile, theme="light"),
    "web_dark": make_builtin_profile_builder(ShWebProfile, theme="dark"),
    "presentation": make_builtin_profile_builder(ShPresentationProfile),
}
"""Built-in plotting profiles with set values for different contexts."""
