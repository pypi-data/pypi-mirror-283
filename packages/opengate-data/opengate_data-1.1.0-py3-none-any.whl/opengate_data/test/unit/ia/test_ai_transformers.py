''' Unit test tra '''

import sys
import os
import configparser
import pytest
import unittest

from ....opengate_client import OpenGateClient
from ....ai_transformers.ai_transformers import AITransformersBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]
non_type_list = [111, 1.0, True, {"key": "value"}, "str"]


@pytest.fixture
def client():
    """ Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="url", api_key="api_key")


class TestAITransfomers(unittest.TestCase):
    """Unit tests for the AI Pipelines functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = AITransformersBuilder(client)

    def test_with_organization_name(self):
        organization = "organization_name"
        self.builder.with_organization_name(organization)
        assert self.builder.organization_name == organization

    def test_with_identifier(self):
        self.builder.with_identifier('identifier')
        assert self.builder.identifier == 'identifier'

    def test_with_config_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), 'config_test.ini')
        self.builder.with_config_file(config_file_path, 'id', 'transformer_id')
        self.assertEqual(self.builder.config_file, config_file_path)
        self.assertEqual(self.builder.identifier, '23c15db1-3383-4afe-8780-fae37b88d2f6')

    def test_add_file_plk_with_type(self):
        self.builder.add_file('/opengate-data-py/test/utils/pkl_encoder.pkl', 'application/octet-stream')
        assert self.builder.files == [('/opengate-data-py/test/utils/pkl_encoder.pkl', 'application/octet-stream')]

    def test_add_file_plk_without_type(self):
        self.builder.add_file('/opengate-data-py/test/utils/pkl_encoder.pkl')
        assert self.builder.files == [('/opengate-data-py/test/utils/pkl_encoder.pkl', 'application/octet-stream')]

    def test_add_file_python_with_type(self):
        self.builder.add_file('/opengate-data-py/test/utils/inittransformer.py')
        assert self.builder.files == [('/opengate-data-py/test/utils/inittransformer.py', 'text/python')]

    def test_add_file_python_without_type(self):
        self.builder.add_file('/opengate-data-py/test/utils/inittransformer.py')
        assert self.builder.files == [('/opengate-data-py/test/utils/inittransformer.py', 'text/python')]

    def test_with_find_name(self):
        self.builder.with_find_by_name('name_transform')
        assert self.builder.find_name == 'name_transform'

    def test_with_evaluate(self):
        data_evaluate = {"data": {"PPLast12H": 0, }, "date": "2022-06-13T13:59:34.779+02:00"}
        self.builder.with_evaluate(data_evaluate)
        assert self.builder.data_evaluate == data_evaluate

    def test_with_output_file_path(self):
        self.builder.with_output_file_path('opengate-data-py/test/unit/ia/test_ai_transformers.py')
        assert self.builder.output_file_path == 'opengate-data-py/test/unit/ia/test_ai_transformers.py'

    def test_with_file_name(self):
        self.builder.with_file_name('file_name')
        assert self.builder.file_name == 'file_name'

    def test_create(self):
        self.builder.with_organization_name('organization_name')
        self.builder.add_file('create_transformer')
        self.builder.create()
        self.builder.build()
        url = 'url/north/ai/organization_name/transformers'
        assert self.builder.url == url and self.builder.method == 'create'

    def test_find_all_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.find_all()
        url = 'url/north/ai/organization_name/transformers'
        self.builder.build()
        assert self.builder.url == url and self.builder.method == 'find'

    def test_find_one_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.find_one()
        url = f'url/north/ai/organization_name/transformers/{self.builder.identifier}'
        self.builder.build()
        assert self.builder.url == url and self.builder.method == 'find'

    def test_update_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.add_file('create_transformer')
        self.builder.update()
        self.builder.build()
        url = f'url/north/ai/organization_name/transformers/{self.builder.identifier}'
        assert self.builder.url == url and self.builder.method == 'update'

    def test_delete(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.delete()
        url = f'url/north/ai/organization_name/transformers/{self.builder.identifier}'
        self.builder.build()
        assert self.builder.url == url and self.builder.method == 'delete'

    def test_download_url(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.add_file('create_transformer')
        self.builder.with_output_file_path('output_file')
        self.builder.with_file_name('file_name')
        self.builder.download()
        self.builder.build()
        url = f'url/north/ai/organization_name/transformers/{self.builder.identifier}/{self.builder.file_name}'
        assert self.builder.url == url and self.builder.method == 'download'

    def test_evaluate_url(self):
        data_evaluate = {"data": {"PPLast12H": 0, }, "date": "2022-06-13T13:59:34.779+02:00"}
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier('identifier')
        self.builder.with_evaluate(data_evaluate)
        self.builder.evaluate()
        self.builder.build()
        url = f'url/north/ai/organization_name/transformers/{self.builder.identifier}/transform'
        assert self.builder.url == url and self.builder.method == 'evaluate'

    def test_save(self):
        self.builder.with_organization_name("organization_name")
        self.builder.save()
        self.builder.build()
        assert self.builder.method == 'save'

    def test_set_config_file_identifier(self):
        self.builder.with_identifier('identifier')
        config_file_path = os.path.join(os.path.dirname(__file__), 'config_test.ini')
        self.builder.with_config_file(config_file_path, 'id', 'transformer_id')
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