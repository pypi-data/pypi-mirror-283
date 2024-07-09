from setuptools import setup

readme = open("./README.md", "r")


setup(
    name="villamar",
    packages=["villamar"],  # this must be the same as the name above
    version="0.1",
    description="Esta es la descripcion",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author="Josue Villamar",
    author_email="",
    # use the URL to the github repo
    url="https://github.com/villamar32/villamar",
    download_url="https://github.com/villamar32/villamar/tarball/0.1",
    keywords=["network", "automation", "python"],
    classifiers=[],
    license="MIT",
    include_package_data=True,
)
