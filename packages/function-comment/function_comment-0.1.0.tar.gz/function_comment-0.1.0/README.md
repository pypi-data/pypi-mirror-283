# function_comment

A Python library to create full-function comments using decorators.

## Installation

You can install the package using pip:

```bash
pip install function_comment


```python
from function_comment import bbkp, ujmp

@bbkp
@ujmp
def some_function():
    print("This should not be printed")

def normal_function():
    print("This should be printed")

if __name__ == "__main__":
    some_function()       # This will do nothing
    normal_function()     # This will print "This should be printed"
