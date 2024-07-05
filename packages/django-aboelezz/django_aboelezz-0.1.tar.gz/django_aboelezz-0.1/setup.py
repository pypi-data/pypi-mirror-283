from setuptools import setup, find_packages

setup(
    name='django-aboelezz',
    version='0.1',
    packages=find_packages(include=['myapp', 'myapp.*']),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    entry_points='''
        [console_scripts]
    ''',
)
