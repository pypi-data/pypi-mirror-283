from setuptools import setup

name = "types-pytest-lazy-fixture"
description = "Typing stubs for pytest-lazy-fixture"
long_description = '''
## Typing stubs for pytest-lazy-fixture

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pytest-lazy-fixture`](https://github.com/tvorog/pytest-lazy-fixture) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pytest-lazy-fixture`.

This version of `types-pytest-lazy-fixture` aims to provide accurate annotations
for `pytest-lazy-fixture==0.6.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pytest-lazy-fixture. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7c26da22bda786dce26d3a70fc18c14a7f4bd378` and was tested
with mypy 1.10.1, pyright 1.1.370, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="0.6.3.20240707",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pytest-lazy-fixture.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pytest_lazyfixture-stubs'],
      package_data={'pytest_lazyfixture-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
