#!/bin/bash
# Script to initialize Fuseki with a dataset for LangGraphSemantic

# Wait for Fuseki to be available
echo "Waiting for Fuseki to start..."
until curl -s http://fuseki:3030/ > /dev/null; do
  sleep 1
done

# Create the dataset
echo "Creating dataset..."
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "dbName=langgraphsemantic&dbType=tdb" \
     http://fuseki:3030/$/datasets

echo "Fuseki initialization complete."
