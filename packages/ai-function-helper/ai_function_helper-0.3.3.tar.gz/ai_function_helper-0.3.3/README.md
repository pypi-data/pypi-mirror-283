# AI Function Helper

[![PyPI version](https://badge.fury.io/py/ai-function-helper.svg)](https://badge.fury.io/py/ai-function-helper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-function-helper.svg)](https://pypi.org/project/ai-function-helper/)

**Streamline your AI-powered Python functions with ease!**


## 🌟 Key Features

- **Seamless OpenAI Integration**: Easy setup with various AI models (GPT-3.5, GPT-4, Mistral, etc.)
- **Flexible Function Decorators**: Customize AI-powered tasks with ease
- **Synchronous and Asynchronous Support**: Use AI functions in both sync and async contexts
- **Batch Processing**: Efficiently handle multiple inputs in a single API call
- **Robust Error Handling**: Automatic retries and comprehensive error management
- **Type Safety**: Pydantic models for JSON parsing and validation
- **Debugging Capabilities**: Detailed logging of API interactions
- **Function Calling**: Support for OpenAI's function calling feature
- **Multiple Return Formats**: Flexible output handling (JSON, string, raw response)
- **Image Input Support**: Process and analyze images within your AI functions
- **JSON Mode**: Automatic JSON response formatting for compatible models
- **Customizable System Prompts**: Fine-tune AI behavior with detailed instructions
- **Error Prevention**: Block hijacking attempts and ensure adherence to function parameters
- **Conversation History**: Maintain context across multiple interactions using HistoryInput
- **Timeout Management**: Set custom timeouts for API calls
- **Custom Base URL**: Support for custom OpenAI-compatible endpoints

## 📚 Table of Contents

- [AI Function Helper](#ai-function-helper)
  - [🌟 Key Features](#-key-features)
  - [📚 Table of Contents](#-table-of-contents)
  - [🚀 Installation](#-installation)
  - [🏁 Quick Start](#-quick-start)
  - [🧠 Core Concepts](#-core-concepts)
  - [🔧 Advanced Usage](#-advanced-usage)
    - [Customizing AI Function Behavior](#customizing-ai-function-behavior)
    - [Using HistoryInput for Conversation Context](#using-historyinput-for-conversation-context)
    - [Image Input Support](#image-input-support)
    - [JSON Mode Support](#json-mode-support)
    - [Asynchronous Usage](#asynchronous-usage)
    - [Error Handling and Debugging](#error-handling-and-debugging)
    - [Timeout Management](#timeout-management)
    - [Custom Base URL](#custom-base-url)
    - [System Message Customization](#system-message-customization)
  - [🛠️ Using Tools (Function Calling)](#️-using-tools-function-calling)
  - [📘 Examples](#-examples)
    - [Simple Text Generation](#simple-text-generation)
    - [Interactive Quiz Bot](#interactive-quiz-bot)
    - [Data Analysis Assistant](#data-analysis-assistant)
    - [Complex Travel Planner](#complex-travel-planner)

## 🚀 Installation

Install AI Function Helper using pip:

```bash
pip install ai-function-helper
```

## 🏁 Quick Start

Get up and running with AI Function Helper in just a few lines of code:

```python
from ai_function_helper import AIFunctionHelper

# Initialize AI Function Helper
ai_helper = AIFunctionHelper("your-api-key")

# Create an AI-powered function
@ai_helper.ai_function(model="gpt-3.5-turbo", max_tokens=200)
def generate_short_story(theme: str) -> str:
    """
    Generate a short story based on a given theme.
    """

# Use the function
story = generate_short_story(theme="A day in the life of a time traveler")
print(story)
```

## 🧠 Core Concepts

AI Function Helper is built around several key concepts:

1. **AIFunctionHelper Class**: The main entry point for creating AI-powered functions.
2. **AI Function Decorator**: Transforms regular Python functions into AI-powered ones, supporting both sync and async usage.
3. **Pydantic Models**: Ensures type safety and easy validation of AI-generated responses.
4. **Error Handling**: Built-in mechanisms for handling API errors and retrying failed calls.
5. **Debugging**: Comprehensive logging options for troubleshooting and optimization.
6. **JSON Mode**: Automatic JSON response formatting for compatible models.
7. **System Prompts**: Customizable instructions to guide AI behavior.
8. **HistoryInput**: Allows for maintaining conversation context across multiple interactions.
9. **ImageInput**: Supports processing and analysis of images within AI functions.
10. **Tools**: Enables the use of custom functions within the AI's reasoning process.

## 🔧 Advanced Usage

### Customizing AI Function Behavior

Fine-tune your AI functions with various parameters:

```python
@ai_helper.ai_function(
    model="gpt-4o",
    max_tokens=500,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    timeout=60,
    show_debug=True,
    debug_level=2,
    force_json_mode=True,
    block_hijack=True,
    block_hijack_throw_error=False,
    language="French",
    disable_prefill=False
)
def advanced_function(input_data: str) -> ComplexResponseModel:
    """
    An advanced AI-powered function with custom settings.
    """
```

### Using HistoryInput for Conversation Context

The `HistoryInput` class allows you to maintain conversation history across multiple interactions:

```python
from ai_function_helper import AIFunctionHelper, HistoryInput

@ai_helper.ai_function(model="gpt-3.5-turbo", max_tokens=4000)
async def chat_response(history: HistoryInput, user_input: str) -> str:
    """
    Generate a chat response based on the conversation history and user input.
    """

# Usage
chat_history = HistoryInput([
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing well, thank you! How can I assist you today?"}
])

response = await chat_response(history=chat_history, user_input="Tell me a joke")
```

### Image Input Support

Process and analyze images within your AI functions:

```python
from ai_function_helper import AIFunctionHelper, ImageInput
from pathlib import Path

@ai_helper.ai_function(model="gpt-4-vision-preview", max_tokens=300)
def analyze_image(image: ImageInput) -> str:
    """
    Analyze the contents of the image and provide a description.
    """

# Using a URL
result = analyze_image(image=ImageInput(url="https://example.com/image.jpg"))

# Using a local file
result = analyze_image(image=ImageInput(url=Path("local_image.jpg")))
```

### JSON Mode Support

AI Function Helper supports automatic JSON mode for compatible models. The following models are currently supported:

- gpt-4o, gpt-4-turbo, gpt-4-turbo-2024-04-09, gpt-3.5-turbo
- gpt-4-1106-preview, gpt-3.5-turbo-1106, gpt-4-0125-preview
- gpt-3.5-turbo-0125, gpt-4-turbo-preview
- mistral-small-2402, mistral-small-latest, mistral-large-2402, mistral-large-latest

You can add support for additional models using the `add_json_mode_models` method:

```python
AIFunctionHelper.add_json_mode_models(["new-model-1", "new-model-2"])
```

### Asynchronous Usage

AI Function Helper supports both synchronous and asynchronous functions:

```python
@ai_helper.ai_function(model="gpt-3.5-turbo")
async def async_function(input_data: str) -> str:
    """
    An asynchronous AI-powered function.
    """

# Usage
import asyncio

async def main():
    result = await async_function("Hello, AI!")
    print(result)

asyncio.run(main())
```

### Error Handling and Debugging

Enable detailed logging and set retry attempts:

```python
AIFunctionHelper.set_max_retries(3)  # Set max retries globally

@ai_helper.ai_function(show_debug=True, debug_level=2)
def debug_example(input_data: str) -> str:
    """
    This function will display detailed debug information.
    """
```

### Timeout Management

Set custom timeouts for API calls:

```python
@ai_helper.ai_function(timeout=30)
def time_sensitive_function(input_data: str) -> str:
    """
    This function will timeout after 30 seconds if no response is received.
    """
```

### Custom Base URL

Support for custom OpenAI-compatible endpoints:

```python
ai_helper = AIFunctionHelper("your-api-key", base_url="https://your-custom-endpoint.com/v1")
```

### System Message Customization

Customize the system message to guide the AI's behavior:

```python
@ai_helper.ai_function(
    model="gpt-4o",
    language="Spanish",
    block_hijack=True
)
def spanish_assistant(query: str) -> str:
    """
    A Spanish-speaking assistant that resists hijacking attempts.
    """
```

## 🛠️ Using Tools (Function Calling)

AI Function Helper supports OpenAI's function calling feature, allowing you to define custom functions that the AI can use during its reasoning process:

```python
def get_weather(city: str) -> dict:
    """Get the current weather for a city."""
    # Implementation here

@ai_helper.ai_function(
    model="gpt-4o",
    tools=[get_weather]
)
def plan_trip(destination: str) -> str:
    """
    Plan a trip to the specified destination, considering the weather.
    """

result = plan_trip("Paris")
```

## 📘 Examples

### Simple Text Generation

```python
@ai_helper.ai_function(model="gpt-3.5-turbo", max_tokens=100)
def generate_haiku(theme: str) -> str:
    """
    Generate a haiku based on the given theme.
    The haiku should follow the 5-7-5 syllable structure and capture the essence of the theme.
    """

haiku = generate_haiku(theme="autumn leaves")
print(haiku)
```

### Interactive Quiz Bot

```python
from pydantic import BaseModel
from typing import List

class QuizQuestion(BaseModel):
    question: str
    correct_answer: str

@ai_helper.ai_function(model="gpt-3.5-turbo", max_tokens=1500)
async def generate_quiz(topic: str, num_questions: int) -> List[QuizQuestion]:
    """
    Generate a quiz on the given topic with the specified number of questions.
    Each question should be challenging but appropriate for a general audience.
    Provide a clear and concise correct answer for each question.
    """

# Usage
questions = await generate_quiz("Python programming", 3)
for q in questions:
    print(f"Q: {q.question}")
    print(f"A: {q.correct_answer}\n")
```

### Data Analysis Assistant

```python
from pydantic import BaseModel
from typing import List, Dict

class DataPoint(BaseModel):
    timestamp: str
    value: float
    category: str

class AnalysisResult(BaseModel):
    summary: str
    trend: str
    anomalies: List[Dict[str, any]]

@ai_helper.ai_function(model="gpt-4o", max_tokens=1000)
async def analyze_data(data: List[DataPoint]) -> AnalysisResult:
    """
    Analyze the given series of data points and provide insights.
    Your analysis should include:
    1. A brief summary of the overall data trends.
    2. Identification of the primary trend (increasing, decreasing, or stable).
    3. Detection of any anomalies or outliers in the data.
    Use statistical reasoning to support your analysis.
    """

# Usage
data = [
    DataPoint(timestamp="2023-01-01", value=100, category="A"),
    DataPoint(timestamp="2023-01-02", value=110, category="B"),
    DataPoint(timestamp="2023-01-03", value=105, category="A"),
    DataPoint(timestamp="2023-01-04", value=200, category="B"),
    DataPoint(timestamp="2023-01-05", value=115, category="A"),
]
result = await analyze_data(data)
print(f"Summary: {result.summary}")
print(f"Trend: {result.trend}")
print("Anomalies:", result.anomalies)
```

### Complex Travel Planner

```python
from pydantic import BaseModel, Field
from typing import List

class Destination(BaseModel):
    city: str
    country: str
    days: int

class Activity(BaseModel):
    name: str
    description: str
    duration: float

class TravelPlan(BaseModel):
    destinations: List[Destination]
    activities: List[Activity]
    budget_estimate: float

def get_weather(city: str, date: str) -> dict:
    """Mock function to get weather forecast"""
    return {"temperature": "25°C", "condition": "Sunny"}

def find_hotels(city: str, check_in: str, guests: int) -> List[dict]:
    """Mock function to find hotels"""
    return [{"name": "Grand Hotel", "price": 150}, {"name": "Cozy Inn", "price": 100}]

@ai_helper.ai_function(
    model="gpt-4o",
    max_tokens=2000,
    tools=[get_weather, find_hotels]
)
async def plan_trip(destinations: List[str], duration: int, interests: List[str]) -> TravelPlan:
    """
    Create a comprehensive travel plan based on the given destinations, duration, and interests.
    Use the provided tools to get weather information and find hotels.
    """

# Usage
plan = await plan_trip(
    destinations=["Paris", "Rome"],
    duration=7,
    interests=["history", "food", "art"]
)
print(plan)
```
