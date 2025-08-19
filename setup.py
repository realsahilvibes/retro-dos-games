from setuptools import setup, find_packages

setup(
    name='retro-dos-game',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pygame',  # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'retro-dos-game=main:main',  # Adjust the entry point as necessary
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A retro-style DOS game built in Python.',
    license='MIT',
    keywords='game retro dos python',
    url='https://github.com/yourusername/retro-dos-game',  # Replace with your repository URL
)