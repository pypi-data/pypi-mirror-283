""" Unit test tra """

import sys
import os
import configparser
import pytest

from ....opengate_client import OpenGateClient
from ....provision.processor.provision_processor import ProvisionProcessorBuilder


@pytest.fixture
def client():
    """ Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="url", api_key="api_key")


class TestProvisionProcessor:
    """Unit tests for the Provision Processor functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = ProvisionProcessorBuilder(client)

    def test_with_organization_name(self):
        organization = "organization_name"
        self.builder.with_organization_name(organization)
        assert self.builder.organization_name == organization

    def test_with_identifier(self):
        self.builder.with_identifier('identifier')
        assert self.builder.provision_processor_id == 'identifier'

    def test_with_name(self):
        self.builder.with_name('name')
        assert self.builder.provision_processor_name == 'name'

    def test_with_bulk_file(self):
        bulk_file_path = os.path.join(os.path.dirname(__file__), 'demotest.xlsx')
        self.builder.with_bulk_file(bulk_file_path)

    def test_with_bulk_process_identitifer(self):
        self.builder.with_bulk_process_identitifer('process_identifier')
        assert self.builder.bulk_process_id == 'process_identifier'

    def test_bulk(self):
        bulk_file_path = os.path.join(os.path.dirname(__file__), 'demotest.xlsx')
        self.builder.with_organization_name('organization_name').with_identifier('identifier').with_bulk_file(
            bulk_file_path).bulk()
        url = 'url/north/v80/provisionProcessors/provision/organizations/organization_name/identifier/bulk'
        assert self.builder.url == url and self.builder.method == 'bulk_provision_processor'

    def test_find_by_name(self):
        self.builder.with_organization_name('organization_name').with_name(
            'provision_processor_name').find_by_name().build()
        url = 'url/north/v80/provisionProcessors/provision/organizations/organization_name'
        assert self.builder.url == url and self.builder.method == 'find_by_name'

    def test_bulk_status(self):
        self.builder.with_organization_name('organization_name').with_bulk_process_identitifer(
            'bulk_process_id').bulk_status().build()
        url = 'url/north/v80/provisionProcessors/provision/organizations/organization_name/bulk/bulk_process_id'
        assert self.builder.url == url and self.builder.method == 'bulk_status'

    def test_bulk_details(self):
        self.builder.with_organization_name('organization_name').with_bulk_process_identitifer(
            'bulk_process_id').bulk_details()
        url = 'url/north/v80/provisionProcessors/provision/organizations/organization_name/bulk/bulk_process_id/details'
        assert self.builder.url == url and self.builder.method == 'bulk_details'

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