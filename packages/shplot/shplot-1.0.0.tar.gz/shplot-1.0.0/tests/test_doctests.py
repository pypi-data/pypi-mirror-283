from doctest import DocFileSuite

import shplot
import shplot.profiles

DOCTEST_MODULES = {
    shplot: ["_shplot.py"],
    shplot.profiles: ["_interface.py", "builtin.py"],
}  # type: ignore
DOCTEST_FILES = ["../README.md"]


def load_tests(loader, tests, ignore):
    for mod, modfiles in DOCTEST_MODULES.items():
        for file in modfiles:
            tests.addTest(DocFileSuite(file, package=mod))

    for file in DOCTEST_FILES:
        tests.addTest(DocFileSuite(file))

    return tests
