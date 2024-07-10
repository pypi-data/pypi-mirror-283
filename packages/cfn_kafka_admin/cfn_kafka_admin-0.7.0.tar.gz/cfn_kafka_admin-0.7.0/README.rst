===============
cfn-kafka-admin
===============

------------------------------------------------------------------------------
CLI Tool and Lambda Functions to CRUD Kafka resources via AWS CloudFormation
------------------------------------------------------------------------------


|PYPI_VERSION|

|FOSSA| |PYPI_LICENSE|

|CODE_STYLE| |TDD|

.. image:: https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiY2xwc0NER1JuU1J3MThYczhFMDJLWlQxWGpoRnhNWHNtbGN1NGpVMVNTMk12UlQxdWVlZ2w5YnhPQzhkMnV4cTI0S0tIdTRyTmRHWWErWXJPNWFpcWlzPSIsIml2UGFyYW1ldGVyU3BlYyI6IkxaRGZCMW1KbVE1RWRJYjciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main
        :target: https://eu-west-1.codebuild.aws.amazon.com/project/eyJlbmNyeXB0ZWREYXRhIjoibVAvWVBBNjZlNWFwTWEwSEdWcGx6MWpudy9KeEZTb1lXdWFuQ3FwbjJCRTBnc1lyZm41eHRqV2k0bDN6UTBmaEpJMGd0Y3I3Vm5kTGtZQzc1b25Uckxxd3hERzlpSzJndVFOekJUR0NMM0V0YXljSWx4Yjc2YmJpUzlZM01RPT0iLCJpdlBhcmFtZXRlclNwZWMiOiI3bnllb1dlbU8rZis1ekh5IiwibWF0ZXJpYWxTZXRTZXJpYWwiOjF9


Manage Kafka resources via AWS CFN
===================================

* Topics
* ACLs
* Schemas (non AWS Glue Schema)


.. |PYPI_VERSION| image:: https://img.shields.io/pypi/v/cfn-kafka-admin.svg
        :target: https://pypi.python.org/pypi/cfn-kafka-admin

.. |PYPI_LICENSE| image:: https://img.shields.io/pypi/l/cfn-kafka-admin
    :alt: PyPI - License
    :target: https://github.com/compose-x/cfn-kafka-admin/blob/master/LICENSE

.. |PYPI_PYVERS| image:: https://img.shields.io/pypi/pyversions/cfn-kafka-admin
    :alt: PyPI - Python Version
    :target: https://pypi.python.org/pypi/cfn-kafka-admin

.. |PYPI_WHEEL| image:: https://img.shields.io/pypi/wheel/cfn-kafka-admin
    :alt: PyPI - Wheel
    :target: https://pypi.python.org/pypi/cfn-kafka-admin

.. |FOSSA| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcompose-x%2Fcfn-kafka-admin.svg?type=shield

.. |CODE_STYLE| image:: https://img.shields.io/badge/codestyle-black-black
    :alt: CodeStyle
    :target: https://pypi.org/project/black/

.. |TDD| image:: https://img.shields.io/badge/tdd-pytest-black
    :alt: TDD with pytest
    :target: https://docs.pytest.org/en/latest/contents.html

.. |BDD| image:: https://img.shields.io/badge/bdd-behave-black
    :alt: BDD with Behave
    :target: https://behave.readthedocs.io/en/latest/
