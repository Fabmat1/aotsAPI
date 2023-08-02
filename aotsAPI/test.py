import aotsAPI
import astropy.io.fits as fits
from api_calls import bulk_upload_spectra, bulk_download_spectra

# aotsAPI.config_params["url"] = http://somealternativeurl.com # parameters may be modified like this

# response = bulk_upload_spectra([r"spec-0299-51671-05921.fits",
#                                 r"spec-4040-55605-0538.fits",
#                                 r"spec-4040-55605-05381.fits",
#                                 r"spec-56389-HD134427N004207M01_sp08-158.fits",], 1)
#
# print(response.status_code, response.content)


response = bulk_download_spectra(["LAMOST J134545.23-000641.6"], 1, "test.zip")
print(response.status_code)