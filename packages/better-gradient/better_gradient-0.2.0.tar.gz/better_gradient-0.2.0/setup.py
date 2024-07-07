from setuptools import setup, find_packages

setup(
    name='better-gradient',
    version='0.2.0',  # Update the version number as needed
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'better-gradient = better_gradient.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version
)
