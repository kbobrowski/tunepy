from setuptools import setup

long_description = \
"""
Python decorator which allows to interactively tune arguments of a function.
Automatically determines output type (matplotlib / numpy image / return value / console output).
Decorated function can take instances of a "tunable" class (which determines range of the variable) instead of constant values as arguments.
"""

setup(
        name='tunepy',
        version='1.0.dev2',
        description='Interactive function argument tuning',
        long_description=long_description,
        url='https://github.com/kbobrowski/tunepy',
        author='Kamil Bobrowski',
        author_email='kamil.bobrowski@gmail.com',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ],
        keywords='optimization visualization tuning interactive',
        packages=['tunepy'],
        python_requires='>=3'
)



