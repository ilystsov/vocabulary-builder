import glob
import shutil

from doit.task import clean_targets
from doit.tools import create_folder


LOCALES_DIRECTORY = "vocabulary_builder/locales"
LANGUAGES = ["fr", "uk", "de"]


def task_pot():
    """Recreate .pot file."""
    return {
        "actions": [
            "pybabel extract --mapping babel.cfg -o translations.pot vocabulary_builder"
        ],
        "file_dep": glob.glob("vocabulary_builder/templates/*.html"),
        "targets": ["translations.pot"],
        "clean": [clean_targets],
    }


def task_init_po():
    """Initialize .po files for new languages."""
    for lang in LANGUAGES:
        yield {
            "name": lang,
            "actions": [
                f"pybabel init -D translations -d locales -l {lang} -i translations.pot"
            ],
            "file_dep": ["translations.pot"],
        }


def task_po():
    """Update translations."""
    for lang in LANGUAGES:
        yield {
            "name": lang,
            "actions": [
                f"pybabel update -D translations -d locales -l {lang} "
                "-i translations.pot"
            ],
            "file_dep": ["translations.pot"],
            "targets": [f"locales/{lang}/LC_MESSAGES/translations.po"],
        }


def task_mo():
    """Compile translations."""
    for lang in LANGUAGES:
        yield {
            "name": lang,
            "actions": [
                (create_folder, [f"{LOCALES_DIRECTORY}/{lang}/LC_MESSAGES"]),
                f"pybabel compile -D translations -l {lang} "
                f"-i locales/{lang}/LC_MESSAGES/translations.po "
                f"-d {LOCALES_DIRECTORY}",
            ],
            "file_dep": [f"locales/{lang}/LC_MESSAGES/translations.po"],
            "targets": [f"{LOCALES_DIRECTORY}/{lang}/LC_MESSAGES/translations.mo"],
            "clean": [clean_targets],
        }


def task_i18n():
    return {
        "actions": [],
        "task_dep": ["mo", "po", "pot"],
    }


def task_docs():
    """Generate HTML docs"""
    return {
        "actions": ["sphinx-build -b html docs docs/_build/html"],
        "file_dep": ["docs/api.rst", "docs/index.rst", "docs/conf.py"],
        "targets": ["docs/_build/html/index.html"],
        "clean": [lambda: shutil.rmtree("docs/_build")],
    }


def task_test():
    """Run tests"""
    return {
        "actions": [
            "python3.10 -m pytest tests",
        ],
        "verbosity": 2,
    }


def task_lint():
    """Check code style with flake8 and pydocstyle"""
    return {
        "actions": ["flake8 vocabulary_builder", "pydocstyle vocabulary_builder"],
        "file_dep": glob.glob("vocabulary_builder/**/*.py")
        + glob.glob("tests/**/*.py"),
    }
