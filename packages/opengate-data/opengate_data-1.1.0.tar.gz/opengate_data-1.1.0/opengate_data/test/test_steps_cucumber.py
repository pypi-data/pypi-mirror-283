""" Steps for the features """
import sys
import os
import configparser
import pytest
from pytest_bdd import scenarios, given, when, then, parsers, step
from behave import step
import ast
import time
import re
import pandas as pd
from io import StringIO
import json
import re
from .ownworld import testing_data
from opengate_data.searching.filter import FilterBuilder
from opengate_data.searching.select import SelectBuilder
from opengate_data.searching.builder.entities_search import EntitiesSearchBuilder
from opengate_data.searching.builder.operations_search import OperationsSearchBuilder
from opengate_data.searching.builder.datapoints_search import DataPointsSearchBuilder
from opengate_data.searching.builder.datasets_search import DatasetsSearchBuilder
from opengate_data.searching.builder.timeseries_search import TimeseriesSearchBuilder
from opengate_data.searching.builder.rules_search import RulesSearchBuilder
from opengate_data.ai_models.ai_models import AIModelsBuilder
from opengate_data.ai_pipelines.ai_pipelines import AIPipelinesBuilder
from opengate_data.ai_transformers.ai_transformers import AITransformersBuilder
from opengate_data.rules.rules import RulesBuilder
from opengate_data.collection.iot_collection import IotCollectionBuilder
from opengate_data.collection.iot_bulk_collection import IotBulkCollectionBuilder
from opengate_data.provision.bulk.provision_bulk import ProvisionBulkBuilder
from opengate_data.provision.processor.provision_processor import ProvisionProcessorBuilder
from opengate_data.opengate_client import OpenGateClient

scenarios('collection/iot_collection.feature')
scenarios('collection/iot_bulk_collection.feature')
scenarios('ia/model.feature')
scenarios('ia/transformers.feature')
scenarios('ia/pipelines.feature')
scenarios('rules/rules.feature')
scenarios('provision/bulk/provision_bulk.feature')
scenarios('searching/searching_entities.feature')
scenarios('searching/searching_rules.feature')
scenarios('searching/searching_datasets.feature')
scenarios('timeseries/timeseries.feature')
scenarios('datapoints/datapoints.feature')
scenarios('provision/processor/provision_processor.feature')


current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, '..')
sys.path.append(project_dir)

config = configparser.ConfigParser()
config_file_path = os.path.join(current_dir, 'config_test.ini')
config.read(config_file_path)

builder_instance = None

# ! Important: Do not upload API keys or URLs; make sure they are set to None before uploading.
url = 'url'
api_key = 'api-key'
user = None
password = None


@pytest.fixture
def client():
    return OpenGateClient(url=url, api_key=api_key, user=user, password=password)


@pytest.fixture
@given(parsers.parse('I want to build a "{build_type}"'))
def ai_builder(client, build_type):
    global builder_instance
    if build_type == 'model':
        builder_instance = AIModelsBuilder(client)
    elif build_type == 'transformer':
        builder_instance = AITransformersBuilder(client)
    elif build_type == 'pipeline':
        builder_instance = AIPipelinesBuilder(client)
    elif build_type == 'rule':
        builder_instance = RulesBuilder(client)
    elif build_type == 'entity':
        builder_instance = EntitiesSearchBuilder(client)
    elif build_type == 'dataset':
        builder_instance = DatasetsSearchBuilder(client)
    elif build_type == 'timeserie':
        builder_instance = TimeseriesSearchBuilder(client)
    elif build_type == 'datapoint':
        builder_instance = DataPointsSearchBuilder(client)
    elif build_type == 'iot collection':
        builder_instance = IotCollectionBuilder(client)
    elif build_type == 'iot bulk collection':
        builder_instance = IotBulkCollectionBuilder(client)
    elif build_type == 'provision bulk':
        builder_instance = ProvisionBulkBuilder(client)
    elif build_type == 'searching rules':
        builder_instance = RulesSearchBuilder(client)
    else:
        raise ValueError(f'Invalid builder type: {build_type}')
    return builder_instance


@given(parsers.parse('I want to use an artificial intelligence file "{file}"'))
def step_file(file):
    builder_instance.add_file(file)


@given(parsers.parse('I want to save id in a configuration file "{config_file}" "{section}" "{config_key}"'))
def step_set_id_config_file(config_file, section, config_key):
    builder_instance.with_config_file(config_file, section, config_key)
    time.sleep(2)


@given(parsers.parse('I want to search id in a configuration file "{config_file}" "{section}" "{config_key}"'))
def step_search_id_config_file(config_file, section, config_key):
    builder_instance.with_config_file(config_file, section, config_key)
    time.sleep(2)


@given(parsers.parse('I want to search by name "{name}"'))
def step_search_by_name(name):
    """ search by name """
    builder_instance.with_find_by_name(name)


@given(parsers.parse('I want to download with name "{name}"'))
def step_save_outuput_file(name):
    """ Save outuput file """
    builder_instance.with_output_file_path(name)


@when(parsers.parse('I want to remove with name "{name}"'))
def step_remove_outuput_file(name):
    """ Remove outuput file """
    current_file = os.path.abspath(name)
    os.remove(current_file)


@given(parsers.parse('I want to use a prediction "{prediction}"'))
def step_prediction_code(prediction):
    """ Prediction """
    predic = ast.literal_eval(prediction)
    builder_instance.with_prediction(predic)


@given(parsers.parse('I want to use a evaluate transformer "{prediction}"'))
def step_evaluate_code(prediction):
    """ Evaluate """
    predic = ast.literal_eval(prediction)
    builder_instance.with_evaluate(predic)


@given(parsers.parse('I want to use a file name download transform "{file_name}"'))
def step_file_name(file_name):
    """ file name download transform """
    builder_instance.with_file_name(file_name)


@given(parsers.parse(
    'Set identifier in configuration file with section "{section}" and key {key} and {value} with identifier "{identifier}"'))
def step_identifier_config(section, key, identifier):
    """ Step set identifier """
    config.set(section, key, identifier)


@given(parsers.parse('I want to use organization "{organization}"'))
def step_organization(organization):
    """ organization """
    builder_instance.with_organization_name(get_value_from_path(testing_data, organization))


@given(parsers.parse('I want to use a identifier "{identifier}"'))
def step_identifier(identifier):
    builder_instance.with_identifier(get_value_from_path(testing_data, identifier))


@given(parsers.parse('I want add action "{add_action}"'))
def step_add_action(add_action):
    builder_instance.add_action(add_action)


@given(parsers.parse('I want to use a name "{name}"'))
def step_with_name(name):
    """ with name """
    builder_instance.with_name(name)


@given(parsers.parse('I want to use a filter "{filter_data}"'))
def step_with_body(filter_data):
    """ filter """
    builder_instance.with_body(ast.literal_eval(filter_data))


@given(parsers.parse('I want to use a channel "{channel}"'))
def step_with_channel(channel):
    """ channel """
    builder_instance.with_channel(get_value_from_path(testing_data, channel))


@given('I want to use a active rule as False')
def step_rule_activate_false():
    builder_instance.with_active(False)


@given(parsers.parse('I want to use a mode "{mode}"'))
def step_with_mode(mode):
    """ mode """
    builder_instance.with_mode(get_value_from_path(testing_data, mode))


@given(parsers.parse('I want to use a type "{type_data}"'))
def step_with_type(type_data):
    """ type """
    builder_instance.with_type(ast.literal_eval(type_data))


@given(parsers.parse('I want to use a condition "{condition}"'))
def step_with_condition(condition):
    """ actions delay """
    builder_instance.with_condition(ast.literal_eval(condition))


@given(parsers.parse('I want to use a actions delay {actions_delay}'))
def step_with_actions_delay(actions_delay):
    """ actions delay """
    builder_instance.with_actions_delay(1000)


@given(parsers.parse('I want to use a actions "{actions}"'))
def step_with_actions(actions):
    """ actions """
    builder_instance.with_actions(ast.literal_eval(actions))


@given(parsers.parse('I want to use a code "{code}"'))
def step_with_code(code):
    """ code """
    builder_instance.with_code(code)


@given(parsers.parse('I want to use a parameters "{parameters}"'))
def step_with_parameters(parameters):
    """ parameters """
    builder_instance.with_parameters(ast.literal_eval(parameters))


@given(parsers.parse('I want to use a format "{format_path}"'))
def step_with_format(format_path):
    """ format """
    builder_instance.with_format(format_path)


@given(parsers.parse('I want to use a transpose'))
def step_with_transpose():
    """ transpose """
    builder_instance.with_transpose()


@given(parsers.parse('I want to use a mapping "{mapping_transpose}"'))
def step_with_mapped_transpose(mapping_transpose):
    """ mapping """
    builder_instance.with_mapped_transpose(ast.literal_eval(mapping_transpose))


@then(parsers.parse('I wait "{number_second}" seconds'))
def step_wait_seconds(number_second):
    """ timeSleep """
    time.sleep(number_second)


@given(parsers.parse('I want to use device identifier "{device_identifier}"'))
def step_with_device_identifier(device_identifier):
    """ device identifier for collection """
    builder_instance.with_device_identifier(device_identifier)


@given(parsers.parse('I want to use origin device identifier "{origin_device_identifier}"'))
def step_with_origin_device_identifier(origin_device_identifier):
    """ device origin identifier for collection """
    builder_instance.with_origin_device_identifier(origin_device_identifier)


@given(parsers.parse('I want to use version "{version}"'))
def step_with_version(version):
    """ device version for collection """
    builder_instance.with_version(version)


@given(parsers.parse('I want to use version "{path}"'))
def step_with_path(path):
    """ device version for collection """
    builder_instance.with_version(path)


@given(parsers.parse('I want to use trustedboot "{trustedboot}"'))
def step_with_trustedboot(trustedboot):
    """ trustedboot """
    builder_instance.with_trustedboot(trustedboot)


@given(parsers.parse('I want to use add datastream datapoints "{datastream_id}", {datapoints}'))
def add_datastream_datapoints(datastream_id, datapoints):
    datapoints = eval(datapoints)
    builder_instance.add_datastream_datapoints(datastream_id, datapoints)


@given(parsers.parse('I want to use add datastream datapoints with from "{datastream_id}", {datapoints}'))
def add_datastream_datapoints_with_from(datastream_id, datapoints):
    datapoints = eval(datapoints)
    builder_instance.add_datastream_datapoints_with_from(datastream_id, datapoints)


@given(parsers.parse('I want to use add device datastream datapoints "{device_id}", "{datastream_id}", {datapoints}'))
def add_device_datastream_datapoints(device_id, datastream_id, datapoints):
    datapoints = eval(datapoints)
    builder_instance.add_device_datastream_datapoints(device_id, datastream_id, datapoints)


@given(parsers.parse(
    'I want to use add device datastream datapoints with from "{device_id}", "{datastream_id}", {datapoints}'))
def add_device_datastream_datapoints_with_from(device_id, datastream_id, datapoints):
    datapoints = eval(datapoints)
    builder_instance.add_device_datastream_datapoints_with_from(device_id, datastream_id, datapoints)


@given(parsers.parse(
    'I want to use from dataframe with device id "{device_id}", datastream id "{datastream_id}" and value {value}'))
def from_dataframe(device_id, datastream_id, value):
    df = pd.DataFrame({
        'device_id': [device_id],
        "data_stream_id": [datastream_id],
        'value': [value]
    })
    builder_instance.from_dataframe(df)


@given("I want to use from spreadsheet")
def from_spreadsheet():
    builder_instance.from_spreadsheet("test/utils/collect.xlsx", 0)


@given(parsers.parse('I want to use from dict "{json_dict}"'))
def step_from_dict(json_dict):
    builder_instance.from_dict(ast.literal_eval(json_dict))


@given(parsers.parse('I want to use from csv "{csv_path}"'))
def step_from_csv(csv_path):
    builder_instance.from_csv(csv_path)


@given(parsers.parse('I want to use from excel "{excel_path}"'))
def step_from_excel(excel_path):
    builder_instance.from_excel(excel_path)


@given(parsers.parse('I want to use from pandas "{pandas}"'))
def step_from_excel(pandas):
    df1 = pd.DataFrame(ast.literal_eval(pandas))
    builder_instance.from_dataframe(df1)


@given("I set the JSON payload for the IoT collection")
def set_json_payload():
    data = {
        'version': '1.1.1',
        'datastreams': [
            {
                "id": "entity.location",
                "datapoints": [
                    {
                        "value": {
                            "position": {
                                "type": "Point",
                                "coordinates": [
                                    1111,
                                    3333]
                            }
                        }
                    }

                ]
            },
            {'id': 'device.temperature.value', 'datapoints': [{'value': 25, 'at': 1000}]}
        ]
    }
    builder_instance.from_dict(data)


@then("The dictionary should match the expected JSON output")
def verify_dict():
    to_dict = builder_instance.build().to_dict()
    expect_dict = {'version': '1.1.1', 'datastreams': [{'id': 'entity.location', 'datapoints': [
        {'value': {'position': {'type': 'Point', 'coordinates': [1111, 3333]}}}]}, {'id': 'device.temperature.value',
                                                                                    'datapoints': [
                                                                                        {'value': 25, 'at': 1000},
                                                                                        {'value': 25,
                                                                                         'at': 1431602523123,
                                                                                         'from': 1431602523123},
                                                                                        {'value': 25,
                                                                                         'at': 1431602523123}]}]}
    assert to_dict == expect_dict


@then("The dictionary for bulk iot collection expected JSON output")
def verify_dict():
    to_dict = builder_instance.build().to_dict()
    assert isinstance(to_dict, dict)


@then(parsers.parse('The status code from collection should be "{status_code}"'))
def check_response(status_code):
    response = builder_instance.build().execute()
    assert response['status_code'] == int(status_code)


@then('Check that I receive data')
def check_response():
    response = builder_instance.build().execute()
    assert response is not None
    assert len(response) > 0


@then(parsers.parse('The status code from device "{device}" iot collection should be "{status_code}"'))
def check_response(device, status_code):
    response = builder_instance.build().execute()
    assert response[device]['status_code'] == int(status_code)


@when('To dict')
def step_create():
    """ Step create"""
    response = builder_instance.build().to_dict()
    print(response)
    assert response['code'] == int(status_code)


@when('I create')
def step_create():
    """ Step create"""
    builder_instance.create()


@when('I update')
def step_update():
    """ Step update """
    builder_instance.update()


@when('I find all')
def step_find_all():
    """ Step find all """
    builder_instance.find_all()


@when('I find one')
def step_find_one():
    """ Step find one """
    builder_instance.find_one()


@when('I validate')
def step_validate():
    """ Step find one """
    builder_instance.validate()


@when('I download')
def step_download():
    """ Step download """
    builder_instance.download().build().execute()


@when('I prediction')
def step_prediction():
    """ Step download """
    builder_instance.prediction()


@when('I save')
def step_save():
    """ Step save """
    builder_instance.save()


@when('I evaluate transformer')
def step_evaluate():
    """ Step download """
    builder_instance.evaluate()


@when('I delete')
def step_delete():
    """ Step delete """
    builder_instance.delete()


@when('I search')
def step_search():
    """ Step search """
    builder_instance.search()


@when('I catalog')
def step_catalog():
    """ Step catalog """
    builder_instance.catalog()


@when('I update parameters')
def step_update_parameters():
    """ Step parameters """
    builder_instance.update_parameters()


@then(parsers.parse('The response should be "{status_code}"'))
def step_status_code(status_code):
    """Step_then_the_response_should_be"""
    response = builder_instance.build().execute()
    assert response['status_code'] == int(status_code)


@then(parsers.parse('The prediction should be {prediction}'))
def step_prediction_result(prediction):
    """ Step The prediction should be"""
    response = builder_instance.build().execute()
    predic = ast.literal_eval(prediction)
    builder_instance.with_prediction(predic)
    assert response['data'] == predic
    time.sleep(2)


@given(parsers.parse('I want to use a select {select}'))
def step_prediction_result(select):
    select_list = json.loads(select)
    builder_instance.with_select(select_list)


@given(parsers.parse('I want to use a select {select}'))
def step_prediction_result(select):
    select = select.replace("'", '"')
    select_list = json.loads(select)
    builder_instance.with_select(select_list)


@then(parsers.parse('The response search should be "{expected_type}"'))
def step_response_should_be_expected_type_search(expected_type):
    """ expected type search """
    response_data = builder_instance.build().execute()
    if expected_type == 'dict':
        assert isinstance(response_data, dict), 'is not a dict'
    elif expected_type == 'csv':
        assert isinstance(response_data, str), 'is not a csv'
    elif expected_type == 'pandas':
        assert isinstance(response_data, pd.DataFrame), 'is not a pandas DataFrame'
    else:
        raise ValueError(f'Unsupported data type for test: {expected_type}')


@then(parsers.parse('verify table values:\n{attr_value_table}'))
def verify_table_values(attr_value_table):
    """ compare table """
    pd_datapoints = builder_instance.build().execute()

    # Convertir la tabla del feature en un DataFrame
    attr_value_df = pd.read_csv(StringIO(attr_value_table), sep='|', skipinitialspace=True)

    # Limpiar los nombres de las columnas y eliminar columnas no deseadas
    attr_value_df.columns = attr_value_df.columns.str.strip()
    columns_to_drop = [col for col in attr_value_df.columns if col.startswith('Unnamed')]
    attr_value_df.drop(columns=columns_to_drop, inplace=True)
    attr_value_df.replace("NaN", None, inplace=True, regex=True)
    attr_value_df.replace("None", None, inplace=True, regex=True)

    # Convertir ambos DataFrames a JSON
    pd_datapoints_json = pd_datapoints.to_json(orient='records', date_format='iso', date_unit='s')
    attr_value_json = attr_value_df.to_json(orient='records', indent=4)

    # Convertir los JSON a listas de diccionarios para la comparación
    pd_datapoints_records = json.loads(pd_datapoints_json)
    attr_value_records = json.loads(attr_value_json)

    # Eliminar espacios en blanco adicionales en los valores de attr_value_records
    for record in attr_value_records:
        for key in record:
            if isinstance(record[key], str):
                record[key] = re.sub(r'\s+', ' ', record[key]).strip()

    assert pd_datapoints_records == attr_value_records, "Data does not match"


def get_value_from_path(data_dict, path):
    """ search path in objet ownword.py """
    keys = path.split('.')
    value = data_dict
    for key in keys:
        value = value.get(key)
        if value is None:
            raise ValueError(f'Invalid path: {path}')
    return value


