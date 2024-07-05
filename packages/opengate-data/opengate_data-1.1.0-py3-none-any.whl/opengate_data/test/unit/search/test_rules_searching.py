import pytest
from ....searching.builder.rules_search import RulesSearchBuilder
from ....opengate_client import OpenGateClient
from ....searching.filter import FilterBuilder
from ....searching.select import SelectBuilder


@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestRulesSearching:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = RulesSearchBuilder(client)
        self.filter_builder = FilterBuilder()
        self.select_builder = SelectBuilder()

    def test_with_filter(self):
        filter_builder_build = self.filter_builder.and_(
            self.filter_builder.eq("provision.administration.organization", "organization"),
        ).build()
        filt = {'and': [{'eq': {'provision.administration.organization': 'organization'}}]}
        self.builder.with_filter(filter_builder_build)
        assert self.builder.body_data["filter"] == filt
        assert filter_builder_build == filt

    def test_with_select(self):
        select_builder_build = self.select_builder.add("provision.device.identifier", ["value"]).add("volTot",
                                                                                                ["value"]).build()
        self.builder.with_select(select_builder_build)
        assert self.builder.body_data['select'] == select_builder_build
        select = [{'name': 'provision.device.identifier', 'fields': [{'field': 'value'}]}, {'name': 'volTot', 'fields': [{'field': 'value'}]}]
        assert select_builder_build == select
        assert self.builder.body_data["select"] == select

    def test_with_limit(self):
        self.builder.with_limit(1000, 2)
        assert self.builder.body_data["limit"] == {'size': 1000, 'start': 2}

    def test_add_by_group(self):
        self.builder.add_by_group("provision.device.model")
        assert self.builder.body_data["group"] == {'parameters': [{'name': 'provision.device.model'}]}

    def test_add_sort_by(self):
        self.builder.add_sort_by("datapoints._current.at", "DESCENDING")
        assert self.builder.body_data["sort"] == {'parameters': [{'name': 'datapoints._current.at', 'type': 'DESCENDING'}]}

    def test_with_format_dict_pandas(self):
        self.builder.with_format("dict")
        assert self.builder.format_data == "dict"
        self.builder.with_format("pandas")
        assert self.builder.format_data == "pandas"

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
