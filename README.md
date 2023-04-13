# devAI

devAI is a cooperative and friendly AI assistant built using the GPT-4 architecture. This assistant is designed to be resourceful and helpful, providing answers and solutions to a wide range of questions and tasks. The devAI project consists of multiple tools, a custom prompt template, output parser, and language models to provide the best possible assistance to users.

## Features

- Friendly and cooperative AI assistant
- Based on the advanced GPT-4 architecture
- Customizable prompt templates and output parsers
- Multiple tools for different tasks, such as web search, terminal commands, and user input
- Integration with various language models, such as ChatOpenAI, HuggingFaceHub, and GPT4All

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system

### Installation and Running

1. Clone the devAI repository to your local machine.
2. Navigate to the project directory.
3. Build the Docker image by running `docker-compose build`.
4. Start the Docker container using `docker-compose up -d`.
5. Access the running container with `docker exec -it python_app /bin/bash`.
6. Run the devAI application by executing `python devAI.py`.
7. Interact with the AI assistant by providing questions or prompts.
8. To exit the application, type 'exit' and press Enter. To stop and remove the container, run `docker-compose down`.

## Contributions

Contributions to the devAI project are welcome! Feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
