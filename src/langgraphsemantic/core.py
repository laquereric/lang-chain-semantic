"""
Core module for converting Pydantic models to SHACL shapes.

This module provides the main functionality for analyzing Pydantic models
and generating equivalent SHACL shapes for RDF validation.
"""

from typing import Any, Dict, List, Optional, Set, Type, Union
import inspect
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, SH
import pydantic
from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField


class ModelIntrospector:
    """
    Analyzes Pydantic models using Python's introspection capabilities.
    
    This class extracts information about fields, types, and validation
    rules from Pydantic models to facilitate conversion to SHACL shapes.
    """
    
    def __init__(self, base_namespace: str = "http://example.org/"):
        """
        Initialize the ModelIntrospector.
        
        Args:
            base_namespace: The base URI namespace for generated shapes
        """
        self.base_namespace = base_namespace
        self.ns = Namespace(base_namespace)
        
    def introspect_model(self, model_class: Type[BaseModel]) -> Dict[str, Any]:
        """
        Extract metadata from a Pydantic model class.
        
        Args:
            model_class: The Pydantic model class to analyze
            
        Returns:
            A dictionary containing model metadata
        """
        model_name = model_class.__name__
        fields = {}
        
        for name, field in model_class.__fields__.items():
            field_info = self._extract_field_info(field)
            fields[name] = field_info
            
        validators = self._extract_validators(model_class)
        
        return {
            "name": model_name,
            "fields": fields,
            "validators": validators,
            "doc": model_class.__doc__,
            "config": getattr(model_class, "Config", None)
        }
    
    def _extract_field_info(self, field: ModelField) -> Dict[str, Any]:
        """
        Extract information from a Pydantic model field.
        
        Args:
            field: The Pydantic ModelField to analyze
            
        Returns:
            A dictionary containing field metadata
        """
        field_type = field.outer_type_
        constraints = {}
        
        # Extract field constraints
        if field.field_info.min_length is not None:
            constraints["min_length"] = field.field_info.min_length
            
        if field.field_info.max_length is not None:
            constraints["max_length"] = field.field_info.max_length
            
        if field.field_info.regex is not None:
            constraints["pattern"] = field.field_info.regex.pattern
            
        if field.field_info.gt is not None:
            constraints["gt"] = field.field_info.gt
            
        if field.field_info.ge is not None:
            constraints["ge"] = field.field_info.ge
            
        if field.field_info.lt is not None:
            constraints["lt"] = field.field_info.lt
            
        if field.field_info.le is not None:
            constraints["le"] = field.field_info.le
            
        return {
            "type": field_type,
            "required": field.required,
            "default": field.default if not field.required else None,
            "description": field.field_info.description,
            "constraints": constraints
        }
    
    def _extract_validators(self, model_class: Type[BaseModel]) -> List[Dict[str, Any]]:
        """
        Extract validator functions from a Pydantic model.
        
        Args:
            model_class: The Pydantic model class to analyze
            
        Returns:
            A list of dictionaries containing validator metadata
        """
        validators = []
        
        for name, method in inspect.getmembers(model_class):
            if hasattr(method, "__validators__"):
                for field_name, validator_info in method.__validators__:
                    validators.append({
                        "field": field_name,
                        "function": method,
                        "mode": validator_info.get("mode", ""),
                        "pre": validator_info.get("pre", False)
                    })
                    
        return validators


class TypeMapper:
    """
    Maps Python/Pydantic types to RDF/SHACL equivalents.
    
    This class provides functionality to convert Python type annotations
    to appropriate RDF datatypes and SHACL constraints.
    """
    
    def __init__(self):
        """Initialize the TypeMapper."""
        self.type_map = {
            str: XSD.string,
            int: XSD.integer,
            float: XSD.decimal,
            bool: XSD.boolean,
            # Add more type mappings as needed
        }
        
    def map_type(self, python_type: Type) -> Optional[URIRef]:
        """
        Map a Python type to an RDF datatype.
        
        Args:
            python_type: The Python type to map
            
        Returns:
            The corresponding RDF datatype URI or None if no mapping exists
        """
        # Handle basic types
        if python_type in self.type_map:
            return self.type_map[python_type]
        
        # Handle Optional types
        origin = getattr(python_type, "__origin__", None)
        args = getattr(python_type, "__args__", [])
        
        if origin is Union and type(None) in args:
            # This is an Optional type
            for arg in args:
                if arg is not type(None):
                    return self.map_type(arg)
        
        # Handle List types
        if origin is list:
            if args and len(args) == 1:
                # Return the type of list items
                return self.map_type(args[0])
        
        # Handle custom Pydantic models
        if inspect.isclass(python_type) and issubclass(python_type, BaseModel):
            # For custom models, we'll return None and handle them separately
            return None
            
        # Default to string if no mapping is found
        return XSD.string


class ShapeGenerator:
    """
    Produces complete SHACL shapes from Pydantic models.
    
    This class generates RDF graphs containing SHACL shapes based on
    the structure and validation rules of Pydantic models.
    """
    
    def __init__(self, base_namespace: str = "http://example.org/"):
        """
        Initialize the ShapeGenerator.
        
        Args:
            base_namespace: The base URI namespace for generated shapes
        """
        self.base_namespace = base_namespace
        self.ns = Namespace(base_namespace)
        self.introspector = ModelIntrospector(base_namespace)
        self.type_mapper = TypeMapper()
        
    def generate_shape(self, model_class: Type[BaseModel]) -> Graph:
        """
        Generate a SHACL shape from a Pydantic model.
        
        Args:
            model_class: The Pydantic model class to convert
            
        Returns:
            An RDF graph containing the SHACL shape
        """
        model_info = self.introspector.introspect_model(model_class)
        graph = Graph()
        
        # Bind common namespaces
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("xsd", XSD)
        graph.bind("sh", SH)
        graph.bind("ex", self.ns)
        
        # Create the node shape
        shape_uri = self.ns[f"{model_info['name']}Shape"]
        graph.add((shape_uri, RDF.type, SH.NodeShape))
        graph.add((shape_uri, SH.targetClass, self.ns[model_info['name']]))
        
        if model_info['doc']:
            graph.add((shape_uri, RDFS.comment, Literal(model_info['doc'])))
        
        # Add property shapes for each field
        for field_name, field_info in model_info['fields'].items():
            self._add_property_shape(graph, shape_uri, field_name, field_info)
        
        return graph
    
    def _add_property_shape(self, graph: Graph, shape_uri: URIRef, 
                           field_name: str, field_info: Dict[str, Any]) -> None:
        """
        Add a property shape for a field to the graph.
        
        Args:
            graph: The RDF graph to add to
            shape_uri: The URI of the parent node shape
            field_name: The name of the field
            field_info: The field metadata
        """
        # Create a blank node for the property shape
        prop_shape = BNode()
        graph.add((shape_uri, SH.property, prop_shape))
        
        # Add path
        graph.add((prop_shape, SH.path, self.ns[field_name]))
        
        # Add description if available
        if field_info['description']:
            graph.add((prop_shape, SH.description, Literal(field_info['description'])))
        
        # Add datatype if applicable
        field_type = field_info['type']
        datatype = self.type_mapper.map_type(field_type)
        
        if datatype:
            graph.add((prop_shape, SH.datatype, datatype))
        
        # Add cardinality constraints
        if field_info['required']:
            graph.add((prop_shape, SH.minCount, Literal(1)))
        
        # Add other constraints
        constraints = field_info['constraints']
        
        if 'min_length' in constraints:
            graph.add((prop_shape, SH.minLength, Literal(constraints['min_length'])))
            
        if 'max_length' in constraints:
            graph.add((prop_shape, SH.maxLength, Literal(constraints['max_length'])))
            
        if 'pattern' in constraints:
            graph.add((prop_shape, SH.pattern, Literal(constraints['pattern'])))
            
        if 'gt' in constraints:
            graph.add((prop_shape, SH.minExclusive, Literal(constraints['gt'])))
            
        if 'ge' in constraints:
            graph.add((prop_shape, SH.minInclusive, Literal(constraints['ge'])))
            
        if 'lt' in constraints:
            graph.add((prop_shape, SH.maxExclusive, Literal(constraints['lt'])))
            
        if 'le' in constraints:
            graph.add((prop_shape, SH.maxInclusive, Literal(constraints['le'])))
