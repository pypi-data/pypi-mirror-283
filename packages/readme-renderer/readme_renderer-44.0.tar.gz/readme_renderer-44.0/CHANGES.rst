Changes
=======

44.0 (2024-07-08)
-----------------

* Drop support for Python 3.8 (#315)
* Require docutils 0.21.2 and higher (#315)
* Remove HTML5 ``<s>`` tag from the list of allowed HTML tags (#315)
* Test all supported CPython and PyPy versions in CI (#315)
* Resolve Node 16 deprecation warnings in CI (#309)
* Lint specific directories (#312)
* Build a wheel once for all tox test environments (#308)
* Lazy open output files, and always close them (#314)
* Gitpod: Migrate to the Even Better TOML extension (#306)
* check-manifest: Remove a now-default ``.gitpod.yml`` exclusion (#307)

43.0 (2024-02-26)
-----------------

* Allow HTML5 ``picture`` tag through cleaner (#299)
* Test against Python 3.12 (#300)

42.0 (2023-09-07)
-----------------

* Migrate from ``bleach`` to ``nh3`` (#295)
* Migrate from ``setup.py`` to ``pyproject.toml``

41.0 (2023-08-18)
-----------------

* Allow HTML5 ``figcaption`` tag through cleaner (#291)
* Test ``README.rst`` from this project (#288)

40.0 (2023-06-16)
-----------------

* Add CLI option to render package README. (#271)
* Adapt tests to pygments 2.14.0 (#272)
* Update release process to use Trusted Publishing (#276)
* Replace usage of deprecated ``pkg_resources`` with ``importlib.metadata`` (#281)
* Drop support for Python 3.7 (#282), Test against Python 3.11 (#280)

37.3 (2022-10-31)
-----------------

* Allow HTML5 ``figure`` tag through cleaner (#265)

37.2 (2022-09-24)
-----------------

* Allow HTML5 ``s`` tag through cleaner (#261)

37.1 (2022-09-03)
-----------------

* Allow HTML5 ``nav`` tag through cleaner (#259)

37.0 (2022-08-21)
-----------------

* Remove command line example from docs (#197)
* Multiple pyproject.toml fixes (#251)
* Confirm handling multiple inline strong (#252)
* Convert RST output to HTML5 (#253)
* Add Typing to classifiers (#254)
* Development tweaks - coverage reporting, actions updates (#255)
* Add test confirming behavior with unknown lexers (#256)

36.0 (2022-08-06)
-----------------

* Enable gitpod development (#238)
* Allow rst admonitions to render (#242)
* Add badges to README (#243)
* Update codebase for modern Python (#244)
* Fix table cell spans (#245)
* Allow ``math`` directive in rst (#246)
* Preserve ``lang`` attribute in ``pre`` (#247)

35.0 (2022-04-19)
-----------------

* Add py.typed to the built wheel (#228)
* Use isolated build for tox (#229)
* Fix renderer ignore (#230)
* Remove legacy check command and distutils (#233)
* Emit a warning when no content is rendered (#231)
* Drop support for Python 3.6 (#236)
* Update html attribute order in tests (#235)

34.0 (2022-03-11)
-----------------

* Add static types (#225)

33.0 (2022-03-05)
-----------------

* Support cmarkgfm>=0.8.0 (#224)

33.0 (2022-02-05)
-----------------

* Support cmarkgfm>=0.8.0 (#224)
* Support Python 3.10

32.0 (2021-12-13)
-----------------

* Allow start attribute in ordered lists (#216)
* No limit rendering RST one column field names (#219)

31.0 (2021-12-09)
-----------------

* Render disabled checkboxes from Markdown (#217)

30.0 (2021-09-30)
-----------------

* support cmarkgfm>=0.6.0 (#209)

29.0 (2021-02-22)
-----------------

* Support cmarkgfm>=0.5.0 (#180)
* Drop support for Python 2 and 3.5 (#188)

28.0 (2020-10-20)
-----------------

* Support Python 3.9

27.0 (2020-10-09)
-----------------

* Add support for align attribute rendering Markdown headers (#173)

26.0 (2020-04-22)
-----------------

* Fix regression with image width/height attributes (#164)


25.0 (2020-03-14)
-----------------

* Support Python 3.7 and 3.8
* Drop support for Python 3.4
* Require Pygments>=2.5.1


24.0 (2018-10-27)
-----------------

* Remove dependency on ``future``. (#134)


23.0 (2018-10-22)
-----------------

* Breaking change: Move the cmarkgfm dependency into an extra (#130). Users
  that want to render Markdown will need to install readme_render[md] instead.


22.0 (2018-09-17)
-----------------

* Unify handling of SVG and other images in RST. (#113)
* Support width and alignment of images in RST (#114)


21.0 (2018-05-28)
-----------------

* Allow <caption>. (#105)
* Add specific tests for the raw directive. (#103)
* Include docinfo when rendering rst. (#99)
* Make Python 3 the default lexer for highlighting Python code in Markdown (#97)
* Allow align attribute on <p> tags (#98)


20.0 (2018-04-13)
-----------------

* Reformat docutils messages into more human-friendly output. (#92)
* Fix incorrect escaping of html entities in pre tags when using markdown. (#89)
* Allow width, height, alt, and align attributes on img tags. (#91)
* Fix check to not report success when there is invalid RST. (#90)


19.0 (2018-04-10)
-----------------

* Allow details and summary tags. (#77)
* Add .pytest_cache to .gitignore. (#85)
* Warn about Markdown content type when checking RST. (#83)
* Update pep8 tox env to use py3.6. (#84)
* Add Pygments-based syntax highlighting for Markdown. (#82)
* Update docs about check to talk about Markdown. (#80)


18.1 (2018-04-01)
-----------------

* Change Github-flavored Markdown identifier from ``gfm`` to ``GFM``.


18.0 (2018-03-30)
-----------------

* Add support for GitHub-flavored Markdown. (#67)
* Switch to cmarkgfm completely for rendering Markdown. (#68)
* Warn about missing long description. (#69)
* Make Github-Flavored Markdown the default variant (#73)


17.4 (2018-03-16)
-----------------

* All renderers now accept arbitrary ``kwargs`` for future-proofing.


17.3 (2018-03-08)
-----------------

* Gracefully handle new exceptions from bleach.


17.2 (2017-03-11)
-----------------

* Fix an issue cleaning plaintext values.


17.1 (2017-03-09)
-----------------

* Fix an issue attempting to clean data that had ``<a>`` tags without a href.


17.0 (2017-03-08)
-----------------

* Fix issue with bleach >= 2.0.


16.0 (2016-12-09)
-----------------

* Fix issue with docutils >= 0.13.1.


0.7.0 (2016-01-04)
------------------

* Renamed to ``readme_renderer``: https://github.com/pypa/readme_renderer
  to work around an name overlap with ``README`` files shipped in Python's
  default site-packages directory on certain case-insensitive file systems.

* Added `PyPA Code of Conduct`_.

* Allow <sub> and <sup> tags when cleaning rST HTML output.

* Dropped support for Python 2.6.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
