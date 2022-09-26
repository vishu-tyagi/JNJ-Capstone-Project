#!/bin/bash
pytest -v -W error::UserWarning -W ignore::pytest.PytestDeprecationWarning -W ignore::pytest.PytestUnknownMarkWarning "$@"