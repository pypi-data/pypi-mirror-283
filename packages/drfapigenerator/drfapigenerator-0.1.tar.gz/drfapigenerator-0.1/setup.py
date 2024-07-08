from setuptools import setup, find_packages

setup(
    name='drfapigenerator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
        'djangorestframework',
    ],
    entry_points={
        'console_scripts': [
            # Define any command line scripts here
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.2',  # Specify the appropriate Django version
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
