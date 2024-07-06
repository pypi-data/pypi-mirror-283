# AI Function Helper

AI Function Helper is a Python package that simplifies the process of creating AI-powered functions using OpenAI's API. It provides a flexible and easy-to-use interface for defining and executing AI-assisted tasks.

## Features

- Easy integration with OpenAI's API
- Supports various AI models
- Customizable function decorators
- Built-in error handling and retrying
- JSON parsing and validation
- Debug mode for detailed logging

## Installation

You can install the AI Function Helper using pip:

```
pip install ai-function-helper
```

## Usage

Here's a quick example of how to use AI Function Helper:

```python
from ai_function_helper import AIFunctionHelper
from pydantic import BaseModel

ai_helper = AIFunctionHelper("your-api-key", "http://your-api-base-url")

class ResponseModel(BaseModel):
    result: str

@ai_helper.ai_function(model="your-preferred-model")
async def example_function(ai_result: ResponseModel, input_data: str) -> ResponseModel:
    """
    Your function description here.
    """
    return ai_result

# Use the function
result = await example_function(input_data="Your input here")
print(result.result)
```

For more detailed usage instructions and examples, please refer to the documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.