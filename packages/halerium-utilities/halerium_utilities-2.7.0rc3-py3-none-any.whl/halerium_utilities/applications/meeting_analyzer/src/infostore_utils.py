
import os
import requests

tenant = os.getenv('HALERIUM_TENANT_KEY')
workspace = os.getenv('HALERIUM_PROJECT_ID')
runnerId = os.getenv('HALERIUM_ID')
runnerToken = os.getenv('HALERIUM_TOKEN')
baseUrl = os.getenv('HALERIUM_BASE_URL')


def add_memory_to_store(store_id, memory: str):
    url = f"{baseUrl}/api/tenants/{tenant}/projects/{workspace}/runners/{runnerId}/information-store/stores/{store_id}/memories"

    headers = {
        "halerium-runner-token": runnerToken,
    }

    payload = {"memory": memory}

    response = requests.post(url, headers=headers, params=payload)

    if response.status_code != 200:
        raise Exception("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()



def add_chunks_to_vectorstore(vectorstore_id: str, chunks: list) -> dict:
    """
    Every item in the chunks list must look like this
    {"content": "...", "metadata": {...}}
    """
    url = f"{baseUrl}/api/tenants/{tenant}/projects/{workspace}/runners/{runnerId}/information-store/vectorstore/{vectorstore_id}/chunks/"

    headers = {
        "halerium-runner-token": runnerToken,
    }

    payload = chunks
    
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()

def get_workspace_information_stores() -> dict:
    url = f"{baseUrl}/api/tenants/{tenant}/projects/{workspace}/runners/{runnerId}/information-store/stores/"

    headers = {
        "halerium-runner-token": runnerToken,
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def get_information_store_info(store_id):
    url = f"{baseUrl}/api/tenants/{tenant}/projects/{workspace}/runners/{runnerId}/information-store/stores/{store_id}/"

    headers = {
        "halerium-runner-token": runnerToken,
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()