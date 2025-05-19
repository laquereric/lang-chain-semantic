"""
Main module for the LangGraphSemantic library.

This module provides the main entry points and high-level interfaces
for the LangGraphSemantic library.
"""

from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel
from rdflib import Graph

from langgraphsemantic.core import ShapeGenerator, ModelIntrospector, TypeMapper
from langgraphsemantic.store import FusekiStore, StoreConnection, QueryExecutor, UpdateExecutor
from langgraphsemantic.integration import SemanticMemory, SemanticRetriever, SemanticModelRegistry


class LangGraphSemantic:
    """
    Main class for the LangGraphSemantic library.
    
    This class provides a high-level interface for working with semantic
    data in LangChain and LangGraph applications.
    """
    
    def __init__(self, fuseki_url: str, dataset: str, base_namespace: str = "http://example.org/"):
        """
        Initialize the LangGraphSemantic instance.
        
        Args:
            fuseki_url: The base URL of the Fuseki server
            dataset: The name of the dataset to use
            base_namespace: The base URI namespace for generated shapes
        """
        self.fuseki_url = fuseki_url
        self.dataset = dataset
        self.base_namespace = base_namespace
        
        # Initialize components
        self.store = FusekiStore(fuseki_url, dataset)
        self.shape_generator = ShapeGenerator(base_namespace)
        self.model_registry = SemanticModelRegistry(self.store, base_namespace)
        
    def register_model(self, model_class: Type[BaseModel]) -> bool:
        """
        Register a Pydantic model for semantic storage and validation.
        
        Args:
            model_class: The Pydantic model class to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        return self.model_registry.register_model(model_class)
    
    def store_instance(self, instance: BaseModel) -> bool:
        """
        Store a Pydantic model instance in the RDF store.
        
        Args:
            instance: The Pydantic model instance to store
            
        Returns:
            True if storage was successful, False otherwise
        """
        model_name = instance.__class__.__name__
        
        # Check if model is registered
        if not self.model_registry.get_model(model_name):
            # Try to register it
            if not self.register_model(instance.__class__):
                return False
        
        # Convert instance to RDF
        graph = self._instance_to_rdf(instance)
        
        # Store the instance data
        return self.store.store_instance_data(graph, model_name)
    
    def validate_instance(self, instance: BaseModel) -> Dict[str, Any]:
        """
        Validate a Pydantic model instance against its SHACL shape.
        
        Args:
            instance: The Pydantic model instance to validate
            
        Returns:
            A dictionary containing validation results
        """
        return self.model_registry.validate_instance(instance)
    
    def create_memory(self, memory_key: str = "semantic_memory") -> SemanticMemory:
        """
        Create a SemanticMemory instance for use with LangChain.
        
        Args:
            memory_key: The key to use for memory in chain inputs/outputs
            
        Returns:
            A SemanticMemory instance
        """
        return SemanticMemory(self.store, memory_key)
    
    def create_retriever(self) -> SemanticRetriever:
        """
        Create a SemanticRetriever instance for use with LangChain.
        
        Returns:
            A SemanticRetriever instance
        """
        return SemanticRetriever(self.store)
    
    def _instance_to_rdf(self, instance: BaseModel) -> Graph:
        """
        Convert a Pydantic model instance to an RDF graph.
        
        Args:
            instance: The Pydantic model instance to convert
            
        Returns:
            An RDFLib Graph containing the instance data
        """
        from rdflib import URIRef, Literal
        
        model_name = instance.__class__.__name__
        graph = Graph()
        
        # Create a URI for the instance
        instance_uri = URIRef(f"{self.base_namespace}{model_name}_{id(instance)}")
        
        # Add type triple
        graph.add((instance_uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), 
                  URIRef(f"{self.base_namespace}{model_name}")))
        
        # Add property triples
        for field_name, field_value in instance.dict().items():
            if field_value is not None:
                if isinstance(field_value, (str, int, float, bool)):
                    graph.add((instance_uri, URIRef(f"{self.base_namespace}{field_name}"), 
                              Literal(field_value)))
                elif isinstance(field_value, list):
                    for i, item in enumerate(field_value):
                        if isinstance(item, (str, int, float, bool)):
                            graph.add((instance_uri, URIRef(f"{self.base_namespace}{field_name}"), 
                                      Literal(item)))
                        elif isinstance(item, BaseModel):
                            # Handle nested models
                            nested_graph = self._instance_to_rdf(item)
                            graph += nested_graph
                            
                            # Link to the nested instance
                            nested_uri = URIRef(f"{self.base_namespace}{item.__class__.__name__}_{id(item)}")
                            graph.add((instance_uri, URIRef(f"{self.base_namespace}{field_name}"), 
                                      nested_uri))
                elif isinstance(field_value, BaseModel):
                    # Handle nested models
                    nested_graph = self._instance_to_rdf(field_value)
                    graph += nested_graph
                    
                    # Link to the nested instance
                    nested_uri = URIRef(f"{self.base_namespace}{field_value.__class__.__name__}_{id(field_value)}")
                    graph.add((instance_uri, URIRef(f"{self.base_namespace}{field_name}"), 
                              nested_uri))
        
        return graph


# Export main classes
__all__ = [
    'LangGraphSemantic',
    'ShapeGenerator',
    'FusekiStore',
    'SemanticMemory',
    'SemanticRetriever',
    'SemanticModelRegistry'
]
