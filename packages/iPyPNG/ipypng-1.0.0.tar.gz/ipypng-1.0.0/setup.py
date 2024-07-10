from setuptools import setup,find_packages

version = '1.0.0'

with open('./README.rst',encoding='utf-8') as f:
    readme = f.read()


setup(
    name="iPyPNG",
    version=version,
    author="HGStyle",
    author_email="hgstyle@outlook.fr",
    url="https://github.com/HGStyle/iPyPNG",
    project_urls={
        "Documentation": "https://github.com/HGStyle/iPyPNG",
    },
    description="Convert real PNG to Apple fake PNG (CgBI)",
    long_description=readme,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    keywords="CgBI",
)
