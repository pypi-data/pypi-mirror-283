# opencepk-lib-python-common

Common Python packages

## Sample use case:

````

repos:

  - repo: https://github.com/opencepk/opencepk-lib-python-common
    rev: v0.0.5
    hooks:
      - id: python-pypi-version-check  # this is the id we refer to in precommit.hook
        name: Check version
        description: python-pypi-version-check
        args: ['./pyproject.toml']
        entry: python-pypi-version-check
        language: system
        pass_filenames: false  # Do not pass filenames to the hook (this is important to keep)

  - repo: https://github.com/opencepk/opencepk-lib-python-common
    rev: v0.0.5
    hooks:
    - id: find-and-replace-strings  # this is the id we refer to in precommit.hook
      name: find-and-replace-strings
      description: Find and replace strings
      entry: find-and-replace-strings
      language: python
      pass_filenames: true
      exclude_types:
        - binary
      files: '.*\.md$'
      verbose: true

      ```

````

## Find and Replace strings

  [find and replace strings documentation](./opencepk_lib_python_common/find_and_replace_strings_package/README.md)
