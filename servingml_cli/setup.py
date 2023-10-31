from setuptools import setup

setup(
    name='servingml',
    version='0.1',
    py_modules=['cli', 'build', 'deploy'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        servingml=cli:cli
    ''',
)
