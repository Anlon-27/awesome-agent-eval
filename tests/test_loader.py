from agent_eval.loader import DatasetLoader

def test_dataset_loader():
    cases = DatasetLoader.load_from_file('datasets/tool_test_cases.json')
    assert len(cases) == 2
    assert cases[0].task_id == 'TC-TOOL-001'
    assert cases[0].layer == 'L1'
    assert cases[0].ground_truth.expected_tools[0].name == 'get_weather'