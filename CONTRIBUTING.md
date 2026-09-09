# Welcome to the SciFlawBenchHarness Contributing guide

Thank you for taking the time to contribute to our project!

## developer Setup

Follow the instructions in the README to get the repository running on your machine.

For developer packages to be added as well, make sure to

```bash
pip install ."[dev]"
```

from whatever environment manager you are using instead of just using '.'


## Issues and discussions

For any bugs or general fixes to the harness itself, make sure to check the issues section. If you see any open issues related to what you are suggesting, upvote that issue and perhaps add a comment under this issue for further clarification on your specific perspective on the isssue. Otherwhise, open a new issue according to our templates to specify what needs to be fixed or added.

For additional feature requests, please put these under the discussions section before opening a related issue so that maintainers can have a dialogue about implementation before they are fully done.


## Style considerations

Ruff linting and formatting has been setup on the repository so please try and match things according to that. to check if your code is in compliance before making a commit simply run the following:
    ```bash
    ruff check .
    ```
Ensure that there are no errors before a commit is made

For docstrings, the following style is preferred:

    ```python
    """
    <description>

    Args:
        <arg1_name> (<arg1_type>): ...
        <arg2_name> (<arg2_type>): ...
        ...

    Returns (<return_type>): ...

    """
    ```

On the commit messages, try to preface the message with one of the following tags:
    a) "Fix": fix for unintended or innefficient behaviour,
    b) "Feat": New feature or added functioniality,
    c) "Breaking": Break to the previous api such that downstream users may need to update their configurations

## Testing policy

This project uses pytest as the platform on which tests are written. once the environment is sourced, running the test
suite can be accomplished with the following command:  `pytest`

To run a specific test file that you may be developing it is also possible to specify by using:

```python
pytest /path/to/your/file <options>
```

Ensure that for any major feature addition that there are unit tests that make sure it has its intended behaviour just from the perspective the class by itself.

If the addition is more structural or would generally benefit from having more involved tests, add an integration test with either the fake classes as can be seen in `tests/integration/smoke` or with real api calls by copying the patterns in `tests/integration/live`. If the test will ultimately require API usage which may be limited, mark it with live to prevent running them by mistake. When needed, the live suite of tests can be run using the 'live' argument to pytest.


## Checklist before making a pull request

1. There are no ruff formatting or linting errors
2. Any major channged/additional functions are properly documented with updated docstrings in the proper style
3. any additional **new** code paths should have a test checking that they function as intended
4. running pytest causes no errors
