"""
Goal: Implement ZWL API testing
@authors:
    Gaël MONDON
"""
import base64
import json
import os

from fastapi.testclient import TestClient
from app.main import app
from app.config import defaults


valid_credentials = base64.b64encode(str.encode("{}:{}".format(defaults['username'], defaults['password']))).decode("utf-8")
current_dir = os.getcwd()

client = TestClient(app)


def read_json_file(filename):
    # read file
    with open(filename, 'r') as file:
        return file.read()


def exec_post_global(url, data, add_headers=None):
    h = {"Content-Type": "application/json", "Authorization": "Basic " + valid_credentials}
    if add_headers is not None:
        h = h | add_headers
    #print(current_dir+'/headers:{}'.format(h))
    return client.post(url, json=data, headers=h)


def test_post_aws():
    response = exec_post_global("/zabbix/aws/sns",
                                read_json_file(current_dir+'/tests/data/aws.notif.json'),
                                {'x-amz-sns-message-type': 'Notification'})
    print(current_dir+'/test_post_aws.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_gcp():
    response = exec_post_global("/zabbix/gcp",
                                read_json_file(current_dir+'/tests/data/gcp.incident1.json'))
    print(current_dir+'/test_post_gcp.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_azure_common():
    response = exec_post_global("/zabbix/azure/common",
                                read_json_file(current_dir+'/tests/data/azure.common.json'))
    print(current_dir+'/test_post_azure_common.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_generic():
    response = exec_post_global("/zabbix/generic",
                                read_json_file(current_dir+'/tests/data/generic.json'))
    print(current_dir+'/test_post_generic.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_health_stats():
    response = client.get("/health/stats",
                          headers={"Authorization": "Basic " + valid_credentials})
    print(current_dir+'/test_get_health_stats.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_health():
    response = client.get("/health")
    print(current_dir+'/test_get_health.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_help():
    response = client.get("/help")
    print(current_dir+'/test_get_help.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


if __name__ == "__main__":
    """ Health & stats """
    test_get_help()
    test_get_health()
    test_get_health_stats()

    """ Generic """
    test_post_generic()

    """ Azure """
    test_post_azure_common()

    """ GCP """
    test_post_gcp()

    """ AWS """
    #test_post_aws()

