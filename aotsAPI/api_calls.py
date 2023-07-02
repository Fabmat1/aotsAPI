import requests
from aotsAPI import config_params


def fetch_csrf_token(func):
    def wrapper(*args, **kwargs):
        s = requests.Session()
        # TODO: Figure out some other url pattern that returns a valid CSRF Token
        r1 = s.get(config_params["url"] + r"/w/the-edr3-hot-subd/dash/dashboard/")
        csrf_token = r1.cookies['csrftoken']
        kwargs["csrf_token"] = csrf_token
        kwargs["session"] = s
        return func(*args, **kwargs)
    return wrapper


@fetch_csrf_token
def bulk_upload_spectra(file_list, projectid, *args, **kwargs):
    """
    :param file_list: A list of filepaths of the files to upload
    :param projectid: The project name or ID the files should be attributed to
    :return: The servers HTTP response
    """
    s = kwargs["session"]
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

    response = s.post(config_params["url"] + "/api/observations/api-spec-upload/", files=specfiles,
                      data={'csrfmiddlewaretoken': kwargs["csrf_token"]}, headers=headers)
    return response


@fetch_csrf_token
def bulk_download_spectra(file_list, projectid, output_path, *args, **kwargs):
    """
    :param file_list: A list of either names of stars for which spectra should be fetched, or primary keys of the spectra
    :param projectid: The project name or ID the files should be attributed to
    :param output_path: The path to which the .zip file returned by the server should be saved
    :return: The servers HTTP response
    """

    s = kwargs["session"]

    headers = {
        "PUBLICAPIKEY": config_params["public-key"],
        "SECRETAPIKEY": config_params["secret-key"],
        "PROJECTID": str(projectid),
        "STARIDLIST": ";".join(file_list)
    }

    response = s.get(config_params["url"] + "/api/observations/api-spec-download/",
                      data={'csrfmiddlewaretoken': kwargs["csrf_token"]}, headers=headers)

    if not ".zip" in output_path:
        output_path += ".zip"

    with open(output_path, "wb") as output_path:
        output_path.write(response.content)

    return response
