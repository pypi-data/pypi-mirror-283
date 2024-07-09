import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weedeia-greenbox-core",
    version="0.0.2",
    author="Paulo Porto",
    author_email="cesarpaulomp@gmail.com",
    description="API for GPIO admnistration",
    packages=setuptools.find_packages(),
    entry_points={
      "console_scripts": [
          "weedeia-greenbox-core=main:main",
      ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'fastapi',
        'uvicorn',
        'RPi.GPIO'
    ]
)