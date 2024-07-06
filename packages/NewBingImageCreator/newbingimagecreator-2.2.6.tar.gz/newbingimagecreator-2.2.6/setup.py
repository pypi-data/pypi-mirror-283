import setuptools

with open("README.md") as f:
    long_desc = f.read()

setuptools.setup(
    name='NewBingImageCreator',
    version='2.2.6',
    packages=["NewBingImageCreator", "NewBingImageCreator.aio"],
    url='https://github.com/',
    author='Anonymous',
    install_requires=['httpx'],
    author_email='',
    description='.com',
    long_description=long_desc,
    long_description_content_type="text/markdown"
)
