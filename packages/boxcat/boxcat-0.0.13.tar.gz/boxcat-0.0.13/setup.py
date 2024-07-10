from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='boxcat',
    version="0.0.13",
    author="Michael Yau",
    author_email="mywyau@gmail.com.com",
    description="A small library to test github actions and using some dodgy fp in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mywyau/boxcat",

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project's dependencies here.
        # For example: 'numpy', 'requests',
    ],
    tests_require=[
        'pytest',  # or 'unittest', if you prefer
    ],
    test_suite='test',
    entry_points={
        'console_scripts': [
            # Define command-line scripts here.
            # For example: 'your_script=your_module:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
