import glob
import shutil

from doit.task import clean_targets
from doit.tools import create_folder
LOCALES_DIRECTORY = 'src/locales'


def task_pot():
    """Recreate .pot file."""
    return {
        'actions': ['pybabel extract --mapping babel.cfg -o translations.pot src'],
        'file_dep': glob.glob('src/templates/*.html'),
        'targets': ['translations.pot'],
        'clean': [clean_targets],
    }


def task_po():
    """Update translations."""
    return {
        'actions': ['pybabel update -D translations -d locales -l fr -i translations.pot '],
        'file_dep': ['translations.pot'],
        'targets': ['locales/fr/LC_MESSAGES/translations.po'],
    }


def task_mo():
    """Compile translations."""
    return {
        'actions': [
            (create_folder, [f'{LOCALES_DIRECTORY}/fr/LC_MESSAGES']),
            f'pybabel compile -D translations -l fr -i locales/fr/LC_MESSAGES/translations.po -d {LOCALES_DIRECTORY}'
        ],
        'file_dep': ['locales/fr/LC_MESSAGES/translations.po'],
        'targets': [f'{LOCALES_DIRECTORY}/fr/LC_MESSAGES/translations.mo'],
        'clean': [clean_targets],
    }


def task_i18n():
    return {
        'actions': [],
        'task_dep': ['mo', 'po', 'pot'],
    }


def task_html():
    """Generate HTML docs"""
    return {
        'actions': ['sphinx-build -b html docs docs/_build/html'],
        'file_dep': ['docs/api.rst', 'docs/index.rst', 'docs/conf.py'],
        'targets': ['docs/_build/html/index.html'],
        'clean': [lambda: shutil.rmtree('docs/_build')],
    }
