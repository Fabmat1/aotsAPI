import requests
from aotsAPI import config_params


def bulk_upload_spectra(file_list, projectid, *args, **kwargs):
    """
    :param file_list: A list of filepaths of the files to upload
    :param projectid: The project name or ID the files should be attributed to
    :return: The servers HTTP response
    """
    s = requests.Session()
    # TODO: Figure out some other url pattern that returns a valid CSRF Token
    r1 = s.get(config_params["url"]+r"/w/the-edr3-hot-subd/dash/dashboard/")
    csrf_token = r1.cookies['csrftoken']

    specfiles = []
    for i, file in enumerate(file_list):
        try:
            with open(file, "rb") as f:
                specfiles.append(("spectrumfile", f.read()))
        except FileNotFoundError:
            print(f"The file {file} could not be opened, skipping...")

    headers = {
        "PUBLICAPIKEY": config_params["public-key"],
        "SECRETAPIKEY": config_params["secret-key"],
        "PROJECTID": str(projectid)
    }

    response = s.post(config_params["url"] + "/api/observations/api-spec-upload/", files=specfiles, data={'csrfmiddlewaretoken': csrf_token}, headers=headers)
    return response
