Fork of [bboe/update-checker](https://github.com/bboe/update_checker)

# update_checker

A python module that will check for package updates.

Only whitelisted packages can be checked for updates. Contact update_checker's
author for information on adding a package to the whitelist.

### Installation

The update_checker module can be installed via:

    pip install update_checker_rg

### Usage

To simply output when there is a newer version of the `praw` package, you can
use the following bit of code:

```python
from update_checker import update_check
update_check('praw', '0.0.1')
```

If you need more control, such as performing operations conditionally when
there is an update you can use the following approach:

```python
from update_checker import UpdateChecker
checker = UpdateChecker()
result = checker.check('praw', '0.0.1')
if result:  # result is None when an update was not found or a failure occured
   # result is a UpdateResult object that contains the following attributes:
   # * available_version
   # * package_name
   # * running_version
   # * release_date (is None if the information isn't available)
   print(result)
   # Conditionally perform other actions
```
