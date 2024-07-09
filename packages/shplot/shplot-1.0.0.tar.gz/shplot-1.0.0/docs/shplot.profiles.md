# shplot.profiles package

### *class* shplot.profiles.ProfileBase(\*\*args)

Bases: `Corgy`

Base class for profiles.

Profile classes are thin wrappers around subsets of Matplotlib
parameters. Once instantiated, they can be used to generate a
dictionary, which can be used to update `matplotlib.rcParams`.

Profile classes have a dataclass-like interface. All attributes are
exposed as properties, and can be set either at initialization (as
keyword arguments) or later. Unless specified otherwise, attributes
directly correspond to Matplotlib parameters with the same name.

### Examples

```pycon
>>> from shplot.profiles import ColorProfile
>>> profile = ColorProfile(fg_secondary="gray")
>>> profile.rc()
{'grid.color': 'gray', 'legend.edgecolor': 'gray'}
```

```pycon
>>> profile.grid_alpha = 0.5
>>> profile.rc()
{'grid.color': 'gray', 'legend.edgecolor': 'gray',
'grid.alpha': 0.5}
```

#### rc()

Get profile configuration.

* **Returns:**
  Dictionary with `rcParams`. Unset attributes are not
  included in the returned dictionary so that different
  profiles can be combined together.
* **Return type:**
  dict[str, *Any*]

#### config(reload_mpl=True)

Update `matplotlib.rcParams` with profile configuration.

* **Parameters:**
  **reload_mpl** (*bool*) – Whether to reload `matplotlib` and `pyplot`
  modules before applying the configuration. Reloading is
  necessary for fonts to be updated.
* **Return type:**
  None

### Examples

```pycon
>>> import matplotlib as mpl
>>> print(mpl.rcParams["grid.color"])
#b0b0b0
>>> color_prof = ColorProfile(fg_secondary="gray")
>>> color_prof.config()
>>> print(mpl.rcParams["grid.color"])
gray
```

#### context(reload_mpl=True)

Context manager for `config` method.

* **Parameters:**
  **reload_mpl** (*bool*) – Whether to first reload `matplotlib` and
  `pyplot` modules.
* **Return type:**
  *Generator*[None, None, None]

### Examples

```pycon
>>> mpl.rcParams["grid.color"] = 'black'
>>> print(mpl.rcParams["grid.color"])
black
>>> color_prof = ColorProfile(fg_secondary="red")
>>> with color_prof.context():
...     print(mpl.rcParams["grid.color"])
red
>>> print(mpl.rcParams["grid.color"])
black
```

### *class* shplot.profiles.ColorProfile(\*\*args)

Bases: [`ProfileBase`](#shplot.profiles.ProfileBase)

Wrapper for color related Matplotlib params.

#### *property* palette *: list[str]*

`axes.prop_cycle` colors.

#### *property* fg *: str*

Primary foreground color, used for text, axes lines, ticks, etc.

#### *property* fg_secondary *: str*

Secondary foreground color, used for grid lines and legend frame.

#### *property* bg *: str*

Axes and figure face color.

#### *property* grid_alpha *: float*

#### *property* legend_frame_alpha *: float*

#### *property* transparent *: bool*

Whether to save figures with transparent background.

### *class* shplot.profiles.FontProfile(\*\*args)

Bases: [`ProfileBase`](#shplot.profiles.ProfileBase)

Wrapper for font related Matplotlib params.

#### *property* family *: list[str]*

#### *property* style *: Literal['normal', 'italic', 'oblique']*

#### *property* variant *: Literal['normal', 'small-caps']*

#### *property* weight *: Literal['normal', 'bold', '100', '200', '300', '400', '500', '600', '700', '800', '900']*

#### *property* stretch *: Literal['ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'normal', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded', 'wider', 'narrower']*

#### *property* serif *: list[str]*

#### *property* sans_serif *: list[str]*

#### *property* monospace *: list[str]*

#### *property* cursive *: list[str]*

#### *property* fantasy *: list[str]*

#### *property* text_usetex *: bool*

#### *property* latex_preamble *: list[str]*

#### *property* math_fontset *: Literal['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']*

#### *property* custom_math_rm *: str*

#### *property* custom_math_sf *: str*

#### *property* custom_math_tt *: str*

#### *property* custom_math_it *: str*

#### *property* custom_math_bf *: str*

#### *property* custom_math_cal *: str*

#### *property* math_fallback *: Literal['cm', 'stix', 'stixsans', 'None']*

#### *property* math_default *: Literal['rm', 'cal', 'it', 'tt', 'sf', 'bf', 'default', 'bb', 'frak', 'scr', 'regular']*

#### *property* pgf_rcfonts *: bool*

#### *property* set_pgf_preamble *: bool*

Whether to set `pgf.preamble` using `latex_preamble`.

### *class* shplot.profiles.FloatOrStr

Bases: `ABC`

Float or string type.

### *class* shplot.profiles.PlotScaleProfile(\*\*args)

Bases: [`ProfileBase`](#shplot.profiles.ProfileBase)

Wrapper for scale related Matplotlib params.

#### *property* font_size *: float*

#### *property* axes_title_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* axes_label_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* xtick_label_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* ytick_label_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* legend_font_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* legend_title_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* figure_title_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* figure_label_size *: [FloatOrStr](#shplot.profiles.FloatOrStr)*

#### *property* marker_size *: float*

#### *property* line_width *: float*

#### *property* full_width_in *: float*

Default figure width in inches.

#### *property* default_aspect_wh *: float*

Default figure aspect ratio (width/height).

#### *property* legend_marker_scale *: float*

#### *property* subplot_left *: float*

#### *property* subplot_right *: float*

#### *property* subplot_bottom *: float*

#### *property* subplot_top *: float*

#### *property* subplot_hspace *: float*

#### *property* subplot_wspace *: float*

#### *property* autolayout *: bool*

#### *property* constrained_layout *: bool*

#### *property* constrained_layout_hspace *: float*

#### *property* constrained_layout_wspace *: float*

### *class* shplot.profiles.AxesProfile(\*\*args)

Bases: [`ProfileBase`](#shplot.profiles.ProfileBase)

Wrapper for axes related Matplotlib params.

#### *property* grid_axes *: Literal['x', 'y', 'both', 'none']*

Which axes to draw grid lines on.

#### *property* grid_lines *: Literal['major', 'minor', 'both']*

Which grid lines to draw.

#### *property* spines *: set[Literal['left', 'right', 'bottom', 'top']]*

Which sides to draw spines on.

#### *property* axis_below *: Literal['all', 'line', 'none']*

Where to draw axis grid lines and ticks.

#### *property* xticks_top *: Literal['none', 'major', 'both']*

Which tick lines to draw on the top x-axis.

#### *property* xticks_bottom *: Literal['none', 'major', 'both']*

Which tick lines to draw on the bottom x-axis.

#### *property* xlabels_top *: bool*

Whether to show labels on the top x-axis.

#### *property* xlabels_bottom *: bool*

Whether to show labels on the bottom x-axis.

#### *property* xtick_direction *: Literal['in', 'out', 'inout']*

Direction of x-axis ticks.

#### *property* xtick_alignment *: Literal['left', 'center', 'right']*

Alignment of x-axis tick labels.

#### *property* xlabel_position *: Literal['left', 'center', 'right']*

Position of x-axis label.

#### *property* yticks_left *: Literal['none', 'major', 'both']*

Which tick lines to draw on the left y-axis.

#### *property* yticks_right *: Literal['none', 'major', 'both']*

Which tick lines to draw on the right y-axis.

#### *property* ylabels_left *: bool*

Whether to show labels on the left y-axis.

#### *property* ylabels_right *: bool*

Whether to show labels on the right y-axis.

#### *property* ytick_direction *: Literal['in', 'out', 'inout']*

Direction of y-axis ticks.

#### *property* ytick_alignment *: Literal['bottom', 'center', 'top', 'baseline', 'center_baseline']*

Alignment of y-axis tick labels.

#### *property* ylabel_position *: Literal['bottom', 'center', 'top']*

Position of y-axis labels.

### *class* shplot.profiles.PlottingProfile(\*\*kwargs)

Bases: [`ProfileBase`](#shplot.profiles.ProfileBase)

Wrapper for color, font, scale, and axes profiles.

All arguments for initialization are optional, and must be passed as
keyword arguments. Arguments other than `color`, `font`, `scale`,
and `axes` are used to update `matplotlib.rcParams` directly, and
will override any values set by the profile.

### Examples

```pycon
>>> from shplot.profiles import PlottingProfile, ColorProfile
>>> color_profile = ColorProfile(fg_secondary="gray")
>>> rc_extra = {"backend": "Agg", "legend.edgecolor": "black"}
>>> profile = PlottingProfile(color=color_profile, **rc_extra)
>>> profile.rc()
{'grid.color': 'gray', 'legend.edgecolor': 'black',
'backend': 'Agg'}
```

* **Parameters:**
  **kwargs** (*Any*)

#### *property* color *: [ColorProfile](#shplot.profiles.ColorProfile)*

#### *property* font *: [FontProfile](#shplot.profiles.FontProfile)*

#### *property* scale *: [PlotScaleProfile](#shplot.profiles.PlotScaleProfile)*

#### *property* axes *: [AxesProfile](#shplot.profiles.AxesProfile)*

## Submodules

* [shplot.profiles.builtin module](shplot.profiles.builtin.md)
