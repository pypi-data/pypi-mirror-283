"""
Crylearn Package

This package provides tools for processing crystal structure data and converting them into graph representations.
"""
import pkg_resources
import importlib.util
import sys
import os

# Get the path of the compiled module
compiled_module_path = os.path.join(
    pkg_resources.get_distribution('Crylearn').location,
    'Crylearn/__pycache__/cry2graph.cpython-39.pyc'
)

# Load the module
spec = importlib.util.spec_from_file_location("Crylearn.cry2graph", compiled_module_path)
cry2graph = importlib.util.module_from_spec(spec)
sys.modules["Crylearn.cry2graph"] = cry2graph
spec.loader.exec_module(cry2graph)
