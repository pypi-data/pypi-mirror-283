# HiDir: Hierarchical Directory

**HiDir** is a Python package designed to efficiently manage and organize files within a **Hierarchical Directory** structure. It provides operations to map, check, move, and copy files based on customizable strategies for file identification and path generation.


## Installation

You can install DirectoryManager via pip:

```shell
pip install hidir
```

## Usage

### Initialization

Create an instance of DirectoryManager by specifying the root directory and optional parameters:
```python
from hidir import DirectoryManager

manager = DirectoryManager(root='/path/to/folder', strategy='SHA-256')
```

`files_predict` and `clear_index` is optional parameters. `files_predict` is the estimated number of files. `clear_index` is a boolean value indicating whether to forbid the system file index.

### Method

* `get_base_path(file_name)`: Get the base path for a file based on its name.
* `check_file(file_name)`: Check if a file exists by its name and return its path if it exists.
* `move_file(file_path)`: Move a file to its designated path.
* `copy_file(file_path)`: Copy a file to its designated path.

### Example

```python
# Move a file to its designated folder
manager.move_file('/path/to/file.txt')

# Copy a file to its designated folder
manager.copy_file('/path/to/file.txt')

# Check if a file exists and get its path
file_path = manager.check_file('file.txt')
if file_path:
    print(f'File exists at: {file_path}')
else:
    print('File does not exist.')
```


## Contributing

If you find a bug :bug:, please open a [bug report](https://github.com/allenai/python-package-template/issues/new?assignees=&labels=bug&template=bug_report.md&title=).
If you have an idea for an improvement or new feature :rocket:, please open a [feature request](https://github.com/allenai/python-package-template/issues/new?assignees=&labels=Feature+request&template=feature_request.md&title=).


## License

This package was started off with the [python-package-template](https://github.com/allenai/python-package-template).
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.