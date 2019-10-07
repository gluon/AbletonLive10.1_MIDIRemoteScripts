# Remote Script Framework
The remote script framework is based on top of Live's Python API and mainly used to integrate hardware controllers into Live.

## Maintainers
Push 2 Team

## Documentation

The latest documentation for the remote script framework is on [Jupiter](http://jupiter.office.ableton.com/remote-script-framework-docs/).
It is manually published at this point.

### Generate documentation

The documentation is written in reStructuredText and uses [Sphinx](http://www.sphinx-doc.org/) to generate a website from it. The sphinx
package and the [Read The Docs](https://readthedocs.org/) theme needs to be installed:
```
pip install sphinx sphinx_rtd_theme
```

[Graphviz](http://www.graphviz.org/) is used to generate inheritance graphs. On Windows it has to be installed manually. On Mac it can be installed using brew:
```
brew install graphviz
```

As the framework is depending on the Live API, the documentation can only be generated from within the Live repo. To generate it you need the following commands:
```
cd [remote-script-framework-repo]
sphinx-build -b html docs/ html-output/
```
