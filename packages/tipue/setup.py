from setuptools import setup

setup(
    name='lektor-tipue',
    version='0.1',
    author=u'seantis gmbh',
    author_email='info@seantis.ch',
    license='MIT',
    install_requires=[
        'beautifulsoup4',
    ],
    py_modules=['lektor_tipue'],
    entry_points={
        'lektor.plugins': [
            'tipue = lektor_tipue:TipuePlugin',
        ]
    }
)
