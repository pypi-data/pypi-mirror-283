from setuptools import setup

setup(name='sqladmin_async',
      version='2.9',
      description='Fork of Sqladmin with async functions',
      package_data={"sqladmin_async": ["statics/**/*", "templates/**/*"]},
      author_email='ilikepustoshka@gmail.com',
      license="Copyright © 2024, Scherba Matthew. All rights reserved.",
      zip_safe=False,
      classifiers = [
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Topic :: Internet :: WWW/HTTP",
            "Operating System :: OS Independent",
            ],
      requires = [
            "starlette",
            "sqlalchemy",
            "wtforms",
            "jinja2",
            "python_multipart",
      ])
# pypi-AgEIcHlwaS5vcmcCJGE5OGFlZDdiLTBjOTAtNGE1MC05MGU0LTJhZmE0NzQ2NmMzNAACKlszLCIzZGJkNWEyNi1mZTRmLTQzYWEtOGNmNy1kMjljYTI4NWEwYmMiXQAABiBC246edtj0HC4M5KTLK7i_PNv-uI-GH4RrlqEDfl6MQw