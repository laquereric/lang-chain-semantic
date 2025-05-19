from setuptools import setup, find_packages

setup(
    name="langgraphsemantic",
    version="0.1.0",
    description="A library for connecting Pydantic models to SHACL shapes in RDF stores",
    author="LangGraphSemantic Team",
    author_email="example@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rdflib>=6.0.0",
        "SPARQLWrapper>=2.0.0",
        "pydantic>=1.8.0",
        "langchain>=0.0.267",
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
