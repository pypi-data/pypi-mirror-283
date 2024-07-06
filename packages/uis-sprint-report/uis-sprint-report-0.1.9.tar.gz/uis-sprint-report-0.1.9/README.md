[![PyPI version](https://badge.fury.io/py/uis-sprint-report.svg)](https://badge.fury.io/py/uis-sprint-report)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# UIS Sprint Report

`UIS Sprint Report` is a command-line tool designed to generate detailed reports for sprint activities, manage sprint-related data through embeddings, and interact via a chat interface, specifically tailored for University Information Services.

## Installation

To install `UIS Sprint Report`, you can use pip:

```bash
pip install uis-sprint-report
```

Ensure that the Ollama local model server is running and that you have downloaded the necessary models locally before running this command-line tool.

## Usage

The tool is intended to be run with various commands based on the required operation: generating reports, creating PowerPoint presentations of sprint goals, or engaging in an interactive chat to query sprint statuses.

### Command-Line Interface

```bash
uis-sprint-report --access-token "YOUR_TOKEN" --command "pptx" --sprint-goals "Goal 1; Goal 2"
```

### Input Parameters

- `--api-base` (`str`): Base URL for API access. Default is `"https://gitlab.developers.cam.ac.uk/"`.
- `--access-token` (`str`): Access token for API authentication.
- `--command` (`str`): Command to execute. Options are `"report"`, `"pptx"`, or `"chat"`.
- `--group-id` (`int`): GitLab group ID. Default is `5`.
- `--iteration-id` (`int`): Iteration ID within the group. Default is `383`.
- `--labels` (`str`): Labels to filter the issues. Default is `"team::Identity"`.
- `--model` (`str`): Ollama model to use. Default is `"mistral:latest"`.
- `--cache-file` (`str`): Path to the cache file. Default is `".cache"`.
- `--chunk-size` (`int`): Size of the text chunks for processing. Default is `500`.
- `--chunk-overlap` (`int`): Overlap between text chunks. Default is `0`.
- `--max-tokens` (`int`): Maximum tokens for model inference. Default is `1500`.
- `--sprint-goals` (`str`): Description of sprint goals.
- `--pptx-file` (`str`): Path for saving the generated PowerPoint file. Default is `"sprint_goals.pptx"`.
- `--max-attempts` (`int`): Maximum attempts for generating a response. Default is `5`.

### Commands

- **report**: Generates a report detailing the sprint activities.
- **pptx**: Creates a PowerPoint presentation based on sprint activities and goals.
- **chat**: Starts an interactive chat session for querying sprint data.

Each command initializes the `ChatOllama` model with the specified `model` and `max_tokens`, then executes the function corresponding to the command.

## Features

- Integrated report generation from GitLab issues.
- PowerPoint presentation creation for sprint reviews.
- Interactive chat functionality for live sprint data querying.
- Supports local execution with Ollama models for enhanced data privacy and control.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://gitlab.developers.cam.ac.uk/ee345/demo/issues).

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
