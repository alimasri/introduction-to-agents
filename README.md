# Introduction to AI Agents Workshop

Welcome to this hands-on workshop on AI Agents! This project is designed to help you understand and experiment with AI agents using modern tools and frameworks. Through practical examples and interactive exercises, you'll learn how to build and work with AI agents that can perform various tasks.

## What You'll Learn

- Understanding the fundamentals of AI agents
- Building agents using LangChain and related libraries
- Working with different types of agents and their use cases
- Best practices for agent development and deployment

## Workshop Structure

The workshop is organized into several components:

### 1. Interactive Workshop Notebook
The `workshop.ipynb` notebook contains the main workshop content, including:
- Theoretical concepts and explanations
- Code examples
- Hands-on exercises
- Real-world use cases

### 2. Example Implementations
The `code/` directory contains practical examples:
- `filemanager_agent.py`: A demonstration of an agent that can manage files
- `sales.py` and `sales_data_generator.py`: Examples of agents working with data
- `sales.parquet`: Sample dataset for the exercises

## Prerequisites

Before starting the workshop, ensure you have:
- Python 3.12 installed
- Basic understanding of Python programming
- Familiarity with Jupyter notebooks
- OpenAI API key (for LangChain integration)
- `uv` package manager installed
- Langsmith API key (optional)

## Setup Instructions

1. Clone this repository:
```bash
git clone <repository-url>
cd introduction-to-agents
```

2. Setup your virtual environment and install the necessary packages:
```bash
uv sync
```

3. Set up your environment variables:
```bash
cp .env.example .env_vars
# Edit .env with your OpenAI API key and other configurations
```

## Workshop Resources

- The `assets/` directory contains additional resources and materials
- The `workshop.ipynb` notebook is your main guide through the workshop
- Example code in the `code/` directory serves as reference implementations

## Author

Ali Masri <https://alimasri.info>