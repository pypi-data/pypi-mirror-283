from isaac_analyzer.yaml_loader import load_yaml_resource


def test_load_yaml():
    data = load_yaml_resource("items.yaml")
    assert isinstance(data, dict)
    assert "items" in data  # Replace with actual checks based on your YAML structure
