from setuptools import setup, find_packages

version = '0.1'
LONG_DESCRIPTION = """
=====================================
Django Mariposa
=====================================

Simple django wrapper for mariposa supplying management commands
"""

setup(
    name="django-mariposa",
    version=version,
    description="django-mariposa",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='python',
    author='Skylar Saveland',
    author_email='skylar.saveland@gmail.com',
    url='http://github.com/skyl/django-mariposa',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['mariposa==0.1'],
)
