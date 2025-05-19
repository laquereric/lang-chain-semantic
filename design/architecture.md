# LangGraphSemantic Architecture

## Overview

LangGraphSemantic is a library that bridges the gap between Pydantic models, SHACL shapes, and RDF stores, with a specific focus on integration with LangChain and LangGraph. This document outlines the high-level architecture of the system, its core components, and the data flow between them.

## System Architecture

The LangGraphSemantic system consists of the following major components:

1. **Core Converter**: Transforms Pydantic models to SHACL shapes and vice versa
2. **RDF Store Interface**: Manages communication with RDF triple stores (primarily Fuseki)
3. **LangChain/LangGraph Integration**: Connects the semantic capabilities to LangChain and LangGraph
4. **Validation Engine**: Ensures data conforms to the defined shapes

### Architecture Diagram

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  LangChain/         │     │  LangGraphSemantic  │     │  RDF Store          │
│  LangGraph          │     │  Core               │     │  (Fuseki)           │
│                     │     │                     │     │                     │
└─────────┬───────────┘     └─────────┬───────────┘     └─────────┬───────────┘
          │                           │                           │
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Pydantic Models    │────▶│  SHACL Shapes       │────▶│  RDF Triples        │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Core Components

### 1. Model Converter

The Model Converter is responsible for transforming Pydantic models into SHACL shapes:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Pydantic Model     │────▶│  Type Mapper        │────▶│  SHACL Shape        │
│  Introspection      │     │                     │     │  Generator          │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

#### Key Classes:
- `ModelIntrospector`: Analyzes Pydantic models using Python's introspection
- `TypeMapper`: Maps Python/Pydantic types to RDF/SHACL equivalents
- `ConstraintMapper`: Converts Pydantic constraints to SHACL constraints
- `ShapeGenerator`: Produces complete SHACL shapes from the mapped components

### 2. RDF Store Interface

The RDF Store Interface manages communication with RDF triple stores:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Store Connection   │────▶│  Query/Update       │────▶│  Triple Store       │
│  Manager            │     │  Executor           │     │  (Fuseki)           │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

#### Key Classes:
- `StoreConnection`: Manages connections to RDF stores
- `QueryExecutor`: Executes SPARQL queries
- `UpdateExecutor`: Executes SPARQL updates
- `TransactionManager`: Handles transaction management for batch operations

### 3. LangChain/LangGraph Integration

This component connects the semantic capabilities to LangChain and LangGraph:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  LangChain          │────▶│  Semantic           │────▶│  LangGraph          │
│  Components         │     │  Middleware         │     │  State Management   │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

#### Key Classes:
- `SemanticMemory`: Extends LangChain memory with semantic capabilities
- `SemanticRetriever`: Enhances retrieval with semantic queries
- `SemanticStateManager`: Manages LangGraph state with semantic validation

### 4. Validation Engine

The Validation Engine ensures data conforms to the defined shapes:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Data Validator     │────▶│  Validation         │────▶│  Error              │
│                     │     │  Reporter           │     │  Handler            │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

#### Key Classes:
- `ShapeValidator`: Validates data against SHACL shapes
- `ValidationReport`: Structures validation results
- `ErrorHandler`: Processes and formats validation errors

## Data Flow

### Pydantic to RDF Flow

1. **Model Registration**: A Pydantic model is registered with LangGraphSemantic
2. **Shape Generation**: The model is converted to a SHACL shape
3. **Shape Storage**: The shape is stored in the RDF store
4. **Instance Validation**: When model instances are created, they are validated against the shape
5. **Triple Generation**: Valid instances are converted to RDF triples
6. **Triple Storage**: The triples are stored in the RDF store

### RDF to Pydantic Flow

1. **Query Execution**: A SPARQL query retrieves data from the RDF store
2. **Triple Processing**: The retrieved triples are processed
3. **Shape Retrieval**: The corresponding SHACL shape is retrieved
4. **Model Generation**: A Pydantic model is generated or retrieved based on the shape
5. **Instance Creation**: The data is used to create an instance of the Pydantic model
6. **Validation**: The instance is validated against the Pydantic model's constraints

## Integration Points

### LangChain Integration

LangGraphSemantic integrates with LangChain through:

1. **Memory Components**: Enhanced memory with semantic capabilities
2. **Retrievers**: Semantic retrieval mechanisms
3. **Chains**: Custom chains for semantic processing

### LangGraph Integration

LangGraphSemantic integrates with LangGraph through:

1. **State Management**: Semantic validation of graph state
2. **Persistence**: RDF-based persistence of graph state
3. **Transitions**: Semantically validated state transitions

### Fuseki Integration

LangGraphSemantic integrates with Apache Jena Fuseki through:

1. **Connection Management**: Efficient connection handling
2. **Query Optimization**: Optimized SPARQL queries
3. **Transaction Support**: Proper transaction management
4. **Authentication**: Support for Fuseki's authentication mechanisms

## Deployment Architecture

The deployment architecture includes Docker containers for:

1. **Fuseki Server**: Stores RDF data and SHACL shapes
2. **Jupyter Notebook**: Provides an interactive environment for development and demonstration
3. **Application Container**: Hosts the LangGraphSemantic library and application code

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                           │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │                 │    │                 │    │              │ │
│  │  Fuseki Server  │◄───┤  Application    │◄───┤  Jupyter     │ │
│  │                 │    │                 │    │  Notebook    │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Conclusion

The LangGraphSemantic architecture provides a robust foundation for integrating Pydantic models with RDF stores through SHACL shapes, with specific support for LangChain and LangGraph. This architecture enables semantic validation, storage, and retrieval of structured data in a way that leverages the strengths of all involved technologies.
