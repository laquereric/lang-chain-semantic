"""
Integration module for connecting LangGraphSemantic with LangChain and LangGraph.

This module provides components that integrate semantic capabilities with
LangChain and LangGraph frameworks.
"""

from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel
from rdflib import Graph, URIRef, Literal
import langchain
from langchain.memory import BaseMemory
from langchain.schema import BaseRetriever

from langgraphsemantic.core import ShapeGenerator
from langgraphsemantic.store import FusekiStore


class SemanticMemory(BaseMemory):
    """
    Memory component that stores and retrieves data using semantic representations.
    
    This class extends LangChain's BaseMemory to provide semantically-enhanced
    memory capabilities using RDF and SHACL.
    """
    
    def __init__(self, 
                 store: FusekiStore,
                 memory_key: str = "semantic_memory",
                 return_messages: bool = False):
        """
        Initialize the SemanticMemory.
        
        Args:
            store: The FusekiStore instance for data storage
            memory_key: The key to use for memory in chain inputs/outputs
            return_messages: Whether to return memory as messages
        """
        self.store = store
        self.memory_key = memory_key
        self.return_messages = return_messages
        self.shape_generator = ShapeGenerator()
        
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load memory variables based on the inputs.
        
        Args:
            inputs: The inputs dictionary
            
        Returns:
            A dictionary containing memory variables
        """
        # This is a simplified implementation
        # In a real implementation, you would query the RDF store based on inputs
        
        query = f"""
        SELECT ?subject ?predicate ?object
        WHERE {{
            GRAPH <{self.store.data_graph_uri}/memory> {{
                ?subject ?predicate ?object
            }}
        }}
        LIMIT 10
        """
        
        try:
            results = self.store.query.execute_select(query)
            
            # Convert results to a more usable format
            memory_data = []
            for result in results:
                memory_data.append({
                    "subject": str(result.get("subject", "")),
                    "predicate": str(result.get("predicate", "")),
                    "object": str(result.get("object", ""))
                })
                
            return {self.memory_key: memory_data}
        except Exception as e:
            print(f"Failed to load memory: {e}")
            return {self.memory_key: []}
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """
        Save the context of a model run to memory.
        
        Args:
            inputs: The inputs to the model
            outputs: The outputs from the model
        """
        # This is a simplified implementation
        # In a real implementation, you would convert inputs/outputs to RDF
        # and store them in the RDF store
        
        # Create a simple graph with the input/output data
        graph = Graph()
        
        # Add some triples representing the context
        memory_uri = URIRef(f"{self.store.data_graph_uri}/memory/context_{id(inputs)}")
        
        for key, value in inputs.items():
            if isinstance(value, str):
                graph.add((memory_uri, URIRef(f"{self.store.base_url}/input/{key}"), Literal(value)))
                
        for key, value in outputs.items():
            if isinstance(value, str):
                graph.add((memory_uri, URIRef(f"{self.store.base_url}/output/{key}"), Literal(value)))
        
        # Store the graph
        if len(graph) > 0:
            self.store.update.insert_graph(graph, f"{self.store.data_graph_uri}/memory")
    
    def clear(self) -> None:
        """Clear all memory contents."""
        self.store.update.delete_graph(f"{self.store.data_graph_uri}/memory")


class SemanticRetriever(BaseRetriever):
    """
    Retriever that uses semantic queries to find relevant documents.
    
    This class extends LangChain's BaseRetriever to provide semantically-enhanced
    retrieval capabilities using RDF and SPARQL.
    """
    
    def __init__(self, store: FusekiStore):
        """
        Initialize the SemanticRetriever.
        
        Args:
            store: The FusekiStore instance for data retrieval
        """
        super().__init__()
        self.store = store
        
    def _get_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """
        Get documents relevant to the query.
        
        Args:
            query: The query string
            
        Returns:
            A list of relevant documents
        """
        # This is a simplified implementation
        # In a real implementation, you would use more sophisticated semantic matching
        
        # Convert the query to a SPARQL query
        # This is a very basic approach - in practice, you would use NLP techniques
        # to convert the natural language query to a semantic query
        
        keywords = query.lower().split()
        filter_clauses = []
        
        for keyword in keywords:
            filter_clauses.append(f'FILTER(CONTAINS(LCASE(STR(?text)), "{keyword}"))')
            
        filter_str = " || ".join(filter_clauses)
        
        sparql_query = f"""
        SELECT ?doc ?text ?title ?source
        WHERE {{
            GRAPH <{self.store.data_graph_uri}/documents> {{
                ?doc a <http://example.org/Document> ;
                     <http://example.org/text> ?text .
                OPTIONAL {{ ?doc <http://example.org/title> ?title }}
                OPTIONAL {{ ?doc <http://example.org/source> ?source }}
            }}
            {filter_str}
        }}
        LIMIT 5
        """
        
        try:
            results = self.store.query.execute_select(sparql_query)
            
            # Convert results to documents
            documents = []
            for result in results:
                doc = {
                    "id": str(result.get("doc", "")),
                    "text": str(result.get("text", "")),
                    "metadata": {
                        "title": str(result.get("title", "")) if "title" in result else "",
                        "source": str(result.get("source", "")) if "source" in result else ""
                    }
                }
                documents.append(doc)
                
            return documents
        except Exception as e:
            print(f"Failed to retrieve documents: {e}")
            return []


class SemanticModelRegistry:
    """
    Registry for Pydantic models with semantic capabilities.
    
    This class manages the registration and retrieval of Pydantic models,
    along with their corresponding SHACL shapes.
    """
    
    def __init__(self, store: FusekiStore, base_namespace: str = "http://example.org/"):
        """
        Initialize the SemanticModelRegistry.
        
        Args:
            store: The FusekiStore instance for shape storage
            base_namespace: The base URI namespace for generated shapes
        """
        self.store = store
        self.base_namespace = base_namespace
        self.shape_generator = ShapeGenerator(base_namespace)
        self.registered_models = {}
        
    def register_model(self, model_class: Type[BaseModel]) -> bool:
        """
        Register a Pydantic model and generate its SHACL shape.
        
        Args:
            model_class: The Pydantic model class to register
            
        Returns:
            True if registration was successful, False otherwise
        """
        model_name = model_class.__name__
        
        try:
            # Generate SHACL shape
            shape_graph = self.shape_generator.generate_shape(model_class)
            
            # Store the shape
            success = self.store.store_shape(shape_graph, model_name)
            
            if success:
                self.registered_models[model_name] = model_class
                return True
            else:
                return False
        except Exception as e:
            print(f"Failed to register model {model_name}: {e}")
            return False
    
    def get_model(self, model_name: str) -> Optional[Type[BaseModel]]:
        """
        Get a registered Pydantic model by name.
        
        Args:
            model_name: The name of the model to retrieve
            
        Returns:
            The Pydantic model class, or None if not found
        """
        return self.registered_models.get(model_name)
    
    def validate_instance(self, instance: BaseModel) -> Dict[str, Any]:
        """
        Validate a Pydantic model instance against its SHACL shape.
        
        Args:
            instance: The Pydantic model instance to validate
            
        Returns:
            A dictionary containing validation results
        """
        model_name = instance.__class__.__name__
        
        if model_name not in self.registered_models:
            return {"valid": False, "error": "Model not registered"}
        
        # Convert instance to RDF
        # This is a simplified implementation
        graph = Graph()
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
        
        # Validate against shape
        return self.store.validate_against_shape(graph, model_name)
