"""
RDF store interface for connecting to Fuseki and other RDF triple stores.

This module provides functionality for connecting to RDF stores,
executing SPARQL queries, and managing RDF data.
"""

from typing import Any, Dict, List, Optional, Union
import requests
from rdflib import Graph, URIRef, Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET


class StoreConnection:
    """
    Manages connections to RDF stores.
    
    This class provides methods for connecting to RDF triple stores,
    particularly Apache Jena Fuseki, and executing SPARQL operations.
    """
    
    def __init__(self, endpoint_url: str, update_endpoint: Optional[str] = None):
        """
        Initialize the StoreConnection.
        
        Args:
            endpoint_url: The URL of the SPARQL query endpoint
            update_endpoint: The URL of the SPARQL update endpoint (if different)
        """
        self.endpoint_url = endpoint_url
        self.update_endpoint = update_endpoint or endpoint_url
        self.query_wrapper = SPARQLWrapper(endpoint_url)
        self.query_wrapper.setReturnFormat(JSON)
        self.update_wrapper = SPARQLWrapper(self.update_endpoint)
        self.update_wrapper.setMethod(POST)
        
    def test_connection(self) -> bool:
        """
        Test the connection to the RDF store.
        
        Returns:
            True if the connection is successful, False otherwise
        """
        try:
            self.query_wrapper.setQuery("ASK { ?s ?p ?o }")
            self.query_wrapper.setReturnFormat(JSON)
            results = self.query_wrapper.query().convert()
            return results.get('boolean', False)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
            
    def close(self) -> None:
        """Close the connection to the RDF store."""
        # SPARQLWrapper doesn't maintain persistent connections,
        # so there's nothing to close
        pass


class QueryExecutor:
    """
    Executes SPARQL queries against RDF stores.
    
    This class provides methods for executing various types of SPARQL
    queries and processing the results.
    """
    
    def __init__(self, connection: StoreConnection):
        """
        Initialize the QueryExecutor.
        
        Args:
            connection: A StoreConnection instance
        """
        self.connection = connection
        
    def execute_select(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SPARQL SELECT query.
        
        Args:
            query: The SPARQL SELECT query string
            
        Returns:
            A list of dictionaries containing the query results
        """
        self.connection.query_wrapper.setQuery(query)
        self.connection.query_wrapper.setReturnFormat(JSON)
        results = self.connection.query_wrapper.query().convert()
        
        bindings = []
        for binding in results["results"]["bindings"]:
            result = {}
            for var, value in binding.items():
                result[var] = self._convert_binding_value(value)
            bindings.append(result)
            
        return bindings
    
    def execute_ask(self, query: str) -> bool:
        """
        Execute a SPARQL ASK query.
        
        Args:
            query: The SPARQL ASK query string
            
        Returns:
            The boolean result of the ASK query
        """
        self.connection.query_wrapper.setQuery(query)
        self.connection.query_wrapper.setReturnFormat(JSON)
        results = self.connection.query_wrapper.query().convert()
        return results.get("boolean", False)
    
    def execute_construct(self, query: str) -> Graph:
        """
        Execute a SPARQL CONSTRUCT query.
        
        Args:
            query: The SPARQL CONSTRUCT query string
            
        Returns:
            An RDFLib Graph containing the constructed triples
        """
        self.connection.query_wrapper.setQuery(query)
        graph = self.connection.query_wrapper.query().convert()
        return graph
    
    def _convert_binding_value(self, value: Dict[str, str]) -> Any:
        """
        Convert a SPARQL binding value to a Python object.
        
        Args:
            value: A dictionary containing the binding value
            
        Returns:
            The converted Python object
        """
        value_type = value.get("type")
        value_data = value.get("value")
        
        if value_type == "uri":
            return URIRef(value_data)
        elif value_type == "literal":
            datatype = value.get("datatype")
            lang = value.get("xml:lang")
            if datatype:
                return Literal(value_data, datatype=URIRef(datatype))
            elif lang:
                return Literal(value_data, lang=lang)
            else:
                return Literal(value_data)
        elif value_type == "bnode":
            return BNode(value_data)
        else:
            return value_data


class UpdateExecutor:
    """
    Executes SPARQL updates against RDF stores.
    
    This class provides methods for executing SPARQL UPDATE operations
    and managing transactions.
    """
    
    def __init__(self, connection: StoreConnection):
        """
        Initialize the UpdateExecutor.
        
        Args:
            connection: A StoreConnection instance
        """
        self.connection = connection
        
    def execute_update(self, update: str) -> bool:
        """
        Execute a SPARQL UPDATE operation.
        
        Args:
            update: The SPARQL UPDATE string
            
        Returns:
            True if the update was successful, False otherwise
        """
        try:
            self.connection.update_wrapper.setQuery(update)
            self.connection.update_wrapper.query()
            return True
        except Exception as e:
            print(f"Update failed: {e}")
            return False
    
    def insert_graph(self, graph: Graph, graph_uri: Optional[str] = None) -> bool:
        """
        Insert an RDFLib Graph into the store.
        
        Args:
            graph: The RDFLib Graph to insert
            graph_uri: Optional URI for the named graph
            
        Returns:
            True if the insertion was successful, False otherwise
        """
        turtle = graph.serialize(format="turtle")
        
        if graph_uri:
            update = f"INSERT DATA {{ GRAPH <{graph_uri}> {{ {turtle} }} }}"
        else:
            update = f"INSERT DATA {{ {turtle} }}"
            
        return self.execute_update(update)
    
    def delete_graph(self, graph_uri: str) -> bool:
        """
        Delete a named graph from the store.
        
        Args:
            graph_uri: The URI of the graph to delete
            
        Returns:
            True if the deletion was successful, False otherwise
        """
        update = f"DROP GRAPH <{graph_uri}>"
        return self.execute_update(update)


class FusekiStore:
    """
    High-level interface for working with Apache Jena Fuseki.
    
    This class provides a simplified interface for common operations
    with Fuseki, including storing and retrieving SHACL shapes.
    """
    
    def __init__(self, base_url: str, dataset: str):
        """
        Initialize the FusekiStore.
        
        Args:
            base_url: The base URL of the Fuseki server
            dataset: The name of the dataset to use
        """
        self.base_url = base_url
        self.dataset = dataset
        
        query_endpoint = f"{base_url}/{dataset}/query"
        update_endpoint = f"{base_url}/{dataset}/update"
        
        self.connection = StoreConnection(query_endpoint, update_endpoint)
        self.query = QueryExecutor(self.connection)
        self.update = UpdateExecutor(self.connection)
        
        # Define graph URIs for organizing data
        self.shapes_graph_uri = f"{base_url}/{dataset}/shapes"
        self.data_graph_uri = f"{base_url}/{dataset}/data"
        
    def store_shape(self, shape_graph: Graph, shape_name: str) -> bool:
        """
        Store a SHACL shape in the shapes graph.
        
        Args:
            shape_graph: The RDFLib Graph containing the SHACL shape
            shape_name: A name for the shape
            
        Returns:
            True if the shape was stored successfully, False otherwise
        """
        # Create a named graph URI for this specific shape
        shape_uri = f"{self.shapes_graph_uri}/{shape_name}"
        
        # Store the shape in the named graph
        return self.update.insert_graph(shape_graph, shape_uri)
    
    def get_shape(self, shape_name: str) -> Optional[Graph]:
        """
        Retrieve a SHACL shape from the shapes graph.
        
        Args:
            shape_name: The name of the shape to retrieve
            
        Returns:
            An RDFLib Graph containing the shape, or None if not found
        """
        shape_uri = f"{self.shapes_graph_uri}/{shape_name}"
        
        query = f"""
        CONSTRUCT {{ ?s ?p ?o }}
        WHERE {{
            GRAPH <{shape_uri}> {{
                ?s ?p ?o
            }}
        }}
        """
        
        try:
            return self.query.execute_construct(query)
        except Exception as e:
            print(f"Failed to retrieve shape: {e}")
            return None
    
    def store_instance_data(self, data_graph: Graph, model_name: str) -> bool:
        """
        Store instance data in the data graph.
        
        Args:
            data_graph: The RDFLib Graph containing the instance data
            model_name: The name of the model the data conforms to
            
        Returns:
            True if the data was stored successfully, False otherwise
        """
        # Create a named graph URI for this type of data
        data_uri = f"{self.data_graph_uri}/{model_name}"
        
        # Store the data in the named graph
        return self.update.insert_graph(data_graph, data_uri)
    
    def validate_against_shape(self, data_graph: Graph, shape_name: str) -> Dict[str, Any]:
        """
        Validate data against a SHACL shape.
        
        Args:
            data_graph: The RDFLib Graph containing the data to validate
            shape_name: The name of the shape to validate against
            
        Returns:
            A dictionary containing the validation results
        """
        # This is a simplified implementation that assumes Fuseki has SHACL validation
        # In practice, you might need to use a separate SHACL validation library
        
        shape_graph = self.get_shape(shape_name)
        if not shape_graph:
            return {"valid": False, "error": "Shape not found"}
        
        # In a real implementation, you would use a SHACL validation library here
        # For now, we'll just return a placeholder result
        return {
            "valid": True,
            "conforms": True,
            "results": []
        }
