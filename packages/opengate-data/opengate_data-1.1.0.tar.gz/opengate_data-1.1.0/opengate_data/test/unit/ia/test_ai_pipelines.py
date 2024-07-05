""" Unit test pipelines """

import sys
import os
import configparser
import pytest
import unittest

from ....opengate_client import OpenGateClient
from ....ai_pipelines.ai_pipelines import AIPipelinesBuilder


@pytest.fixture
def client():
    """ Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="url", api_key="api_key")


class TestAIPipelines(unittest.TestCase):
    """Unit tests for the AI Pipelines functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = AIPipelinesBuilder(client)

    def test_with_organization(self):
        self.builder.with_organization_name('test_org')
        assert self.builder.organization_name == 'test_org'

    def test_with_identifier(self):
        self.builder.with_identifier('identifier')
        assert self.builder.identifier == 'identifier'

    def test_with_config_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), 'config_test.ini')
        self.builder.with_config_file(config_file_path, 'id', 'pipeline_id')
        self.assertEqual(self.builder.config_file, config_file_path)
        self.assertEqual(self.builder.identifier, 'c911a30d-f7bb-4a81-8090-30dc7ad097bb')

    def test_with_find_name(self):
        self.builder.with_find_by_name('name_pipeline')
        assert self.builder.find_name == 'name_pipeline'

    def test_with_prediction(self):
        prediction = {'X': [{'input_8': [[5002]]}]}
        self.builder.with_prediction(prediction)
        assert self.builder.data_prediction == prediction

    def test_with_find_by_name(self):
        self.builder.with_find_by_name('file_name')
        assert self.builder.find_name == 'file_name'

    def test_with_name(self):
        self.builder.with_name('name_pipeline')
        assert self.builder.name == 'name_pipeline'

    def test_add_action_transfomer_with_type(self):
        self.builder.add_action('exittransformer.py', 'TRANSFORMER')
        assert self.builder.actions == [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'}]

    def test_add_action_transfomer_without_type(self):
        self.builder.add_action('exittransformer.py', 'TRANSFORMER')
        assert self.builder.actions == [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'}]

    def test_add_action_model_with_type(self):
        self.builder.add_action('snow_create.onnx', 'MODEL')
        assert self.builder.actions == [{'name': 'snow_create.onnx', 'type': 'MODEL'}]

    def test_add_action_model_without_type(self):
        self.builder.add_action('snow_create.onnx', 'MODEL')
        assert self.builder.actions == [{'name': 'snow_create.onnx', 'type': 'MODEL'}]

    def test_add_action_transfomers_and_models(self):
        self.builder.add_action('exittransformer.py', 'TRANSFORMER')
        self.builder.add_action('snow_create.onnx', 'MODEL')
        self.builder.add_action('inittransformer.py', 'TRANSFORMER')
        self.builder.add_action('snow_update.onnx', 'MODEL')
        assert self.builder.actions == [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'},
                                        {'name': 'snow_create.onnx', 'type': 'MODEL'},
                                        {'name': 'inittransformer.py', 'type': 'TRANSFORMER'},
                                        {'name': 'snow_update.onnx', 'type': 'MODEL'}]

    def test_create(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_name('create_pipeline')
        self.builder.add_action('exittransformer.py', 'TRANSFORMER')
        self.builder.create()
        self.builder.build()
        url = 'url/north/ai/organization_name/pipelines'
        assert self.builder.url == url and self.builder.method == 'create'

    def test_find_all_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.find_all()
        url = 'url/north/ai/organization_name/pipelines'
        self.builder.build()
        assert self.builder.url == url and self.builder.method == 'find'

    def test_find_one_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.find_one()
        url = f'url/north/ai/organization_name/pipelines/{self.builder.identifier}'
        self.builder.build()
        assert self.builder.url == url and self.builder.method == 'find'

    def test_update_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.update()
        self.builder.build()
        url = f'url/north/ai/organization_name/pipelines/{self.builder.identifier}'
        assert self.builder.url == url and self.builder.method == 'update'

    def test_delete_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.delete()
        self.builder.build()
        url = f'url/north/ai/organization_name/pipelines/{self.builder.identifier}'
        assert self.builder.url == url and self.builder.method == 'delete'

    def test_prediction_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.with_prediction({'X': [{'input_8': [[5002]]}]})
        self.builder.prediction()
        self.builder.build()
        url = f'url/north/ai/organization_name/pipelines/{self.builder.identifier}/prediction'
        assert self.builder.url == url and self.builder.method == 'prediction'

    def test_save(self):
        self.builder.with_organization_name("organization_name")
        self.builder.save()
        self.builder.build()
        assert self.builder.method == 'save'

    def test_set_config_file_identifier(self):
        self.builder.with_identifier('identifier')
        config_file_path = os.path.join(os.path.dirname(__file__), 'config_test.ini')
        self.builder.with_config_file(config_file_path, 'id', 'pipeline_id')
        self.builder.set_config_file_identifier()
        self.builder.build()
        assert self.builder.method == 'set_config_identifier'

    def test_build_with_build_execute(self):
        self.builder.method_calls = ['build_execute']
        with pytest.raises(Exception):
            self.builder.build()
        assert "You cannot use build() together with build_execute()"

    def test_build_execute_without_build(self):
        self.builder.method_calls = []
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_build_execute_with_build(self):
        self.builder.method_calls = ['build', 'build_execute']
        self.builder.builder = True
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_execute_with_incorrect_order(self):
        self.builder.method_calls = ['build', 'with_device_identifier', 'execute']
        with pytest.raises(Exception):
            self.builder.execute()