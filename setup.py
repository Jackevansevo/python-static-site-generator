from setuptools import setup


setup(
    name="Blog",
    version="1.0",
    long_description=__doc__,
    packages=["blog"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "cmarkgfm",
        "python-frontmatter",
        "jinja2",
        "livereload",
        "pygments",
    ],
    entry_points={"console_scripts": ["blog=blog.main:main"]},
)
