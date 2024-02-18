# QueryFlattenMiddleware for FastAPI

`QueryFlattenMiddleware` is a custom middleware for FastAPI applications that flattens query parameters separated by a specified delimiter. This is particularly useful for endpoints that need to handle multiple values for the same query parameter without using the standard array format. 

## Features

- **Customizable Delimiter**: Easily configure the delimiter used for splitting query parameter values.
- **Seamless Integration**: Works as middleware within any FastAPI application.
- **Efficient Query Handling**: Simplifies the process of handling multiple query parameters by flattening them, making endpoint logic cleaner and more straightforward.

## Requirements

- Python 3.8.1+
- FastAPI

## Installation

To install `QueryFlattenMiddleware`, you can use pip:

```bash
pip install fastapi-query-flatten
```

## Usage

To use `QueryFlattenMiddleware` in your FastAPI application, simply add it as middleware in your app instance. Specify the delimiter you want to use for splitting query parameter values. The default delimiter is a comma (`,`).

### Example

```python
from fastapi import FastAPI
from fastapi_query_flatten import QueryFlattenMiddleware

app = FastAPI()

# Add QueryFlattenMiddleware with a custom delimiter
app.add_middleware(QueryFlattenMiddleware, delimiter=",")
```

With the middleware in place, a request to `/items/?filter=value1,value2,value3` will be processed as if it were `/items/?filter=value1&filter=value2&filter=value3`, allowing the `filter` query parameter to be easily handled as multiple values.

## Contributing

Contributions are welcome! If you have a feature request, bug report, or a pull request, please open an issue or submit a PR on the project's repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
