from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Atom Probe library testing'
LONG_DESCRIPTION = 'Library for interaction between atom probe and client computer'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="atomprobe_lib", 
        version=VERSION,
        author="Victor Petyuk",
        author_email="<victor.petyuk@pnnl.gov>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)