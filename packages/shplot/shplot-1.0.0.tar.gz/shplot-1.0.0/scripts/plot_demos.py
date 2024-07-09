#!/usr/bin/env python3
# Adapted from script in Matplotlib gallery:
# 'matplotlib.org/gallery/style_sheets/style_sheets_reference.html'.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)


def plot_scatter(ax, prng, nb_samples=100):
    """Scatter plot."""
    for mu, sigma, marker, label in [
        (-0.5, 0.75, "o", "Set 1"),
        (0.75, 1.0, "s", "Set 2"),
    ]:
        x, y = prng.normal(loc=mu, scale=sigma, size=(2, nb_samples))
        ax.plot(x, y, ls="none", marker=marker, label=label)
    ax.legend(title="Set")
    return ax


def plot_colored_lines(ax):
    """Plot lines with colors following the style color cycle."""
    t = np.linspace(-10, 10, 100)

    def sigmoid(t, t0):
        return 1 / (1 + np.exp(-(t - t0)))

    nb_colors = len(plt.rcParams["axes.prop_cycle"])
    shifts = np.linspace(-5, 5, nb_colors)
    amplitudes = np.linspace(1, 1.5, nb_colors)
    for t0, a in zip(shifts, amplitudes):
        ax.plot(t, a * sigmoid(t, t0), "-")
    ax.set_xlim(-10, 10)
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"$\sigma(t)$")
    ax.set_title(r"$\sigma(t)=\frac{a}{1 + e^{t_0 - t}}$")
    return ax


def plot_bar_graphs(ax, prng, min_value=5, max_value=25, nb_samples=5):
    """Plot two bar graphs, with letters as x-tick labels."""
    x = np.arange(nb_samples)
    ya, yb = prng.randint(min_value, max_value, size=(2, nb_samples))
    width = 0.25
    ax.bar(x, ya, width, label="A")
    ax.bar(x + width, yb, width, label="B")
    ax.legend(ncol=2)
    ax.set_xticks(x + width, labels=["a", "b", "c", "d", "e"])
    ax.set_xlabel("Letters")
    ax.set_ylabel("Numbers")
    return ax


def plot_colored_circles(ax, prng, nb_samples=15):
    """Plot circle patches.

    NB: draws a fixed amount of samples, rather than using the length of
    the color cycle, because different styles may have different numbers
    of colors.
    """
    for sty_dict, _ in zip(plt.rcParams["axes.prop_cycle"](), range(nb_samples)):
        ax.add_patch(
            plt.Circle(
                prng.normal(scale=3, size=2), radius=1.0, color=sty_dict["color"]
            )
        )
    ax.grid(visible=True)

    # Add title for enabling grid
    ax.set_title("ax.grid(True)", family="monospace", fontsize="small")

    ax.set_xlim([-4, 8])
    ax.set_ylim([-5, 6])
    ax.set_aspect("equal", adjustable="box")  # to plot circles as circles
    return ax


def plot_image_and_patch(ax, prng, size=(20, 20)):
    """Plot an image with random values and add a circular patch."""
    values = prng.random_sample(size=size)
    ax.imshow(values, interpolation="none")
    c = plt.Circle((5, 5), radius=5, label="patch")
    ax.add_patch(c)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])


def plot_histograms(ax, prng, nb_samples=10000):
    """Plot 4 histograms and a text annotation."""
    params = ((10, 10), (4, 12), (50, 12), (6, 55))
    for a, b in params:
        values = prng.beta(a, b, size=nb_samples)
        ax.hist(values, histtype="stepfilled", bins=30, alpha=0.8, density=True)

    # Add a small annotation.
    ax.annotate(
        r"$B(\alpha=4, \beta=12)$",
        xy=(0.25, 4.25),
        xytext=(0.9, 0.9),
        textcoords=ax.transAxes,
        va="top",
        ha="right",
        bbox={"boxstyle": "round", "alpha": 0.2},
        arrowprops={
            "arrowstyle": "->",
            "connectionstyle": "angle,angleA=-95,angleB=35,rad=10",
        },
    )
    return ax


def plot_errors(ax):
    """Plot 4 lines with differently styled errorbars."""
    x = np.arange(10)
    y = 2.5 * np.sin(x / 20 * np.pi)
    yerr = np.linspace(0.05, 0.2, 10)

    ax.errorbar(x, y + 3, yerr=yerr)
    ax.errorbar(x, y + 2, yerr=yerr, uplims=True)
    ax.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True)

    upperlimits = [True, False] * 5
    lowerlimits = [False, True] * 5
    ax.errorbar(x, y, yerr=yerr, uplims=upperlimits, lolims=lowerlimits)


def plot_logscales(ax):
    """Plot on log x and y axis with errorbars going below zero."""
    # Taken from:
    # 'matplotlib.org/gallery/scales/log_demo.html'.

    x = 10.0 ** np.linspace(0.0, 2.0, 20)
    y = x**2.0

    ax.set_xscale("log", nonpositive="clip")
    ax.set_yscale("log", nonpositive="clip")
    ax.errorbar(x, y, xerr=0.1 * x, yerr=5.0 + 0.75 * y)
    # `ylim` must be set after errorbar to allow errorbar to autoscale
    # limits.
    ax.set_ylim(bottom=0.1)
    ax.set_title("Errorbars")


def plot_text(ax):
    """Plot text features."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    ano_kwargs = {
        "xycoords": "axes fraction",
        "ha": "left",
        "va": "top",
        "fontsize": "xx-small",
    }

    ax.annotate(
        "Normal text:", (0, 1), **{**ano_kwargs, "fontsize": "small"}, weight="bold"
    )

    y = 0.9
    for family in ["serif", "sans-serif", "monospace", "fantasy", "cursive"]:
        ax.annotate(family.title(), (0, y), **ano_kwargs, family=family)
        y -= 0.05
        ax.annotate("Italic", (0.1, y), **ano_kwargs, family=family, style="italic")
        y -= 0.05
        ax.annotate("Bold", (0.1, y), **ano_kwargs, family=family, weight="bold")
        y -= 0.05
        ax.annotate(
            "Bold italic",
            (0.1, y),
            **ano_kwargs,
            family=family,
            style="italic",
            weight="bold",
        )
        y -= 0.05

    ano_kwargs["ha"] = "right"

    ax.annotate(
        "Math text:", (1, 1), **{**ano_kwargs, "fontsize": "small"}, weight="bold"
    )
    y = 0.9
    ax.annotate(r"$\mathrm{Roman}$", (1, y), **ano_kwargs)
    y -= 0.075
    ax.annotate(r"$\mathit{Italic}$", (1, y), **ano_kwargs)
    y -= 0.075
    ax.annotate(r"$\mathtt{Typewriter}$", (1, y), **ano_kwargs)
    y -= 0.075
    ax.annotate(r"$\mathbf{Bold}$", (1, y), **ano_kwargs)
    y -= 0.075
    ax.annotate(r"$\mathsf{Sans Serif}$", (1, y), **ano_kwargs)
    y -= 0.075
    ax.annotate(r"$\mathcal{CALLIGRAPHY}$", (1, y), **ano_kwargs)

    ax.annotate(
        "Numbers:", (1, 0.4), **{**ano_kwargs, "fontsize": "small"}, weight="bold"
    )
    ax.annotate("Normal:\n0123456789", (1, 0.3), **ano_kwargs)
    ax.annotate("Math:\n$0123456789$", (1, 0.15), **ano_kwargs)


def plot_figure(label, sfig=None, savefig=True, savedir=None):
    """Plot demonstration figure with a given style."""
    # Use a dedicated RandomState instance to draw the same "random"
    # values across the different figures.
    prng = np.random.RandomState(96917002)

    if sfig is None:
        figwidth = plt.rcParams["figure.figsize"][0]
        rowstocols = 2
        sfig = plt.figure(figsize=(figwidth, rowstocols * figwidth))
    sfig.suptitle(label, x=0.01, ha="left")
    axs = sfig.subplots(ncols=2, nrows=4).flat

    plot_scatter(axs[0], prng)
    plot_errors(axs[1])
    plot_bar_graphs(axs[2], prng)
    plot_colored_lines(axs[3])
    plot_histograms(axs[4], prng)
    plot_colored_circles(axs[5], prng)
    plot_logscales(axs[6])
    plot_text(axs[7])

    if savefig:
        if not Path(label).suffix:
            label += "." + plt.rcParams["savefig.format"]
        savepath = label if savedir is None else (savedir / label)
        sfig.savefig(savepath)


if __name__ == "__main__":
    outdir = Path("demos")
    outdir.mkdir(exist_ok=True)

    plot_figure("mpldefault_pre", savedir=outdir)

    from shplot.profiles.builtin import SH_BUILTIN_PROFILES

    for profile_name, f_profile in SH_BUILTIN_PROFILES.items():
        with f_profile().context():
            plot_figure(profile_name, savedir=outdir)

    plot_figure("mpldefault_post", savedir=outdir)
