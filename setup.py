from setuptools import setup, find_packages

setup(
    name="apispark",
    version="0.1.0",
    description="A lightweight Python framework for building fast, scalable APIs.",
    author="Your Name",
    author_email="gladsonchala@gmail.com",
    url="https://github.com/gladsonchala/apispark",
    packages=find_packages(),  # Automatically find all modules and sub-packages
    install_requires=[
        "fastapi==0.98.0",
        "uvicorn==0.22.0",
        "pydantic==2.1.0",
        "pytest==7.4.0"
    ],
    entry_points={
        'console_scripts': [
            'apispark=apispark.app:main',  # Entry point for the app
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
