import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

# https://docs.python.org/3/distutils/setupscript.html
setuptools.setup(
    name="Blogbot",
    version="0.0.1",
    author="Rafal Mokrzycki",
    author_email="rafalmokrzycki1@gmail.com",
    description="Google Cloud Storage Files Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafal-mokrzycki/blogbot",
    packages=setuptools.find_packages(),
    license="Proprietary",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.10",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    keywords=["GCP", "GCS", "bot", "blog", "LinkedIn"]
    python_requires=">=3.10",
)
