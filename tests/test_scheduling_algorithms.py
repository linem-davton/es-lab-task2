from fastapi import applications
import pytest
import os
import json
import jsonschema
import sys

# Adjust path to include the 'src' directory for importing algorithms
script_dir = os.path.dirname(__file__)
input_models_dir = os.path.join(script_dir, "input_models")

sys.path.append(os.path.abspath(os.path.join(script_dir, "..", "src")))
from algorithms import ldf_single_node, edf_single_node, edf_multinode, ll_multinode, ldf_multinode, ldf_single_node

output_schema_file = os.path.join(script_dir, "..","src","output_schema.json")

with open(output_schema_file) as f:
    output_schema = json.load(f)

input_files = os.listdir(input_models_dir)


# List of algorithms to test
algorithms = [ldf_single_node, edf_single_node, edf_multinode, ldf_multinode, ll_multinode]

# Creating a product of filenames and algorithms for detailed parameterization
test_cases = [(input_file, algo) for input_file in input_files for algo in algorithms]

# Utility function to load models and run scheduling algorithm
def load_and_schedule(filename, algo):
    model_path = os.path.join(input_models_dir, filename)
    with open(model_path) as f:
        model_data = json.load(f)

    application_model = model_data["application"]
    platform_model = model_data["platform"]
   
    if algo in [ldf_single_node, edf_single_node]:
        result = algo(application_model)
    
    elif algo in [edf_multinode, ldf_multinode, ll_multinode]:
        result = algo(application_model, platform_model)
 
    return result, application_model


@pytest.mark.parametrize("filename,algorithm", test_cases)
def test_output_schema(filename, algorithm):
    """Test that the generated schedule adheres to the schema """

    result, application_model = load_and_schedule(filename, algorithm)
    try:
        jsonschema.validate(instance=result, schema=output_schema)
        assert True
    except jsonschema.exceptions.ValidationError as err:
        assert False, f'Output does not match the output schema for {result["name"]}'
        

@pytest.mark.parametrize("filename, algorithm", test_cases)
def test_task_duration(filename, algorithm):
    """Test that each task completes within its estimated duration."""
    result, app_model = load_and_schedule(filename, algorithm)
    for task in result["schedule"]:
        start_time = task["start_time"]
        end_time = task["end_time"]
        task_id = task["task_id"]
        wcet = next(
            (t["wcet"] for t in app_model["tasks"] if t["id"] == task_id), None
        )
        assert end_time == start_time + wcet, f'Incorrect task duration calculation in {result["name"]}'


@pytest.mark.parametrize("filename, algorithm", test_cases)
def test_task_deadline(filename,algorithm):
    """Test that each task respects its deadline."""
    result, app_model = load_and_schedule(filename, algorithm)
    for task in result["schedule"]:
        end_time = task["end_time"]
        task_id = task["task_id"]
        deadline = next(
            (t["deadline"] for t in app_model["tasks"] if t["id"] == task_id), None
        )
        assert end_time <= deadline, f'Task exceeds deadline in {result["name"]}'


@pytest.mark.parametrize("filename, algorithm", test_cases)
def test_task_dependencies(filename, algorithm):
    """Test that each task respects the completion times of its predecessors."""
    result, app_model = load_and_schedule(filename, algorithm)
    for task in result["schedule"]:
        start_time = task["start_time"]
        task_id = task["task_id"]
        predecessors = [
            msg["sender"]
            for msg in app_model["messages"]
            if msg["receiver"] == task_id
            ]
        
        predecessors_end_times = [
            t["end_time"]
            for t in result["schedule"]
            if t["task_id"] in predecessors
            ]
        
        assert start_time >= max(
                predecessors_end_times, default=0
        ), f'Task starts before predecessor ends in {result["name"]}'
