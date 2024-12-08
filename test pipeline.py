import pytest
import os

def test_model_file_exists():
    assert os.path.exists("trained_model.pkl"), "Trained model file is missing!"

def test_raw_data_exists():
    assert os.path.exists("raw_data.csv"), "Raw data file is missing!"

def test_pipeline_steps():
    # Example: Check if DVC pipeline steps are defined
    assert os.path.exists("dvc.yaml"), "DVC pipeline is not set up!"

if __name__ == "__main__":
    pytest.main()
