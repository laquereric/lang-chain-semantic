# Pydantic to SHACL Mapping Analysis

## Overview

This document analyzes the mapping between Pydantic models and SHACL (Shapes Constraint Language) shapes, which is essential for the LangGraphSemantic project. The goal is to establish a clear and comprehensive mapping that will allow Pydantic models to be converted to SHACL shapes and stored in RDF stores.

## Pydantic Model Structure

Pydantic models are Python classes that provide data validation and settings management using Python type annotations. Key features include:

1. **Type Annotations**: Pydantic uses Python's type hints to validate data.
2. **Field Constraints**: Additional validation rules can be applied to fields.
3. **Nested Models**: Models can contain other models as fields.
4. **Custom Validators**: Custom validation logic can be added through validator decorators.
5. **Field Descriptions**: Fields can have descriptions and examples.

Example of a Pydantic model:

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str = Field(..., min_length=2, max_length=2)
    
    @validator('country')
    def country_must_be_iso_code(cls, v):
        if not v.isupper():
            raise ValueError('Country code must be uppercase')
        return v

class Person(BaseModel):
    id: str
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, lt=150)
    email: Optional[str] = None
    addresses: List[Address] = []
    created_at: datetime
    tags: List[str] = []
```

## SHACL Shape Structure

SHACL shapes are RDF constructs that define constraints for validating RDF data. Key components include:

1. **Node Shapes**: Define constraints that apply to nodes in the data graph.
2. **Property Shapes**: Define constraints on properties and their values.
3. **Targets**: Specify which nodes in the data graph should be validated.
4. **Constraints**: Rules that the data must satisfy.
5. **Severity**: Indicates the importance of constraint violations.

Example of a SHACL shape:

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ex:name ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:minLength 1 ;
    ] ;
    sh:property [
        sh:path ex:age ;
        sh:datatype xsd:integer ;
        sh:minCount 1 ;
        sh:minInclusive 0 ;
        sh:maxExclusive 150 ;
    ] ;
    sh:property [
        sh:path ex:email ;
        sh:datatype xsd:string ;
        sh:maxCount 1 ;
    ] .
```

## Mapping Pydantic to SHACL

### Type Mapping

| Pydantic Type | SHACL Constraint |
|---------------|------------------|
| `str` | `sh:datatype xsd:string` |
| `int` | `sh:datatype xsd:integer` |
| `float` | `sh:datatype xsd:decimal` or `sh:datatype xsd:double` |
| `bool` | `sh:datatype xsd:boolean` |
| `datetime` | `sh:datatype xsd:dateTime` |
| `date` | `sh:datatype xsd:date` |
| `time` | `sh:datatype xsd:time` |
| `UUID` | `sh:datatype xsd:string` with pattern constraint |
| `List[T]` | Multiple property values with `sh:datatype` based on `T` |
| `Dict` | Complex mapping requiring custom logic |
| `Union[T1, T2]` | `sh:or` with shapes for each type |
| `Optional[T]` | `sh:maxCount 1` without `sh:minCount` |
| Custom class | Reference to another shape |

### Constraint Mapping

| Pydantic Constraint | SHACL Constraint |
|---------------------|------------------|
| `min_length` | `sh:minLength` |
| `max_length` | `sh:maxLength` |
| `regex` | `sh:pattern` |
| `ge` (>=) | `sh:minInclusive` |
| `gt` (>) | `sh:minExclusive` |
| `le` (<=) | `sh:maxInclusive` |
| `lt` (<) | `sh:maxExclusive` |
| Required field | `sh:minCount 1` |
| Optional field | No `sh:minCount` |
| `@validator` | `sh:sparql` with custom SPARQL query |
| `Literal` values | `sh:in` with list of allowed values |

### Nested Model Mapping

For nested Pydantic models, the mapping creates separate SHACL shapes for each model and links them using `sh:node`:

```turtle
ex:PersonShape
    sh:property [
        sh:path ex:address ;
        sh:node ex:AddressShape ;
    ] .
```

### List Field Mapping

For list fields, the mapping depends on the type of items in the list:

1. **Primitive Types**: Use `sh:datatype` with appropriate cardinality.
2. **Complex Types**: Use `sh:node` with appropriate cardinality.

```turtle
# List of strings
sh:property [
    sh:path ex:tags ;
    sh:datatype xsd:string ;
] .

# List of Address objects
sh:property [
    sh:path ex:addresses ;
    sh:node ex:AddressShape ;
] .
```

### Custom Validators Mapping

Pydantic custom validators are mapped to SPARQL-based constraints in SHACL:

```turtle
ex:CountryShape
    sh:property [
        sh:path ex:code ;
        sh:sparql [
            sh:select """
                SELECT $this ?value
                WHERE {
                    $this ex:code ?value .
                    FILTER (!regex(?value, '^[A-Z]{2}$'))
                }
            """ ;
        ] ;
    ] .
```

## Implementation Strategy

The implementation of the Pydantic-to-SHACL mapping will follow these steps:

1. **Model Introspection**: Analyze Pydantic models using Python's introspection capabilities.
2. **Graph Construction**: Build RDF graphs representing SHACL shapes based on the model structure.
3. **Constraint Translation**: Convert Pydantic constraints to equivalent SHACL constraints.
4. **Validation**: Ensure the generated SHACL shapes correctly validate data according to the original Pydantic models.
5. **Serialization**: Output the SHACL shapes in a suitable RDF format (Turtle, RDF/XML, etc.).

## Challenges and Solutions

### Challenge 1: Complex Validators

Pydantic allows for complex validation logic through custom validators, which may not have direct equivalents in SHACL.

**Solution**: Use SPARQL-based constraints in SHACL to implement complex validation logic. For validators that cannot be expressed in SPARQL, provide extension points in the library.

### Challenge 2: Union Types

Pydantic's Union types represent values that could be of multiple types, which requires special handling in SHACL.

**Solution**: Use `sh:or` to create a disjunction of shapes, each representing one possible type.

### Challenge 3: Dynamic Models

Pydantic supports dynamic model creation, which can be challenging to map to static SHACL shapes.

**Solution**: Implement a runtime model analyzer that can generate SHACL shapes on-the-fly based on the structure of dynamic models.

### Challenge 4: Bidirectional Mapping

For some use cases, it may be necessary to convert SHACL shapes back to Pydantic models.

**Solution**: Implement a bidirectional mapper that can generate Pydantic models from SHACL shapes, with appropriate limitations documented.

## Conclusion

The mapping between Pydantic models and SHACL shapes provides a solid foundation for the LangGraphSemantic project. By leveraging the strengths of both technologies, we can create a powerful interface for storing and validating structured data in RDF stores, while maintaining the ease of use and type safety provided by Pydantic.
