from setuptools import setup, find_packages

VERSION = '1.0.6'
DESCRIPTION = 'LLM function calling interface'
LONG_DESCRIPTION = 'A package that allows you to call functions in LLM'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="LLM_function_calling_interface",
    version=VERSION,
    author="KillT",
    author_email="vqtoan1807@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'LLM', 'function calling'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
