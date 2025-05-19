# Contributing to LangGraphSemantic

We welcome contributions to the LangGraphSemantic project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/LangGraphSemantic.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Environment

The easiest way to set up a development environment is to use Docker:

```bash
docker-compose up -d
```

This will start Fuseki and Jupyter services. You can then access:
- Fuseki at http://localhost:3030
- Jupyter at http://localhost:8888

## Code Style

- Follow PEP 8 guidelines for Python code
- Use type hints wherever possible
- Write docstrings for all public functions, classes, and methods
- Keep lines under 100 characters

## Testing

Before submitting a pull request, please ensure that:

1. All existing tests pass
2. You've added tests for new functionality
3. The demo notebook runs without errors

Run tests with:

```bash
pytest tests/
```

## Pull Request Process

1. Update the README.md and documentation with details of changes if appropriate
2. Update the examples if necessary
3. Make sure all tests pass
4. Submit a pull request with a clear description of the changes

## Code of Conduct

Please be respectful and inclusive in all interactions related to this project.

## License

By contributing to LangGraphSemantic, you agree that your contributions will be licensed under the project's MIT License.
