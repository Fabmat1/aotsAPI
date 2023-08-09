import os

import aotsAPI
from api_calls import bulk_upload_spectra, bulk_upload_rvcurves

# aotsAPI.config_params["url"] = http://somealternativeurl.com # parameters may be modified like this

# response = bulk_upload_spectra([r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits",
#                                 r"C:\Users\fabia\Downloads\spec-0348-51671-0043.fits"], 1)


filelist = []

for dir in os.listdir(r"C:\Users\fabia\PycharmProjects\RVVD\output"):
    if len(filelist) > 50:
        response = bulk_upload_rvcurves(filelist, 1)
        print(response.status_code)
        print(response.content)
        filelist = []

    for file in os.listdir("C:\\Users\\fabia\\PycharmProjects\\RVVD\\output\\" + dir):
        if file.endswith(".fits"):
            filelist.append("C:\\Users\\fabia\\PycharmProjects\\RVVD\\output\\" + dir + "\\"+file)




print(response.content)
