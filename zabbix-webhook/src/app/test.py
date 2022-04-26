"""
Goal: Implement ZWL API testing
@authors:
    Gaël MONDON
"""
import base64
import json

from fastapi.testclient import TestClient
from app.main import app
from app.config import defaults


valid_credentials = base64.b64encode(str.encode("{}:{}".format(defaults['username'], defaults['password']))).decode("utf-8")


client = TestClient(app)

def read_json_file(filename):
    # read file
    with open(filename, 'r') as file:
        return file.read()



def test_post_global(url, data):
    return client.post(url, json=data, headers={"Content-Type": "application/json", "Authorization": "Basic " + valid_credentials})


def test_post_aws(data):
    response = test_post_global("/zabbix/aws/sns", data)
    print('test_post_aws.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_gcp(data):
    response = test_post_global("/zabbix/gcp", data)
    print('test_post_gcp.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_azure_common(data):
    response = test_post_global("/zabbix/azure/common", data)
    print('test_post_azure_common.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_post_generic(data):
    response = test_post_global("/zabbix/generic", data)
    print('test_post_generic.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_health_stats():
    response = client.get("/health/stats", headers={"Authorization": "Basic " + valid_credentials})
    print('test_get_health_stats.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_health():
    response = client.get("/health")
    print('test_get_health.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


def test_get_help():
    response = client.get("/help")
    print('test_get_help.status_code:{}'.format(response.status_code))
    assert response.status_code == 200


if __name__ == "__main__":
    """ Health & stats """
    test_get_help()
    test_get_health()
    test_get_health_stats()

    """ Generic """
    test_post_generic(read_json_file('../test/generic.json'))

    """ Azure """
    test_post_azure_common(read_json_file('../test/azure.common.json'))

    """ GCP """
    test_post_gcp(read_json_file('../test/gcp.incident1.json'))

    """ AWS """
    test_post_aws(read_json_file('../test/aws.notif.json'))

