from dagster import asset
import os

@asset
def deploy_cubejs_models():
    """
    Deploy Cube.js models for semantic layer.
    """
    models_path = os.getenv("CUBEJS_MODELS_PATH", "./cubes/models")
    print(f"Deploying Cube.js models from {models_path}")
