import numpy as np
from astropy.io import fits


shorten_meta_sed = {
    'ra': 'RA',
    'dec': 'DEC',
    'name': 'NAME',
    'source_id': 'SID',
    'teff': 'TEFF',
    'teff_lerr': 'TEFF_LE',
    'teff_uerr': 'TEFF_UE',
    'logg': 'LOGG',
    'logg_lerr': 'LOGG_LE',
    'logg_uerr': 'LOGG_UE',
    'metallicity': 'METAL',
    'metallicity_lerr:': 'METAL_LE',
    'metallicity_uerr:': 'METAL_UE',
    'color_excess': 'CEX',
    'color_excess_lerr': 'CEX_LE',
    'color_excess_uerr': 'CEX_UE',
    'logtheta': 'LOGT',
    'logtheta_lerr': 'LOGT_LE',
    'logtheta_uerr': 'LOGT_UE',
}

keyconformtofitsdict = {
    "source_id": "SID",
    "ra": "RA",
    "dec": "DEC",
    "spec_class": "SPCLASS",
    "logp": "LOGP",
    "deltaRV": "DRV",
    "deltaRV_err": "U_DRV",
    "RVavg": "RVAVG",
    "RVavg_err": "U_RVAVG",
    "Nspec": "NSPEC",
    "associated_files": "ASOC_F",
    "timespan": "TSPAN"
}


colnames_correspondence = {
    "culum_fit_RV": "RV",
    "u_culum_fit_RV": "RVERR",
    "mjd": "MJD"
}


def preprocess_rvcurve(metadata, times, rvs, rv_uerr, rv_lerr, output_name):
    """
    This function pre-processes RV curve data and metadata, converts them into FITS format, and then writes them into a .fits file.

    :param metadata: Metadata for the RV curve.
    :type metadata: dict

    :param times: The time array of the RV curve.
    :type times: numpy.ndarray

    :param rvs: The array containing RV data.
    :type rvs: numpy.ndarray

    :param rv_uerr: The array of upper errors for the RV data.
    :type rv_uerr: numpy.ndarray

    :param rv_lerr: The array of lower errors for the RV data.
    :type rv_lerr: numpy.ndarray

    :param output_name: The name of the output FITS file.
    :type output_name: str
    """

    if len(times) == 0 or len(rvs) == 0 or len(rv_uerr) == 0 or len(rv_lerr):
        return False

    # Convert metadata to fits header
    meta_hdr = fits.Header()
    for key, value in metadata.items():
        key = keyconformtofitsdict[key]
        value = value.iloc[0]
        if isinstance(value, float):
            if not np.isnan(value):
                meta_hdr[key] = value
        else:
            meta_hdr[key] = value

    # Create fits hdu from data and metadata
    # Create Primary HDU and set EXTEND keyword to True
    primary_hdu = fits.PrimaryHDU(header=meta_hdr)
    primary_hdu.header['EXTEND'] = True

    data_hdu = fits.TableHDU.from_columns([
        fits.Column(name='RV', format='E', array=rvs),
        fits.Column(name='RV_LERR', format='E', array=rv_lerr),
        fits.Column(name='RV_UERR', format='E', array=rv_uerr),
        fits.Column(name='MJD', format='E', array=times),
    ], name='RV_observed_data')

    # Create HDU list
    hdul = fits.HDUList([primary_hdu, data_hdu])

    # Write HDU list to fits file
    hdul.writeto(output_name, overwrite=True)

    return True


def preprocess_sed(metadata, model_wavelength, model_flux, model_magnitude, observed_wavelength, observed_flux,
                   observed_flux_lerr, observed_flux_uerr, observed_magnitude, observed_magnitude_lerr,
                   observed_magnitude_uerr, output_filename):
    """
    Preprocesses spectral energy distribution (SED) data and saves it to a FITS file.

    :param metadata: Metadata information to be included in the FITS file header.
    :type metadata: dict

    :param model_flux: Array of model flux values.
    :type model_flux: numpy.ndarray

    :param model_magnitude: Array of model magnitude values.
    :type model_magnitude: numpy.ndarray

    :param observed_flux: Array of observed flux values.
    :type observed_flux: numpy.ndarray

    :param observed_magnitude: Array of observed magnitude values.
    :type observed_magnitude: numpy.ndarray

    :param output_filename: Output file name for the FITS file.
    :type output_filename: str

    :return: None
    """
    # Create an HDU (Header/Data Unit) list to store the data
    hdu_list = fits.HDUList()

    # Create a primary HDU with metadata
    primary_hdu = fits.PrimaryHDU()

    new_meta = {}
    for key, val in metadata.items():
        if key in shorten_meta_sed:
            new_meta[shorten_meta_sed[key]] = val
        elif key in shorten_meta_sed.values():
            new_meta[key] = val

    primary_hdu.header.extend(new_meta)

    observed_table = fits.TableHDU.from_columns([
        fits.Column(name='Observed_Wavelength', format='E', array=observed_wavelength),
        fits.Column(name='Observed_Flux', format='E', array=observed_flux),
        fits.Column(name='Model_Flux_Lower_Err', format='E', array=observed_flux_lerr),
        fits.Column(name='Model_Flux_Upper_Err', format='E', array=observed_flux_uerr),
        fits.Column(name='Observed_Magnitude', format='E', array=observed_magnitude),
        fits.Column(name='Model_Magnitude_Lower_Err', format='E', array=observed_magnitude_lerr),
        fits.Column(name='Model_Magnitude_Upper_Err', format='E', array=observed_magnitude_uerr),
    ], name='SED_Observed_Data')

    # Create a table HDU for model and observed flux/magnitude data
    model_table = fits.TableHDU.from_columns([
        fits.Column(name='Model_Wavelength', format='E', array=model_wavelength),
        fits.Column(name='Model_Flux', format='E', array=model_flux),
        fits.Column(name='Model_Magnitude', format='E', array=model_magnitude),
    ], name='SED_Model_Data')

    # Add the HDUs to the HDU list
    hdu_list.append(primary_hdu)
    hdu_list.append(observed_table)
    hdu_list.append(model_table)

    # Save the HDU list to a FITS file
    hdu_list.writeto(output_filename, overwrite=True)
