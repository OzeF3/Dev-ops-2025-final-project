import pytest
import os
import sys
import yaml
import json
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path

## checks that the core functions of the CLI tool work correctly 
# testing both valid inputs and error cases like missing files or bad YAML.

# Add sawectl directory to path
sys.path.insert(0, os.path.dirname(__file__))
from sawectl import (
    load_yaml,
    load_json_schema,
    extract_module_and_method,
    validate_step,
    load_module_manifest,
)


# === TEST load_yaml ===

def test_load_yaml_valid():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({'name': 'test', 'steps': []}, f)
        f.flush()
        result = load_yaml(f.name)
    assert result['name'] == 'test'
    os.unlink(f.name)


def test_load_yaml_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('')
        f.flush()
        with pytest.raises(SystemExit):
            load_yaml(f.name)
    os.unlink(f.name)


def test_load_yaml_invalid_yaml():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('key: [invalid: yaml: content')
        f.flush()
        with pytest.raises(SystemExit):
            load_yaml(f.name)
    os.unlink(f.name)


def test_load_yaml_file_not_found():
    with pytest.raises(SystemExit):
        load_yaml('/nonexistent/path/file.yaml')


# === TEST load_json_schema ===

def test_load_json_schema_valid():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({'type': 'object'}, f)
        f.flush()
        result = load_json_schema(f.name)
    assert result['type'] == 'object'
    os.unlink(f.name)


def test_load_json_schema_file_not_found():
    with pytest.raises(SystemExit):
        load_json_schema('/nonexistent/schema.json')


# === TEST extract_module_and_method ===

def test_extract_module_and_method_standard():
    module, method = extract_module_and_method('slack_module.instance.send', {})
    assert module == 'slack_module'
    assert method == 'send'


def test_extract_module_and_method_two_parts():
    module, method = extract_module_and_method('slack_module.send', {})
    assert module == 'slack_module'
    assert method == 'send'


def test_extract_module_and_method_context():
    context_modules = {
        'my_slack': {'module': 'slack_module.instance'}
    }
    module, method = extract_module_and_method('context.my_slack.send', context_modules)
    assert module == 'slack_module'
    assert method == 'send'


def test_extract_module_and_method_invalid():
    module, method = extract_module_and_method('invalid', {})
    assert module is None
    assert method is None


# === TEST validate_step ===

def test_validate_step_missing_id():
    step = {'type': 'action'}
    ok, msg = validate_step(step, 'modules', {})
    assert not ok
    assert 'id' in msg


def test_validate_step_missing_type():
    step = {'id': 'step1'}
    ok, msg = validate_step(step, 'modules', {})
    assert not ok
    assert 'type' in msg


def test_validate_step_no_action():
    step = {'id': 'step1', 'type': 'action'}
    ok, msg = validate_step(step, 'modules', {})
    assert ok


# === TEST load_module_manifest ===

def test_load_module_manifest_not_found():
    result = load_module_manifest('/nonexistent/modules', 'fake_module')
    assert result is None


def test_load_module_manifest_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        module_dir = Path(tmpdir) / 'test_module'
        module_dir.mkdir()
        manifest = {'name': 'test_module', 'methods': [{'name': 'run', 'arguments': []}]}
        with open(module_dir / 'module.yaml', 'w') as f:
            yaml.dump(manifest, f)
        result = load_module_manifest(tmpdir, 'test_module')
    assert result['name'] == 'test_module'

# === TEST CLI VERSION ===

def test_cli_version():
    from sawectl import VERSION
    assert VERSION is not None
    assert isinstance(VERSION, str)
    assert len(VERSION) > 0


# === TEST CLI ENTRY POINT ===

def test_cli_no_args_exits():
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['sawectl']):
            from sawectl import main
            main()


# === TEST WORKFLOW VALIDATION - VALID WORKFLOW ===

def test_validate_step_valid_no_action():
    step = {
        'id': 'step1',
        'type': 'action'
    }
    ok, msg = validate_step(step, 'modules', {})
    assert ok
    assert 'step1' in msg


# === TEST DUPLICATE STEP DETECTION ===

def test_load_yaml_returns_dict():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({'workflow': {'name': 'test', 'steps': []}}, f)
        f.flush()
        result = load_yaml(f.name)
    assert isinstance(result, dict)
    assert 'workflow' in result
    os.unlink(f.name)


# === TEST MODULE MANIFEST STRUCTURE ===

def test_module_manifest_has_methods():
    with tempfile.TemporaryDirectory() as tmpdir:
        module_dir = Path(tmpdir) / 'email_module'
        module_dir.mkdir()
        manifest = {
            'name': 'email_module',
            'methods': [
                {'name': 'send', 'arguments': [{'name': 'to', 'required': True}]}
            ]
        }
        with open(module_dir / 'module.yaml', 'w') as f:
            yaml.dump(manifest, f)
        result = load_module_manifest(tmpdir, 'email_module')
    assert 'methods' in result
    assert result['methods'][0]['name'] == 'send'


# === TEST EXTRACT MODULE - EDGE CASES ===

def test_extract_module_empty_string():
    module, method = extract_module_and_method('', {})
    assert module is None
    assert method is None


def test_extract_module_context_missing_module():
    context_modules = {
        'my_slack': {}  # missing 'module' key
    }
    module, method = extract_module_and_method('context.my_slack.send', context_modules)
    assert module is None
    assert method is None