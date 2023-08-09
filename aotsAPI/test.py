import aotsAPI
from api_calls import bulk_upload_spectra, bulk_upload_rvcurves

# aotsAPI.config_params["url"] = http://somealternativeurl.com # parameters may be modified like this

# response = bulk_upload_spectra([r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits"], 1)

response = bulk_upload_rvcurves([r"C:\Users\fabia\PycharmProjects\RVVD\test.fits"], 1)

print(response.content)
