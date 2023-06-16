import aotsAPI
from api_calls import bulk_upload_spectra

# aotsAPI.config_params["url"] = http://somealternativeurl.com # parameters may be modified like this

response = bulk_upload_spectra([r"/path/to/file1",
                                r"/path/to/file2",
                                r"/path/to/file3",
                                r"/path/to/file4"], 1)

print(response)
