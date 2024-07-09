from argparse import ArgumentError, ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

import matplotlib as mpl
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from shplot import ShPlot
from shplot.profiles.builtin import CUD_PALETTE, SH_BUILTIN_PROFILES


class TestShPlot(TestCase):
    def test_get_plot_size_returns_correct_size_with_given_width_aspect(self):
        shplot = ShPlot(width=3.0, aspect=3.0 / 2.0)
        shplot_size = shplot.get_plot_size()
        self.assertAlmostEqual(shplot_size[0], 3.0)
        self.assertAlmostEqual(shplot_size[1], 2.0)

    def test_get_plot_size_returns_correct_size_with_auto_aspect(self):
        shplot = ShPlot(width=3.0)
        mpl_figsize = mpl.rcParams["figure.figsize"]
        mpl_aspect = mpl_figsize[0] / mpl_figsize[1]
        correct_height = 3.0 / mpl_aspect
        shplot_size = shplot.get_plot_size()
        self.assertAlmostEqual(shplot_size[0], 3.0)
        self.assertAlmostEqual(shplot_size[1], correct_height)

    def test_get_plot_size_returns_correct_size_with_auto_width(self):
        shplot = ShPlot(aspect=16.0 / 9.0)
        mpl_width = mpl.rcParams["figure.figsize"][0]
        correct_height = mpl_width * 9.0 / 16.0
        shplot_size = shplot.get_plot_size()
        self.assertAlmostEqual(shplot_size[0], mpl_width)
        self.assertAlmostEqual(shplot_size[1], correct_height)

    def test_get_plot_size_returns_mpl_figsize_with_auto_aspect_width(self):
        shplot = ShPlot()
        mpl_width = mpl.rcParams["figure.figsize"]
        shplot_size = shplot.get_plot_size()
        self.assertAlmostEqual(shplot_size[0], mpl_width[0])
        self.assertAlmostEqual(shplot_size[1], mpl_width[1])

    def test_get_plot_path_adds_extension(self):
        shplot = ShPlot(file="foo/bar/shplot")
        mpl_fmt = mpl.rcParams["savefig.format"]
        self.assertEqual(shplot.get_plot_path(), Path(f"foo/bar/shplot.{mpl_fmt}"))

    def test_get_plot_path_doesnt_add_extension_if_already_provided(self):
        shplot = ShPlot(file="foo/bar/shplot.jpeg")
        self.assertEqual(shplot.get_plot_path(), Path("foo/bar/shplot.jpeg"))

    def test_shplot_parses_float_aspect_from_cmdline(self):
        parser = ArgumentParser()
        ShPlot.add_args_to_parser(parser)
        args_namespace = parser.parse_args(["--aspect", "3.14"])
        self.assertAlmostEqual(args_namespace.aspect, 3.14)

    def test_shplot_parses_tuple_aspect_from_cmdline(self):
        parser = ArgumentParser()
        ShPlot.add_args_to_parser(parser)
        args_namespace = parser.parse_args(["--aspect", "3.14;2.72"])
        self.assertAlmostEqual(args_namespace.aspect, 3.14 / 2.72)

    def test_shplot_raises_on_parsing_bad_aspect(self):
        parser = ArgumentParser(exit_on_error=False)
        ShPlot.add_args_to_parser(parser)
        with self.assertRaises(ArgumentError):
            parser.parse_args(["--aspect", "foo"])
        with self.assertRaises(ArgumentError):
            parser.parse_args(["--aspect", "1:2"])
        with self.assertRaises(ArgumentError):
            parser.parse_args(["--aspect", "1;2;3"])

    def test_shplot_raises_on_setting_bad_aspect(self):
        shplot = ShPlot()
        with self.assertRaises(ValueError):
            shplot.aspect = -1.0

    def test_shplot_passes_profile_args_to_profile(self):
        shplot = ShPlot(
            builtin_profile_name="paper", profile_args={"dummy_rc_key": "dummy_value"}
        )
        self.assertIn("dummy_rc_key", shplot._profile._rc_extra)
        self.assertEqual(shplot._profile._rc_extra["dummy_rc_key"], "dummy_value")

    def test_shplot_open_activates_profile(self):
        mpl.rc_file_defaults()
        shplot = ShPlot(builtin_profile_name="paper")
        shplot.open()
        mpl_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
        self.assertListEqual(mpl_palette, CUD_PALETTE)
        shplot.close()

    def test_shplot_close_deactivates_profile(self):
        mpl.rc_file_defaults()
        orig_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
        shplot = ShPlot(builtin_profile_name="paper")
        shplot.open()
        shplot.close()
        new_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
        self.assertListEqual(new_palette, orig_palette)

    def test_shplot_close_saves_file(self):
        with TemporaryDirectory() as temp_dir:
            plot_path = Path(f"{temp_dir}/shplot.jpg")
            shplot = ShPlot(file=str(plot_path))
            self.assertFalse(plot_path.exists())
            shplot.open()
            self.assertFalse(plot_path.exists())
            shplot.close()
            self.assertTrue(plot_path.exists())

    def test_shplot_open_returns_fig_axes(self):
        shplot = ShPlot()
        open_ret = shplot.open()
        self.assertIsInstance(open_ret, tuple)
        self.assertEqual(len(open_ret), 2)
        self.assertIsInstance(open_ret[0], Figure)
        self.assertIsInstance(open_ret[1], Axes)

    def test_shplot_open_makes_mosaic_if_arg_passed(self):
        shplot = ShPlot()
        open_ret = shplot.open("AAB\nCDB")
        self.assertIsInstance(open_ret, tuple)
        self.assertEqual(len(open_ret), 2)
        self.assertIsInstance(open_ret[0], Figure)
        self.assertIsInstance(open_ret[1], dict)
        self.assertSetEqual(set(open_ret[1].keys()), {"A", "B", "C", "D"})

    def test_shplot_open_passes_kwargs_to_subplots_call(self):
        shplot = ShPlot()
        _, ax = shplot.open(nrows=2, ncols=3)
        self.assertIsInstance(ax, np.ndarray)
        self.assertTupleEqual(ax.shape, (2, 3))

    def test_shplot_open_passes_kwargs_to_subplot_mosaic_call(self):
        shplot = ShPlot()
        _, ax = shplot.open("AAB\nCDB", empty_sentinel="D")
        self.assertSetEqual(set(ax.keys()), {"A", "B", "C"})

    def test_shplot_raises_on_double_open(self):
        shplot = ShPlot()
        shplot.open()
        with self.assertRaises(TypeError):
            shplot.open()

    def test_shplot_raises_on_close_without_open(self):
        shplot = ShPlot()
        with self.assertRaises(TypeError):
            shplot.close()

    def test_shplot_context_opens_and_closes(self):
        mpl.rc_file_defaults()
        orig_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]

        shplot = ShPlot(builtin_profile_name="paper")
        with shplot.context() as open_ret:
            self.assertIsInstance(open_ret, tuple)
            self.assertEqual(len(open_ret), 2)
            self.assertIsInstance(open_ret[0], Figure)
            self.assertIsInstance(open_ret[1], Axes)
            mpl_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
            self.assertListEqual(mpl_palette, CUD_PALETTE)

        mpl_palette = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
        self.assertListEqual(mpl_palette, orig_palette)

    def test_shplot_context_passes_kwargs_to_subplots_call(self):
        shplot = ShPlot()
        with shplot.context(nrows=2, ncols=3) as (_, ax):
            self.assertIsInstance(ax, np.ndarray)
            self.assertTupleEqual(ax.shape, (2, 3))

    def test_shplot_builtin_profile_attr_accepts_all_available_values(self):
        shplot = ShPlot()
        for builtin_profile_name in SH_BUILTIN_PROFILES:
            shplot.builtin_profile_name = builtin_profile_name
        with self.assertRaises(ValueError):
            shplot.builtin_profile_name = "notaprofile"
