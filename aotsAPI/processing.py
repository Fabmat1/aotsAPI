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


def preprocess_rvcurve():
    pass


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
