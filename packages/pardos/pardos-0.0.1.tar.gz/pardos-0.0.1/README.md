# pardos: Quality of Life extensions for pandas

`pardos` is a Python package that extends the functionality of pandas, providing additional methods for enhanced data manipulation and analysis. It aims to simplify common data operations and introduce new features to make working with pandas DataFrames and Series more efficient and intuitive.

Methods are provided as custom accessors or directly added as methods for DataFrames and Series, allowing you to perform operations directly on your data without the need for additional functions or libraries. 

## Features

- Custom accessors for DataFrames and Series
- Additional data manipulation methods
- Time-based operations
- Unix-like file operations on paths stored in Series
- Human-readable time parsing

## Installation

You can install `pardos` using pip:

```bash
pip install pardos
```

## Usage

To use `pardos`, simply import it after importing pandas:

```python
import pandas as pd
import pardos
```

Now you can use the additional methods and accessors provided by `pardos` on your pandas DataFrames and Series.

### Examples

#### Select rows based on column values

```python
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
result = df.select(A=2)
```

#### Add a new column based on existing ones

```python
def new_column(A, B):
    return A + B

df.augment(new_column)
```

#### Remove constant columns
```python

df = df.drop_constant()
```


#### Use human-readable time parsing

```python
df["date"] = pd.to_datetime(df["date"])
recent = df[df["date"].hdt.within("2d")]  # Rows within the last 2 days
```

#### Perform Unix-like operations on file paths

```python
file_paths = pd.Series(["/path/to/file1.txt", "/path/to/file2.txt"])
file_paths.unix.cp("/new/directory")
```

## Contributing

Contributions to `pardos` are welcome! Please feel free to submit a Pull Request.
