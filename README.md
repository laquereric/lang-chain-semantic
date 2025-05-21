# LangChainSemantic

LangChainSemantic is a library that connects Pydantic models to SHACL shapes in RDF stores, with specific support for LangChain and LangGraph. It enables semantic validation, storage, and retrieval of structured data in a way that leverages the strengths of all involved technologies.

## Features

- Convert Pydantic models to SHACL shapes for RDF validation
- Store and retrieve model instances in RDF triple stores
- Validate data against semantic constraints
- Integrate with LangChain for semantic memory and retrieval
- Support for LangGraph state management with semantic validation

## Installation

```bash
pip install langgraphsemantic
```

## Quick Start

```python
from pydantic import BaseModel, Field
from langgraphsemantic import LangGraphSemantic

# Define a Pydantic model
class Person(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, lt=150)
    email: str = None

# Initialize LangGraphSemantic
semantic = LangGraphSemantic(
    fuseki_url="http://localhost:3030",
    dataset="langgraphsemantic",
    base_namespace="http://example.org/"
)

# Register the model (generates SHACL shape)
semantic.register_model(Person)

# Create and store an instance
person = Person(name="John Doe", age=30, email="john.doe@example.com")
semantic.store_instance(person)

# Validate the instance
validation_result = semantic.validate_instance(person)
print(f"Validation result: {validation_result}")
```

## Docker Setup

The project includes Docker configuration for easy setup of a development environment with Fuseki and Jupyter:

```bash
docker-compose up -d
```

This will start:
- Apache Jena Fuseki server on port 3030
- Jupyter Lab on port 8888

## Documentation

For detailed documentation, see the [examples](./examples) directory and the [demo notebook](./examples/demo_notebook.ipynb).

## Architecture

LangGraphSemantic consists of several core components:

1. **Model Converter**: Transforms Pydantic models into SHACL shapes
2. **RDF Store Interface**: Manages communication with RDF triple stores
3. **LangChain/LangGraph Integration**: Connects semantic capabilities to LangChain and LangGraph
4. **Validation Engine**: Ensures data conforms to defined shapes

## Requirements

- Python 3.8+
- RDFLib
- SPARQLWrapper
- Pydantic
- LangChain
- Docker (for running Fuseki)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
