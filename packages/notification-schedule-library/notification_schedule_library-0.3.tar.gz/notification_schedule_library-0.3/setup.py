from setuptools import setup, find_packages

setup(
    name="notification_schedule_library",
    version="0.3",
    packages=find_packages(),
    description="A library for handling notifications.",
    author="Gabriel",
    author_email="gabr.fern99@gmail.com",
    url="https://github.com/gabrfern99/notification_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',  # Example dependency
    ],
    python_requires='>=3.6',

)
