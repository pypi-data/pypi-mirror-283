### IMPORT SOFTWARE ###
#########################################################################################################
# BUILT IN
from datetime import datetime, timedelta
import datetime as dt
import time
import csv
import sys
import requests
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib3
import warnings
import bs4
import re
# OTHER
import netCDF4
import cdsapi
import pandas as pd
import xarray as xr
import numpy as np
from numpy import loadtxt
import numpy.ma as ma
from scipy import interpolate
import tropycal 
from tropycal import tracks, recon, realtime
# METPY
import metpy.calc as mpcalc
from metpy.units import units
# SIPHON 
from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS
from siphon.simplewebservice.wyoming import WyomingUpperAir
from siphon.simplewebservice.iastate import IAStateUpperAir
from siphon.simplewebservice.igra2 import IGRAUpperAir
# PYART & NEXRADAWS
# import os
# os.environ['PYART_QUIET'] = 'True'
# import pyart
# import nexradaws
# import pytz

# SOUNDERPY
from .plot import __full_sounding, __full_hodograph, __simple_sounding, __composite_sounding, __vad_hodograph
from .calc import *

#########################################################################################################

'''
    SOUNDERPY | Vertical Profile Data Retrieval and Analysis Tool For Python
    -------------------------------------------------------------------------
    An atmospheric science Python package that retrieves & visualizes vertical profile data for meteorological analysis. 

    THIS RELEASE
    -------
    Version: 3.0.5 | July 2024

    DOCUMENTATION
    -------
    Docs: https://kylejgillett.github.io/sounderpy/
    Code: https://github.com/kylejgillett/sounderpy
    PyPi: https://pypi.org/project/sounderpy/
    Operational Site: https://sounderpysoundings.anvil.app/

    COPYRIGHT
    ---------
    Created by Kyle J Gillett (@wxkylegillett) 2023, 2024
    
'''

citation_text = f"""
## ---------------------------------- SOUNDERPY ----------------------------------- ##
##          Vertical Profile Data Retrieval and Analysis Tool For Python            ##
##                     v3.0.4 | June 2024 | (C) Kyle J Gillett                      ##
##                 Docs: https://kylejgillett.github.io/sounderpy/                  ##
## --------------------- THANK YOU FOR USING THIS PACKAGE! ------------------------ ##
"""
print(citation_text)

#########################################################################################################



#########################################################################
############################# FUNCTIONS #################################
#########################################################################



#######################
# MODEL REANALYSIS DATA 
#########################################################################

def get_model_data(model, latlon, year, month, day, hour, dataset=None, box_avg_size=0.10, hush=False):
    st = time.time()
    
    r"""Get model reanalysis vertical profile data

       Return a ``dict`` of 'cleaned up' model reanalysis data from a given model, for a given location, date, and time

       :param model: the requested model to use (rap-ruc, era5, ncep)
       :type model: str, required
       :param latlon: the latitude & longitude pair for sounding ([44.92, -84.72])
       :type latlon: list, required
       :param year: valid year
       :type year: str, required
       :param month: valid month
       :type month: str, required
       :param day: valid day
       :type day: str, required
       :param hour: required, valid hour
       :type hour: str, required
       :param dataset: optional, target a specific dataset instead of searching for the first one with data.
       :type dataset: str, optional
       :param box_avg_size: optional, determine an area-averaged box size in degrees, default is 0.10 degrees.
       :type box_avg_size: int, optional
       :param hush: whether to 'hush' a read-out of thermodynamic and kinematic parameters when getting a data.
       :type hush: bool, optional, default is `False`
       :return: clean_data, a dict of ready-to-use vertical profile data including pressure, height, temperature, dewpoint, u-wind, v-wind, & model information
       :rtype: dict
    
    """
    
    # send error message if given model is invaild 
    if model.casefold() not in ['era', 'era5', 'rap', 'ruc', 'rap-ruc', 'rap-now', 'ncep-fnl', 'ncep']:
        raise ValueError(f"The model you requested, '{model}', is not a valid model. Valid models for this function include ['rap-ruc', 'era5', 'ncep']")
    
    # create list of lat-lon points for box-average domain
    #                    + lat                   # - lat                   # - lon                   # + lon
    latlons = [latlon[0] + box_avg_size, latlon[0] - box_avg_size, latlon[1] - box_avg_size, latlon[1] + box_avg_size]

    
    ### ERA 5 REANALYSIS ###
    #########################################################################################################
    '''
    Get ERA-5 reanalysis data the CDS API, return an xarray dataset of the data.
    '''
    if model.casefold() in ['era', 'era5']:
        # define source 
        source = 'ERA5'
        dtype  = 'reanalysis'
        
        print(f'> ERA5 REANALYSIS DATA ACCESS FUNCTION --\n------------------------------------------')
        print(f'> SOME MESSAGES FROM THE ECMWF CDS...')
    
        # define ERA5 dataset names we want to acess data from
        dataset_presLvls = 'reanalysis-era5-pressure-levels'
        dataset_singleLvls = 'reanalysis-era5-single-levels'
        download_flag = 'false' 
        
        # rearange lat-lon list for my sanity
        latlon_list = [latlons[0], latlons[2], latlons[1], latlons[3]]

        # set up cds api call for pressure level data 
        c = cdsapi.Client()
        params = {
                'product_type':'reanalysis',
                'variable': ['temperature', 'geopotential', 'relative humidity', 'U WIND COMPONENT', 'V WIND COMPONENT', 'vertical_velocity'],
                'pressure_level': [
                    '100', '125',
                    '150', '175', '200',
                    '225', '250', '300',
                    '350', '400', '450',
                    '500', '550', '600',
                    '650', '700', '750',
                    '775', '800', '825',
                    '850', '875', '900',
                    '925', '950', '975',
                    '1000',
                ],
                'year'  : year,
                'month' : month,
                'day'   : day,
                'time'  : f'{hour}:00',
                'format': 'netcdf',
                'area'  : latlon_list
                }

        # set up cds api call for surface data 
        c2 = cdsapi.Client()
        params2 = {
                'product_type':'reanalysis',
                'variable': ['2m_temperature', '2m_dewpoint_temperature', 'surface_pressure', '10u', '10v', 'z', 'msl'],
                'year'  : year,
                'month' : month,
                'day'   : day,
                'time'  : f'{hour}:00',
                'format': 'netcdf',
                'area'  : latlon_list
                }

        # retrieve data from CDS
        fl = c.retrieve(dataset_presLvls , params)
        print('> DATASET ACCESSED: '+dataset_presLvls )
        fl2 = c2.retrieve(dataset_singleLvls, params2)
        print('> DATASET ACCESSED: '+dataset_singleLvls )
        # load data to memory via output.nc files
        fl.download("./output.nc")
        fl2.download("./output.nc")
        
        # create xarray datasets from .nc files
        with urlopen(fl.location) as f:
            ds = xr.open_dataset(f.read())
        with urlopen(fl2.location) as f:
            ds2 = xr.open_dataset(f.read())
        
        # merge the two datasets together
        ds2 = ds2.rename({'z':'hgts','sp':'ps','t2m':'Ts','d2m':'tds','u10':'us','v10':'vs', })
        raw_data = xr.merge([ds,ds2])

    #########################################################################################################

    
    
    ### RAP REANALYSIS ###
    #########################################################################################################
    '''
    Get RAP reanalysis data from NCEI THREDDS Server, return a netcdf4 dataset
    '''
    if model in ['rap', 'ruc', 'rap-ruc']:
        
        dtype  = 'reanalysis'
        
        print(f'> RAP REANALYSIS DATA ACCESS FUNCTION --\n-----------------------------------------')

        # rearange latlon list for my sanity
        latlon_list = [latlons[2], latlons[3], latlons[1], latlons[0]]

        # create dict of RAP-data urls for the different datasets of RAP and RUC from NCEI    
        urls = {
        'RAP_25km' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap252/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
        'RAP_25km_old' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap252-old/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
            
        'RAP_25km_anl' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap252anl/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
        'RAP_25km_anl_old' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap252anl-old/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
                
        'RAP_13km' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap130/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
        'RAP_13km_old' : 'https://www.ncdc.noaa.gov/thredds/ncss/model-rap130-old/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
            
        'RAP_13km_anl' : 'https://www.ncei.noaa.gov/thredds/ncss/model-rap130anl/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
        'RAP_13km_anl_old' : 'https://www.ncdc.noaa.gov/thredds/ncss/model-rap130anl-old/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/rap_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
            
        'RUC_13km' : 'https://www.ncei.noaa.gov/thredds/ncss/model-ruc130anl/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/ruc2anl_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
        'RUC_13km_old' : 'https://www.ncei.noaa.gov/thredds/ncss/model-ruc130anl-old/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/ruc2anl_130_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb2',
            
        'RUC_25km' : 'https://www.ncei.noaa.gov/thredds/ncss/model-ruc252anl/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/ruc2anl_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb',
        'RUC_25km_old' : 'https://www.ncei.noaa.gov/thredds/ncss/model-ruc252anl/'+str(year)+str(month)+'/'+str(year)+str(month)+str(day)+'/ruc2anl_252_'+str(year)+str(month)+str(day)+'_'+str(hour)+'00_000.grb'
        }
        
        # if a user defined a target dataset, try it.
        tries = 0
        if dataset is not None:
            try:
                print(f'> SEARCHING FOR {dataset}...')
                url = NCSS(urls[dataset])
                print(f'> DATASET FOUND: {dataset}')
                url_to_use = urls[dataset]
                source = str(dataset)[0:3]
                data = NCSS(url_to_use)
            except:
                 raise ValueError(f'NCSS Connection failed -- the date and dataset you requested is invalid. Ensure you have the correct dates, model, & dataset name\n' +
                            f'Note: data may not be available for every date/time. This catalog experiences periodic outages and may host missing data.\n' +
                            f'The date you entered is: {year}-{month}-{day}-{hour}z. An example of a valid date is: 2014-06-16-18z')
          
        # else, create a simple test for each URL, use the first one that works 
        # and return its data
        else:
            
            tries = 0
            for url, key in zip(urls.values(), urls.keys()):
                try:
                    NCSS(url)
                    print(f'> DATASET USED: {key}')
                    url_to_use = url
                    source = str(key)[0:3]
                    break
                except:
                    tries+=1
                    pass

            if tries == 12:
                    raise ValueError(f'NCSS Connection failed -- ensure you have the correct dates and corresponding model\n' +
                            f'Note: data may not be available for every date/time. This catalog experiences periodic outages and may host missing data.\n' +
                            f'The date you entered is: {year}-{month}-{day}-{hour}z. An example of a valid date is: 2014-06-16-18z')
            else:
                data = NCSS(url_to_use)

            
        # set up TDS query 
        query = data.query()
        
        # subset data by variable names for RAP & RUC (of course they have to be different)
        if source in ['rap', 'RAP']:
            query.variables('Pressure_surface',
                        'Geopotential_height_isobaric', 'Geopotential_height_surface',
                        'Temperature_isobaric', 'Temperature_height_above_ground',
                        'Relative_humidity_isobaric', 'Dewpoint_temperature_height_above_ground',
                        'Relative_humidity_height_above_ground', 'Vertical_velocity_pressure_isobaric',
                        'u-component_of_wind_height_above_ground', 'v-component_of_wind_height_above_ground', 
                        'u-component_of_wind_isobaric', 'v-component_of_wind_isobaric').add_lonlat()
        else:
            query.variables('Pressure_surface',
                        'Geopotential_height_isobaric', 'Geopotential_height_surface',
                        'Temperature_isobaric', 'Temperature_height_above_ground',
                        'Relative_humidity_isobaric','Dewpoint_temperature_height_above_ground',
                        'Relative_humidity_height_above_ground',
                        'u-component_of_wind_height_above_ground', 'v-component_of_wind_height_above_ground', 
                        'u-component_of_wind_isobaric', 'v-component_of_wind_isobaric').add_lonlat()
            
        # subset data by requested domain
        query.lonlat_box(latlon_list[0], latlon_list[1], latlon_list[2], latlon_list[3])
        
        # laod the data from TDS
        raw_data = data.get_data(query)

    #########################################################################################################
    
    
    ### NCEP FNL REANALYSIS ###
    #########################################################################################################
    '''
    Get NCEP-FNL reanalysis data from NCEI THREDDS server, return a netcdf4 dataset
    '''
    
    if model.casefold() in ['ncep-fnl', 'ncep', 'fnl']:
        # define source 
        source = 'NCEP-FNL'
        dtype  = 'reanalysis'
        
        print(f'> NCEP-FNL REANALYSIS DATA ACCESS FUNCTION --\n------------------------------------------')
        
        latlon_list = [latlons[0], latlons[2], latlons[1], latlons[3]]

        # access ncss thredds server 
        try:
            data = NCSS(f"https://thredds.rda.ucar.edu/thredds/ncss/grid/files/g/ds083.3/{year}/{year}{month}/gdas1.fnl0p25.{year}{month}{day}{hour}.f00.grib2")
            worked = True
        except: 
            worked = False
            pass

        if worked == True:
            # set up TDS query 
            query = data.query()

            query.variables('Geopotential_height_isobaric', 'Geopotential_height_surface',
                        'Temperature_isobaric', 'Temperature_height_above_ground',
                        'Relative_humidity_isobaric', 'Dewpoint_temperature_height_above_ground',
                        'Relative_humidity_height_above_ground', 'Pressure_surface',
                        'u-component_of_wind_height_above_ground', 'v-component_of_wind_height_above_ground', 
                        'u-component_of_wind_isobaric', 'v-component_of_wind_isobaric').add_lonlat()

            # subset data by requested domain
            # north=90.000&    west=-.125&    east=-.125&    south=-90.000
            query.lonlat_box(latlon_list[1], latlon_list[3], latlon_list[2], latlon_list[0])

            # laod the data from TDS
            raw_data = data.get_data(query)

        else:
            raise ValueError(f'NCSS Connection failed -- ensure you have the correct dates and corresponding model\n' +
                f'Note: data may not be available for every date/time. This catalog experiences periodic outages and may host missing data.\n' +
                f'The date you entered is: {year}-{month}-{day}-{hour}z. An example of a valid date is: 2014-06-16-18z')
    #########################################################################################################
    
    
    
    ### RAP ANALYSIS ###
    #########################################################################################################
    '''
    Get latest RAP analysis from NCEI THREDDS Server 
    '''
    if model in ['rap-now']:

        print(f'> RAP REANALYSIS DATA ACCESS FUNCTION --\n-----------------------------------------')
        
        latlon_list = [latlons[2],latlons[3],latlons[1],latlons[0]]

        # define dataset URL & try to access it to make sure it works 
        url = 'http://thredds.ucar.edu/thredds/catalog/grib/NCEP/RAP/CONUS_13km/latest.xml'
        try:
            cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/RAP/CONUS_13km/latest.xml')
            source = 'RAP'
            dtype  = 'analysis'
            worked = True
        except:
            worked = False
            pass
        if worked == True:
        # set up TDS query    
            latest_ds = list(cat.datasets.values())[0]
            ncss = NCSS(latest_ds.access_urls['NetcdfSubset'])
            query = ncss.query()
            # Find start time
            start_time = ncss.metadata.time_span['begin']
            fcst_date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            year1  = fcst_date.strftime('%Y')
            month1 = fcst_date.strftime('%m')
            day1   = fcst_date.strftime('%d')
            hour1  = fcst_date.strftime('%H')
            # Subset data by time
            query.time(fcst_date).accept('netcdf4')
            # Subsets data by variables 
            query.variables('MSLP_MAPS_System_Reduction_msl','Pressure_surface','Geopotential_height_isobaric',
                    'Temperature_isobaric', 'Relative_humidity_isobaric','Temperature_height_above_ground',
                    'Relative_humidity_height_above_ground','u-component_of_wind_height_above_ground', 
                    'v-component_of_wind_height_above_ground', 'u-component_of_wind_isobaric', 'v-component_of_wind_isobaric').add_lonlat()

            # Subset data by lat-lon domain 
            query.lonlat_box(latlon_list[0], latlon_list[1], latlon_list[2], latlon_list[3])

            # Gets data
            raw_data = ncss.get_data(query)

        else:
            raise ValueError(f'NCSS Connection failed -- RAP data may not be available at this time')
    #########################################################################################################
    
    
    
    
    ### NOW PARSE RAW MODEL DATA ###
    #########################################################################################################
    '''
    Convert raw datasets into SoudnerPy 'clean_data' dicts
    '''
    
    def parse_data(raw_data, latlon, box_avg_size):
        
        r"""Get model reanalysis vertical profile data
           :param raw_data: raw datasets from data retrieval methods above 
           :type raw_data: dataset, required
           :return: clean_data, a dict of ready-to-use vertical profile data including pressure, height, temperature, dewpoint, u-wind, v-wind, & model information
           :rtype: dict
        """
        
        # if dataset is a xarray.core dataset, it came from the ERA5
        # and specific processing of this data is needed
        if str(type(raw_data)) == "<class 'xarray.core.dataset.Dataset'>":

            print(f'> ERA5 REANALYSIS DATA PARSE FUNCTION --\n------------------------------------------')
            vert_data = {
            'vert_T' : np.mean(np.array(raw_data['t'][0,:,:,:]-273.15), axis=(1,2)),
            'vert_p' : np.array(raw_data['level']),
            'vert_z' : np.mean(np.array(raw_data['z'][0])/9.80665, axis=(1,2)),
            'vert_rh': np.mean(np.array(raw_data['r'][0]), axis=(1,2)),
            'vert_u' : np.mean(np.array(raw_data['u'][0])*1.94384, axis=(1,2)),
            'vert_v' : np.mean(np.array(raw_data['v'][0])*1.94384, axis=(1,2)),
            'vert_Td': (mpcalc.dewpoint_from_relative_humidity(
                np.mean(np.array(raw_data['t'][0,:,:,:]-273.15), axis=(1,2))*units.degC,
                np.mean(np.array(raw_data['r'][0]), axis=(1,2))*units.percent)).m,
            }  
            sfc_data = {
            'sfc_T' : np.mean(np.array(raw_data['Ts'][0,:])-273.15),
            'sfc_p' : np.mean(np.array(raw_data['ps'][0,:])/100),
            'sfc_z' : np.mean(np.array(raw_data['hgts'][0,:])/9.80665),
            'sfc_Td': np.mean(np.array(raw_data['tds'][0,:])-273.15),
            'sfc_rh': (mpcalc.relative_humidity_from_dewpoint(
                np.mean(np.array(raw_data['Ts'][0,:])-273.15)*units.degC, 
                np.mean(np.array(raw_data['tds'][0,:])-273.15)*units.degC)*100),
            'sfc_u' : (np.array(raw_data['us'][0,:])*1.94384),
            'sfc_v' : (np.array(raw_data['vs'][0,:])*1.94384)
            }
            
            # parse out raw dataset date and time
            vtime = np.datetime_as_string(raw_data.time.values[0])
            strftime = [vtime[0:4], vtime[5:7], vtime[8:10], vtime[11:13]]

            latlon_data = {
            'data_lat'    : (raw_data['latitude'][:]),
            'data_lon'    : (raw_data['latitude'][:]),
            'data_latnum' : (raw_data['latitude'][:]).shape[0],
            'data_lonnum' : (raw_data['latitude'][:]).shape[0], 
            'data_time'   : (strftime)
            }



        # if data is a netCDF4 dataset, it is RAP, RUC or NCEP data
        if str(type(raw_data)) == "<class 'netCDF4._netCDF4.Dataset'>":

                # if Geopotential_height_surface exists within the dataset, it is reanalysis data
                if "Geopotential_height_surface" in raw_data.variables.keys():

                    # try to determine how many isobaric levels exist in the dataset
                    # this is mainly for the NCEP-FNL dataset which annoyingly 
                    # comes with varying isobaric level intervals 

                    try:
                        pressures = (ma.getdata(raw_data.variables['isobaric'])).data/100
                    except:
                        try:
                            pressures = (ma.getdata(raw_data.variables['isobaric1'])).data/100
                        except:
                            try:
                                pressures = (ma.getdata(raw_data.variables['isobaric2'])).data/100
                            except:
                                try:
                                    pressures = (ma.getdata(raw_data.variables['isobaric3'])).data/100
                                except:
                                    pass
                                pass
                            pass
                        pass
                    # pressures = (np.array([100, 125, 150, 175, 200, 225, 250, 275, 
                    #                300, 325, 350, 375, 400, 425, 450, 475, 
                    #                500, 525, 550, 575, 600, 625, 650, 675, 
                    #                700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]))
                    
                    # create a dict of vertical data 
                    vert_data = {
                        'vert_T' : np.mean(ma.getdata(raw_data.variables['Temperature_isobaric'][0,:,:,:]-273.15), axis=(1,2)),
                        'vert_p' : pressures,
                        'vert_z' : np.mean(ma.getdata(raw_data.variables['Geopotential_height_isobaric'][0,:,:,:]), axis=(1,2)),
                        'vert_rh': np.mean(ma.getdata(raw_data.variables['Relative_humidity_isobaric'][0,:,:,:]), axis=(1,2)),
                        'vert_u' : np.mean(ma.getdata(raw_data.variables['u-component_of_wind_isobaric'][0,:,:,:]*1.94384), axis=(1,2)),
                        'vert_v' : np.mean(ma.getdata(raw_data.variables['v-component_of_wind_isobaric'][0,:,:,:]*1.94384), axis=(1,2)),
                        'vert_Td': (mpcalc.dewpoint_from_relative_humidity(
                            np.mean(ma.getdata(raw_data.variables['Temperature_isobaric'][0,:,:,:]-273.15), axis=(1,2))*units.degC, 
                            np.mean(ma.getdata(raw_data.variables['Relative_humidity_isobaric'][0,:,:,:]),  axis=(1,2))*units.percent)).m,
                    } 

                    # create a dict of sfc data 
                    sfc_data = {
                        'sfc_T' : np.mean(ma.getdata(raw_data.variables['Temperature_height_above_ground'][0,0,:,:]-273.15)),
                        'sfc_p' : np.mean(ma.getdata(raw_data.variables['Pressure_surface'][0,:,:]/100)),
                        'sfc_z' : np.mean(ma.getdata(raw_data.variables['Geopotential_height_surface'][0,:,:])),
                        'sfc_rh': np.mean(ma.getdata(raw_data.variables['Relative_humidity_height_above_ground'][0,0,:,:])),
                        'sfc_u' : np.mean(ma.getdata(raw_data.variables['u-component_of_wind_height_above_ground'][0,0,:,:]*1.94384)),
                        'sfc_v' : np.mean(ma.getdata(raw_data.variables['v-component_of_wind_height_above_ground'][0,0,:,:]*1.94384)),
                        'sfc_Td': (mpcalc.dewpoint_from_relative_humidity(
                            np.mean(ma.getdata(raw_data.variables['Temperature_height_above_ground'][0,0,:,:]-273.15))*units.degC, 
                            np.mean(ma.getdata(raw_data.variables['Relative_humidity_height_above_ground'][0,0,:,:])*units.percent))).m,
                    } 
                    
                    # parse out raw data date and time
                    dtime = raw_data.variables['Pressure_surface'].dimensions[0]
                    vtime = netCDF4.num2date(raw_data.variables[dtime][:],raw_data.variables[dtime].units)[0]
                    strftime = [vtime.strftime('%Y'), vtime.strftime('%m'),  vtime.strftime('%d'),  vtime.strftime('%H')]

                    # create a dict of lat/lon information 
                    latlon_data = {
                    'data_lat'    : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[1]][:]))),
                    'data_lon'    : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[2]][:]))),
                    'data_latnum' : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[1]][:]))).shape[0],
                    'data_lonnum' : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[2]][:]))).shape[0],
                    'data_time'   : (strftime)
                    }
                    
                    

                else: 

                    # if Geopotential_height_surface is not in the dataset, then it is RAP analysis data 
                    # declare pressures 
                    pressures = (np.array([100, 125, 150, 175, 200, 225, 250, 275, 
                                   300, 325, 350, 375, 400, 425, 450, 475, 
                                   500, 525, 550, 575, 600, 625, 650, 675, 
                                   700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]))

                    # create dict of vertical data 
                    vert_data = {
                    'vert_T' : np.mean(ma.getdata(raw_data.variables['Temperature_isobaric'][0,:,:,:]-273.15), axis=(1,2)),
                    'vert_p' : pressures,
                    'vert_z' : np.mean(ma.getdata(raw_data.variables['Geopotential_height_isobaric'][0,:,:,:]), axis=(1,2)),
                    'vert_rh': np.mean(ma.getdata(raw_data.variables['Relative_humidity_isobaric'][0,:,:,:]), axis=(1,2)),
                    'vert_u' : np.mean(ma.getdata(raw_data.variables['u-component_of_wind_isobaric'][0,:,:,:]*1.94384), axis=(1,2)),
                    'vert_v' : np.mean(ma.getdata(raw_data.variables['v-component_of_wind_isobaric'][0,:,:,:]*1.94384), axis=(1,2)),
                    'vert_Td': (mpcalc.dewpoint_from_relative_humidity(
                        np.mean(ma.getdata(raw_data.variables['Temperature_isobaric'][0,:,:,:]-273.15), axis=(1,2))*units.degC, 
                        np.mean(ma.getdata(raw_data.variables['Relative_humidity_isobaric'][0,:,:,:]),  axis=(1,2))*units.percent)).m,
                } 

                    # create dict of surface data 
                    sfc_data = {
                    'sfc_T' : np.mean(ma.getdata(raw_data.variables['Temperature_height_above_ground'][0,0,:,:]-273.15)),
                    'sfc_p' : np.mean(ma.getdata(raw_data.variables['Pressure_surface'][0,:,:]/100)),
                    #'sfc_z' : (ma.getdata(raw_data.variables['Geopotential_height_surface'][0,:,:])),
                    'sfc_rh': np.mean(ma.getdata(raw_data.variables['Relative_humidity_height_above_ground'][0,0,:,:])),
                    'sfc_u' : np.mean(ma.getdata(raw_data.variables['u-component_of_wind_height_above_ground'][0,0,:,:]*1.94384)),
                    'sfc_v' : np.mean(ma.getdata(raw_data.variables['v-component_of_wind_height_above_ground'][0,0,:,:]*1.94384)),
                    'sfc_Td': (mpcalc.dewpoint_from_relative_humidity(
                        np.mean(ma.getdata(raw_data.variables['Temperature_height_above_ground'][0,0,:,:]-273.15))*units.degC, 
                        np.mean(ma.getdata(raw_data.variables['Relative_humidity_height_above_ground'][0,0,:,:])*units.percent))).m,
                    } 

                    # calculate surface heights 
                    sfc_data['sfc_z'] = np.interp([sfc_data['sfc_p']], vert_data['vert_p'], vert_data['vert_z'])[0]
                    
                    # parse out raw data date and time
                    dtime = raw_data.variables['Pressure_surface'].dimensions[0]
                    vtime = netCDF4.num2date(raw_data.variables[dtime][:],raw_data.variables[dtime].units)[0]
                    strftime = [vtime.strftime('%Y'), vtime.strftime('%m'),  vtime.strftime('%d'),  vtime.strftime('%H')]

                    # create dict of latlon information 
                    latlon_data = {
                    'data_lat'    : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[1]][:]))),
                    'data_lon'    : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[2]][:]))),
                    'data_latnum' : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[1]][:]))).shape[0],
                    'data_lonnum' : (ma.getdata(1000*(raw_data.variables[raw_data.variables['Pressure_surface'].dimensions[2]][:]))).shape[0],
                    'data_time'   : (strftime)
                    }
                
        sb_dict = {}
        new_keys = ['T', 'Td', 'rh', 'u', 'v', 'z', 'p']
        sfc_keys = ['sfc_T', 'sfc_Td', 'sfc_rh', 'sfc_u', 'sfc_v', 'sfc_z', 'sfc_p']
        vert_keys = ['vert_T', 'vert_Td', 'vert_rh', 'vert_u', 'vert_v', 'vert_z', 'vert_p']

        # create a dict of surface-based data 
        for vert_key, sfc_key, new_key in zip(vert_keys, sfc_keys, new_keys):
            sb_dict[new_key] = np.insert(np.flip(vert_data[vert_key])[np.flip(vert_data['vert_z'])>=sfc_data['sfc_z']], 0, sfc_data[sfc_key])
        sb_dict['z'] = sb_dict['z'] - sb_dict['z'][0]
        
        # Interpolates data
        dz = 250 
        soundingtop_hght = sb_dict['z'][-1]
        toplvl      = int(soundingtop_hght/dz)*dz
        numlvls     = int(toplvl/dz)
        interp_lvls = np.linspace(0,toplvl,numlvls+1)

         # prepare new dicts 
        keys = ['T', 'Td', 'rh', 'u', 'v', 'z', 'p']
        units_list = ['degC', 'degC', 'percent', 'kt', 'kt', 'm', 'hPa']
        interp_dict = {}
        zeros_dict  = {}
        clean_data  = {}
        
        surface_height = sfc_data['sfc_z']

        # create dict of clean data 
        for key in keys:
            interp_dict[key] = (interpolate.interp1d(sb_dict['z'], sb_dict[key]))
            zeros_dict[key]  = np.zeros((len(interp_lvls)))
            for zeros_arr in zeros_dict.values():
                zeros_dict[key][0] = sb_dict[key][0]
            for i in range(1,len(zeros_dict[key]),1):
                zeros_dict[key][i] = interp_dict[key](dz*i)
                
        for i, unit, key in zip(range(0, len(units_list)), units_list, keys):
            clean_data[key] = zeros_dict[key]*units(unit)
        #clean_data['zAGL'] = clean_data['z'] + surface_height*units.m
        clean_data['site_info'] = {
                    'site-id'   : 'no-site-id',
                    'site-name' : 'no-site-name',
                    'site-lctn' : 'no-site-location',
                    'site-latlon' : [latlon[0], latlon[1]],
                    'site-elv'  : surface_height,
                    'source'    : f'MODEL {str.upper(dtype)}',
                    'model'     : source,
                    'fcst-hour' : 'F00',
                    'run-time'  : latlon_data['data_time'],
                    'valid-time': latlon_data['data_time'],
                    'box_area'  : f'{box_avg_size}° BOX AVG'}


        print('> COMPLETE --------')
        elapsed_time = time.time() - st
        print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        
        return clean_data
    
    clean_data = parse_data(raw_data, latlon, box_avg_size)
    print(f"> SUMMARY: {clean_data['site_info']['run-time'][3]}Z {clean_data['site_info']['model']} {clean_data['site_info']['fcst-hour']} for {clean_data['site_info']['site-latlon']} at {clean_data['site_info']['valid-time'][1]}-{clean_data['site_info']['valid-time'][2]}-{clean_data['site_info']['valid-time'][0]}-{clean_data['site_info']['valid-time'][3]}Z")
    warnings.filterwarnings("ignore")
        
    if hush == False:
        sounding_params(clean_data).print_vals()
            
    return clean_data
    #########################################################################################################
    
#########################################################################################################   
    
    
    
    
    
    
    
###############
# OBSERVED DATA 
#########################################################################

def get_obs_data(station, year, month, day, hour, hush=False):
    
    # record process time
    st = time.time()
    
    r"""
       Return a ``dict`` of 'cleaned up' observed profile data

       :param station: a three digit RAOB identifier (such as: 'DTX') or 11 digit IGRAv2 identifier (such as: 'GMM00010393')
       :type station: str, required
       :param year: launch year
       :type year: str, required
       :param month: launch month
       :type month: str, required
       :param day: launch day
       :type day: str, required
       :param hour: launch hour
       :type hour: str, required
       :param hush: whether to 'hush' a read-out of thermodynamic and kinematic parameters when getting a data.
       :type hush: bool, optional, default is `False`
       :return: clean_data, a dict of ready-to-use vertical profile data including pressure, height, temperature, dewpoint, u-wind, v-wind, & model information
       :rtype: dict
    """
    
    
    print(f'> OBSERVED DATA ACCESS FUNCTION --\n-----------------------------------')
    
    station = str.upper(station)
    # get station lists from SounderPy GitHub Repo
    RAOB_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/RAOB-STATIONS.txt', 
                                skiprows=7, skipinitialspace = True)
    IGRA_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/IGRA-STATIONS.txt', 
                                skiprows=7, skipinitialspace = True)
    
    got_data = False
    
    # set up siphon API call for raob data -- if station ID is found in RAOB_STATIONS, it is
    # a RAOB ID and siphon UW or ISU must be used to get data
    if len(station) == 11:
        search_for = 'igra'
    else:
        search_for = 'raob'
        
    
    ### RAOB OBSERVATIONS ###
    #########################################################################################################
    if search_for == 'raob':
        # try this process 10 times, sometimes requests fail due to temporary 404 errors
        for i in range(1, 11):
            try: 
                # try UW data request
                df = WyomingUpperAir.request_data(datetime(int(year), int(month), int(day), int(hour)), station)
                got_data = True
                if got_data == True:
                    print(f'> PROFILE FOUND: {station} on {month}/{day}/{year} at {hour}z | From UW')
                    break
            except:  
                got_data = False
                pass

        # search through RAOB sites list with provided RAOB ID, first try ICAO ID, then WMO ID
        if got_data == True:
            try:
                station = RAOB_STATIONS['ICAO'][np.where(RAOB_STATIONS['ICAO'].str.contains(station, na=False, case=True))[0]].values[0].strip()
                name_idx = 'ICAO'
            except:
                try:
                    station = RAOB_STATIONS['WMO'][np.where(RAOB_STATIONS['WMO']==int(station))[0]].values[0]
                    name_idx = 'WMO'
                except:
                    raise ValueError(f'ICAO or WMO identifier not found, please make sure you provided the correct RAOB ID. If you think this is an error' +
                                      'contact the author: https://kylejgillett.github.io/sounderpy/about.html#about-the-author')
                    pass
                pass
            
            # begin loading data 
            # create dict of data
            new_keys = ['p', 'z', 'T', 'Td', 'u', 'v']
            old_keys = ['pressure', 'height', 'temperature', 'dewpoint', 'u_wind', 'v_wind'] # 'latitude', 'longitude']
            units_list = ['hPa', 'meter', 'degC', 'degC', 'kt', 'kt']
            clean_data = {}
            non_dups = np.concatenate(([True], np.diff(df.to_dict('list')['pressure']) != 0))
            for old_key, new_key, unit in zip (old_keys, new_keys, units_list):
                clean_data[new_key] = np.array(df.to_dict('list')[old_key])[non_dups]*units(unit)
            clean_data['site_info'] = {
                'site-id'   : RAOB_STATIONS[RAOB_STATIONS[name_idx]==station][name_idx].values[0],
                'site-name' : RAOB_STATIONS[RAOB_STATIONS[name_idx]==station]['NAME'].values[0],
                'site-lctn' : RAOB_STATIONS[RAOB_STATIONS[name_idx]==station]['LOC'].values[0],
                'site-latlon' : get_latlon('raob', str(station)),
                'site-elv'  : RAOB_STATIONS[RAOB_STATIONS[name_idx]==station]['EL(m)'].values[0],
                'source'    : 'RAOB OBSERVED PROFILE',
                'model'     : 'no-model',
                'fcst-hour' : 'no-fcst-hour',
                'run-time'  : ['none', 'none', 'none', 'none'],
                'valid-time': [year, month, day, hour]}
            
            try:
                # trim data to 98hPa and below for less process time 
                slc = (len(clean_data['p']) - np.where(clean_data['p']<=98.*units('hPa'))[0][0])
                for key in new_keys:
                    clean_data[key] = clean_data[key][:-slc]
            except:
                pass
        else:
            raise ValueError(f'Wyoming Upper Air Archive connection failed -- ensure you have the correct dates and corresponding station identifier\n' +
                             f'There is likely no available data for station {station} on {month}/{day}/{year} at {hour}z')
    #########################################################################################################
    
    

    ### IGRAv2 OBSERVATIONS ###    
    #########################################################################################################     
    elif search_for =='igra': 
        for i in range(1, 3):
            try: 
                # try siphon IGRA request 
                df = IGRAUpperAir.request_data(datetime(int(year), int(month), int(day), int(hour)), station)
                got_data = True
                if got_data == True:
                    print(f'> PROFILE FOUND: {station} on {month}/{day}/{year} at {hour}z | From IGRAv2')
                    break
            except:
                got_data = False
                pass
        
        # if data is found, parse data and create a dict of clean data
        if got_data == True:
            station = IGRA_STATIONS['ID'][np.where(IGRA_STATIONS['ID'].str.contains(station, na=False, case=True))[0]].values[0].strip()
            
            # create dict of data
            head = df[1]
            df = df[0]
            new_keys = ['p', 'z', 'T', 'Td', 'u', 'v']
            old_keys = ['pressure', 'height', 'temperature', 'dewpoint', 'u_wind', 'v_wind'] # 'latitude', 'longitude']
            units_list = ['hPa', 'meter', 'degC', 'degC', 'kt', 'kt']
            clean_data = {}
            zflag=np.array(df['zflag'])
            pflag=np.array(df['pflag'])
            tflag=np.array(df['tflag'])
            for old_key, new_key, unit in zip (old_keys, new_keys, units_list):
                clean_data[new_key] = np.array(df.to_dict('list')[old_key])[zflag+pflag+tflag>=4]*units(unit)
            clean_data['site_info'] = {
                    'site-id'   : IGRA_STATIONS[IGRA_STATIONS['ID']==station]['ID'].str.strip().values[0],
                    'site-name' : IGRA_STATIONS[IGRA_STATIONS['ID']==station]['NAME'].str.strip().values[0],
                    'site-lctn' : '',
                    'site-latlon' : get_latlon('igra', station),
                    'site-elv'  : IGRA_STATIONS[IGRA_STATIONS['ID']==station]['EL(m)'].values[0],
                    'source'    : 'RAOB OBSERVED PROFILE',
                    'model'     : 'no-model',
                    'fcst-hour' : 'no-fcst-hour',
                    'run-time'  : ['none', 'none', 'none', 'none'],
                    'valid-time': [year, month, day, hour]}
            # correct u & v units
            clean_data['u'] = clean_data['u']*1.94384
            clean_data['v'] = clean_data['v']*1.94384  
        else:
            raise ValueError(f'IGRAv2 Dataset connection failed -- ensure you have the correct dates and corresponding station identifier\n' +
                    f'There is likely no available data for station {station} on {month}/{day}/{year} at {hour}z')
    #########################################################################################################      
    
    print('> COMPLETE --------')
    elapsed_time = time.time() - st
    print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print(f"> SUMMARY: {clean_data['site_info']['valid-time'][3]}Z Launch for {clean_data['site_info']['site-id']}, {clean_data['site_info']['site-name']} at {clean_data['site_info']['valid-time'][1]}-{clean_data['site_info']['valid-time'][2]}-{clean_data['site_info']['valid-time'][0]}-{clean_data['site_info']['valid-time'][3]}Z")
    warnings.filterwarnings("ignore")
    if hush == False:
           sounding_params(clean_data).print_vals()
    
    return clean_data 
            
#########################################################################################################

    

    
    
    
    
    
    

#############
# BUFKIT DATA 
#########################################################################

def get_bufkit_data(model, station, fcst_hour, run_year=None, run_month=None, run_day=None, run_hour=None, 
                   hush=False):
    
    # record process time
    st = time.time()
    
    
    r"""Get BUFKIT forecast model vertical profile data
       Return a ``dict`` of 'cleaned up' model forecast data from a given model, for a given BUFKIT site identifier, forecast hour, & model-run-date

       :param model: the requested model to use (such as hrrr, nam, gfs, etc)
       :type model: str, required
       :param station: a 3-4 digit BUFKIT site identifier
       :type station: str, required
       :param fcst_hour: valid forecast hour
       :type fcst_hour: int, required
       :param year: valid year
       :type year: str, required
       :param month: valid month
       :type month: str, required
       :param day: valid day
       :type day: str, required
       :param hour: valid hour
       :type hour: str, required
       :param hush: whether to 'hush' a read-out of thermodynamic and kinematic parameters when getting a data.
       :type hush: bool, optional, default is `False`
       :return: clean_data, a dict of ready-to-use vertical profile data including pressure, height, temperature, dewpoint, u-wind, v-wind, & model information
       :rtype: dict
    """
    
    
    print(f'> BUFKIT DATA ACCESS FUNCTION --\n---------------------------------')
    
    # make sure variables are in the correct case
    model   = str.lower(model)
    station = str.upper(station)

    # remove '#' for URL
    if '#' in station: 
        url_station = station.replace('#', '%23')
    else: 
        url_station = station
    
    # GET MOST-RECENT RUNS FROM PSU SERVERS 
    # if date variables (year, month, day) are not given, the user has 'selected' a most
    # recent forecast run, get that from PSU
    if run_year == None:
        if model not in ['gfs', 'nam', 'namnest', 'rap', 'hrrr', 'sref', 'hiresw']:
            raise ValueError(f"{model} is not a valid model option. Valid models include ['GFS', 'NAM', 'NAMNEST', 'RAP', 'HRRR', 'SREF', 'HIRESW']")
        if model == 'gfs':
            model3 = 'gfs3' 
        else:
            model3 = model
        data_conn = f'http://www.meteo.psu.edu/bufkit/data/{model.upper()}/{model3}_{url_station.lower()}.buf'
     
    
    # GET ARCHIVE DATA FROM THE IEM SERVERS. CORRECT GFS & NAM MODEL NAMES
    # if date variables (year, month, day) are given, the user has 'selected' a 
    # archived forecast for the given date 
    else:
        if model not in ['gfs', 'nam', 'namnest', 'rap', 'hrrr']:
            raise ValueError(f"{model} is not a valid model option. Valid models include ['GFS', 'NAM', 'NAMNEST', 'RAP', 'HRRR']")
        if model == 'namnest':
            model = 'nam4km'
        if model == 'gfs':
            model3 = 'gfs3' 
        else:
            model3 = model
        data_conn = f'https://mtarchive.geol.iastate.edu/{run_year}/{run_month}/{run_day}/bufkit/{run_hour}/{model}/{model3}_{url_station.lower()}.buf'  


    # Check to make sure the user-defined site ID is a valid bufkit site before continuing 
    try:  
        # GET BUFKIT STATIONS LISTING FROM SOUNDERPY GITHUB REPO
        BUFKIT_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/BUFKIT-STATIONS-MASTER.txt', 
                                      skiprows=7, skipinitialspace = True)
        # ATTEMPT TO FIND THE STATION
        station = BUFKIT_STATIONS['ID'][np.where(BUFKIT_STATIONS['ID'].str.contains(station, na=False, case=True))[0]].values[0]
        worked = True
    except:
        worked = False
        pass
    
    if worked == False:
        raise ValueError(f"{station} does not appear to be a valid BUFKIT site identifier. A map of valid BUFKIT stations can be found here from Penn State: http://www.meteo.psu.edu/bufkit/CONUS_RAP_00.html")
        
    # GET BUFKIT FILE 
    # CONVERT LINES OF BYTES TO STRINGS 
    buf_file = urlopen(data_conn)
    buf_file = [str(line).replace("b'", "").replace("\\r\\n'", "") for line in buf_file]

    # CREATE TEMP DATA
    tmp_data, sounding_headers, derived_headers = [], '', ''
    recordSounding = False
    
    # SET UP DATE / TIME OBJECTS FROM THE BUFKIT FILE
    run_time = buf_file[4][buf_file[4].index('TIME') + 7:(buf_file[4].index('TIME')+9)+9]
    run_dt = datetime(int(f'20{run_time[0:2]}'), int(run_time[2:4]), int(run_time[4:6]), int(run_time[7:9])) 
    fct_dt = run_dt + timedelta(hours = fcst_hour)
    hr_deltas = {
         'gfs':[1,180], 'hrrr':[1,48],
         'rap':[1,51],  'nam':[1,48],
         'namnest':[1,60],  'nam4km':[1,60],
         'sref':[1,84],     'hiresw':[1,48]}
    stp_dt = fct_dt + timedelta(hours = hr_deltas[model][0])
    
    if hr_deltas[model][1] < fcst_hour:
            raise ValueError(f'Invalid forecast hour -- BUFKIT only stores up to F0{hr_deltas[model][1]} for the {str.upper(model)}')
    
    # Loop over each line in data file
    for line in buf_file:
        # Find start of sounding data
        if f'TIME = {fct_dt.strftime("%Y")[2:4]}{fct_dt.strftime("%m")}{fct_dt.strftime("%d")}/{fct_dt.strftime("%H")}00' in line:
            recordSounding=True  
        if 'SNPARM' in line:
            sounding_headers=line[line.index('=')+2:].replace(' ', '').split(';')
        if 'STNPRM' in line:
            derived_headers=line[line.index('=')+2:].replace(' ', '').split(';')
        # Append data line to temp data list
        if recordSounding:
            tmp_data.append(line)
        # Break out of loop when end key reached
        if f'TIME = {stp_dt.strftime("%Y")[2:4]}{stp_dt.strftime("%m")}{stp_dt.strftime("%d")}/{stp_dt.strftime("%H")}00' in line:
            tmp_data.pop(-1)
            break
        elif 'YYMMDD/HHMM' in line:
            tmp_data.pop(-1)
            break
    
    # SET UP UTILS
    station_headers=['STID', 'STNM', 'TIME', 'SLAT', 'SLON', 'SELV', 'STIM']
    tmp_str=''
    recordStationInfo, recordDerivedQty, recordSoundingQty = False, False, True
    station_metadata, derived_data, sounding_data = [], [], []

    
    # Check if the last line is blank
    if tmp_data[-1].strip() != '':
        # Add a blank line at the end
        tmp_data.append('')
    
    # PARSE THROUGH FILE, SPLIT LINES AND RECORD DATA WE WANT TO KEEP
    for line in tmp_data:
        # Check for station infromation
        if recordStationInfo and line=='':
            # Break values up to only be seperated by one whitespace
            station_info=(tmp_str.replace(' = ', ' '))
            # Split values into list
            station_info=station_info.split(' ')
            # Remove label values
            station_info=[x for x in station_info if x not in station_headers]
            while '' in station_info:
                station_info.remove('')
            # Add to main list
            station_metadata.append(station_info)
            # Reset temp vars
            tmp_str=''
            recordStationInfo=False
        if any(var in line for var in station_headers):
            recordStationInfo=True
            tmp_str+=(' ' + line)
        # Check for derived sounding quantities
        if recordDerivedQty==True and line=='':
            # Break values up to only be seperated by one whitespace
            derived_qty=(tmp_str.replace(' = ', ' '))
            # Split values into list
            derived_qty=derived_qty.split(' ')
            # Remove non-numeric values
            derived_qty=[x for x in derived_qty if x not in derived_headers]
            while '' in derived_qty:
                derived_qty.remove('')
            # Add to main list
            derived_data.append(derived_qty)
            # Reset temp vars
            tmp_str=''
            recordDerivedQty=False
        if any(var in line for var in derived_headers):
            recordDerivedQty=True
            tmp_str+=(' ' + line)
        # Check for sounding quantities
        if any(var in line for var in sounding_headers):
            recordSoundingQty=True
        if recordSoundingQty and line=='':
            level_list=[]
            # Split data string into values
            data_list=tmp_str.split(' ')
            # Remove empty indices
            while '' in data_list:
                data_list.remove('')
            # Break data up into pressure levels
            for i in range(0, len(data_list), len(sounding_headers)):
                level_list.append(data_list[i:len(sounding_headers)+i])
        elif recordSoundingQty:
            if any(var in line for var in sounding_headers)==False:
                tmp_str+=(' ' + line)
        
    if 'level_list' not in locals():
        raise ValueError(f"The data for the model and forecast hour you requested, from the model-run date you requested, at the BUFKIT site you requested, does not appear to exist\n" +
                         f"Please try a different model, forecast hour, run date or BUFKIT site")
                
    # CREATE BLANK LISTS 
    p = []
    z = []
    T = []
    Td = []
    ws = []
    wd = []

    
    # APPEND LISTS WITH DATA FROM BUFKIT FILES
    if model in ['gfs']:
        for i in range(0, len(level_list)):
            p.append(float(level_list[i][0]))
            z.append(float(level_list[i][8]))
            T.append(float(level_list[i][1]))
            Td.append(float(level_list[i][3]))
            ws.append(float(level_list[i][6]))
            wd.append(float(level_list[i][5]))  
    else:
        for i in range(0, len(level_list)):
            p.append(float(level_list[i][0]))
            z.append(float(level_list[i][9]))
            T.append(float(level_list[i][1]))
            Td.append(float(level_list[i][3]))
            ws.append(float(level_list[i][6]))
            wd.append(float(level_list[i][5])) 
    
    
    # CALCULATE U AND V COMPONENTS 
    u = list(mpcalc.wind_components(ws*units.kts, wd*units.degrees)[0].m)
    v = list(mpcalc.wind_components(ws*units.kts, wd*units.degrees)[1].m)
    
    
    # DEFINE find_nearest() FUNCTION 
    def find_nearest(array, value):
        array = np.asarray(array)
        nearest_idx = (np.abs(array - value)).argmin()
        return nearest_idx
    
    
    # FIND P LEVEL AT 50hPa
    hPa50 = find_nearest(p, 50)

    
    # ARRANGE DATA IN CLEAN_DATA DICT
    clean_data = {}
    lists = [p[0:hPa50], z[0:hPa50], T[0:hPa50], Td[0:hPa50], u[0:hPa50], v[0:hPa50]]
    keys = ['p', 'z', 'T', 'Td', 'u', 'v']
    units_list = ['hPa', 'meter', 'degC', 'degC', 'kt', 'kt']
    for key, lst, unit in zip(keys, lists, units_list):
        clean_data[key] = lst*units(unit) 
    
    # create dict of data
    clean_data['site_info'] = {
                'site-id'   : BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['ID'].str.strip().values[0],
                'site-name' : BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['NAME'].str.strip().values[0],
                'site-lctn' : BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['LOC'].str.strip().values[0],
                'site-latlon' : [BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['LAT'].values[0],
                                 BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['LON'].values[0]],
                'site-elv'  : BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['EL(m)'].values[0],
                'source'    : 'BUFKIT FORECAST PROFILE',
                'model'     : str.upper(model),
                'fcst-hour' : f'F0{fcst_hour}',
                'run-time'  : [run_dt.strftime("%Y"), run_dt.strftime("%m"), run_dt.strftime("%d"), run_dt.strftime("%H")],
                'valid-time': [fct_dt.strftime("%Y"), fct_dt.strftime("%m"), fct_dt.strftime("%d"), fct_dt.strftime("%H")]} 
    
    
    print('> COMPLETE --------')
    elapsed_time = time.time() - st
    print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print(f"> SUMMARY: {clean_data['site_info']['run-time'][3]}Z {clean_data['site_info']['model']} {clean_data['site_info']['fcst-hour']} for {clean_data['site_info']['site-id']}, {clean_data['site_info']['site-name']} at {clean_data['site_info']['valid-time'][1]}-{clean_data['site_info']['valid-time'][2]}-{clean_data['site_info']['valid-time'][0]}-{clean_data['site_info']['valid-time'][3]}Z")
    warnings.filterwarnings("ignore")

    def clean_dewpoints(td):
        for i in range(len(td)):
            if td[i] < -130 * td[i].units: td[i] = -130 * td[i].units

    clean_dewpoints(clean_data['Td'])


    if hush == False:
            sounding_params(clean_data).print_vals()
    
    return clean_data
#########################################################################################################
    
    
    

    
    
    








############
# ACARS DATA 
#########################################################################

# define class
class acars_data:
    
    """
    - NOTE: this is a Python ``Class``, not a function like the tools above. 
       - This ``Class`` sets up a 'connection' to the ACARS data dataset. 
       - After setting up a 'connection' to the data, you can search for available profiles using the class's function, ``.list_profiles()``
       - Then you may select one of the listed profiles and use it as an argument for the class's function, ``.get_profile()``. See below.
       
       :param year: observation year
       :type year: str, required
       :param month: observation month
       :type month: str, required
       :param day: observation day
       :type day: str, required
       :param hour: observation hour
       :type hour: str, required
    """
        
    
    # init 
    def __init__(self, year, month, day, hour):
        self.year = year
        self.hour = hour
        self.month = month
        self.day = day
        self.hour = hour
        
    ### LIST PROFILES ###
    #########################################################################################################
    def list_profiles(self):
        '''
        Return a list of strings that represents ACARS profiles for a given date and hour.
        '''
        
        st = time.time()
        print(f'> LIST ACARS PROFILES FUNCTION --\n---------------------------------')

        # SET UP OU DIRECTORY REF
        # SEARCH FOR DIRECTORY FOR THE USER-SPECIFIED DATE
        data_dir = f'https://sharp.weather.ou.edu//soundings//acars//{self.year}//{self.month}//{self.day}//{self.hour}'

        # ACCESS THE RAW WEBSITE HTML & FIND THE ID_TIME KEYS 
        print(f"> AVAILABLE ACARS PROFILES FOR {self.year}-{self.month}-{self.day} {self.hour}Z...")
        # SET UP BEAUTIFUL SOUP TO PARSE HTML 
        # THIS WORKS AS A SORT OF JERRY-RIGGED WAY
        # TO REVEAL ALL AVAILABLE ACARS PROFILES
        # FOR A GIVEN DATE/TIME
        body = urlopen(data_dir).read().decode("utf-8")
        soup = bs4.BeautifulSoup(body, features="html.parser")

        # ADD PROFILES TO A LIST
        profiles_list = []
        for link in soup.select('a[href$=".txt"]'):
            profiles_list.append(link.get("href")[0:8]) 
        
        
        print('> COMPLETE --------')
        elapsed_time = time.time() - st
        print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

        return profiles_list
    #########################################################################################################


    ### GET PROFILE DATA ###
    #########################################################################################################
    def get_profile(self, acars_profile, hush=False):
        
        '''
        Return a ``dict`` of 'cleaned up' ACARS observation profile data. Do so by selecting one of the profile string "IDs" listed by ``list_profiles()`` and pasting it as an argument in ``get_profile()``

        :param profile: profile "ID"
        :type profile: str, required
        :param hush: whether to 'hush' a read-out of thermodynamic and kinematic parameters when getting a data.
        :type hush: bool, optional, default is `False`
      
        '''
        
        st = time.time()
        print(f'> ACARS DATA ACCESS FUNCTION --\n---------------------------------')
        
        # SET UP OU DIR REF TO THE SPECIFIC PROFILE
        profile_url    = f'https://sharp.weather.ou.edu//soundings//acars//{self.year}//{self.month}//{self.day}//{self.hour}//{acars_profile}.txt'
        
        # SEPERATE DATA BETWEEN HEADER AND ACTUAL DATA 
        try:
            data   = loadtxt(urlopen(profile_url).readlines()[6:-1], dtype='str', comments="%", unpack=True)
            header = loadtxt(urlopen(profile_url).readlines()[0:3], dtype='str', comments="%", unpack=True)
        except HTTPError as err:
            if err.code == 404:
                sys.exit('! ERROR ! -- Invalid profile, try again with a valid profile (ex: BNA_2320)')
            else:
                raise
        
        # PARSE DATE INFO FROM OU FILE
        year  = f'20{header[1][0:2]}'
        month = header[1][2:4]
        day   = header[1][4:6]
        hour  = f'{header[1][7:9]}:{header[1][9:11]}'

        # PARSE PROFILE DATA FROM OU FILE IN DICT
        new_keys = ['p', 'z', 'T', 'Td', 'u', 'v']
        units_list = ['hPa', 'meter', 'degC', 'degC']
        clean_data = {}
        for new_key, idx, unit in zip (new_keys, range(0,4), units_list):
            clean_data[new_key] = np.array([float(ele) for ele in [ele[0:-1] for ele in data[idx]]])*units(unit)
            
        clean_data['u'], clean_data['v'] = mpcalc.wind_components([float(ele) for ele in [ele[0:-1] for ele in data[5]]]*units.kts,
                                                             [float(ele) for ele in [ele[0:-1] for ele in data[4]]]*units.deg)
        
        # GET AIRPORT INFO FROM GITHUB AIRPORTS.CSV
        airports_csv = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/AIRPORTS.csv',
                skiprows=7, skipinitialspace = True)
        where = [np.where(airports_csv['IATA'].str.contains(header[0], na=False, case=True))[0]][0][0]
        
        # ADD AIRPORT DATA INTO DICT
        keys = ['Name', 'City', 'Country', 'Latitude', 'Longitude', 'Altitude']
        airport_info = []
        for key in keys:
            airport_info.append(airports_csv[key][where])
        clean_data['site_info'] = {
                        'site-id'   : header[0],
                        'site-name' : airport_info[0],
                        'site-lctn' : airport_info[2],
                        'site-latlon' : [np.round(airport_info[3],2), np.round(airport_info[4],2)],
                        'site-elv'  : str(int(airport_info[5])),
                        'source'    : 'ACARS OBSERVED AIRCRAFT PROFILE',
                        'model'     : 'no-model',
                        'fcst-hour' : 'no-fcst-hour',
                        'run-time'  : ['none', 'none', 'none', 'none'],
                        'valid-time': [f'20{header[1][0:2]}', header[1][2:4], header[1][4:6], f'{header[1][7:9]}:{header[1][9:11]}']}

        print('> COMPLETE --------')
        elapsed_time = time.time() - st
        print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        print(f"> SUMMARY: {clean_data['site_info']['valid-time'][3]}Z Flight from {clean_data['site_info']['site-id']}, {clean_data['site_info']['site-name']} at {clean_data['site_info']['valid-time'][1]}-{clean_data['site_info']['valid-time'][2]}-{clean_data['site_info']['valid-time'][0]}-{clean_data['site_info']['valid-time'][3]}Z")
        warnings.filterwarnings("ignore")
        if hush == False:
            sounding_params(clean_data).print_vals()
        
        return clean_data
    #########################################################################################################
    
#########################################################################################################










#####################
# PYART VAD FUNCTION
#########################################################################
def pyart_radar_profile(nexrad_site, scan_dt, from_file=False, data_file='none'):


    '''
    Radar data loader and VWP creator function -- powered by PyArt 
    (https://arm-doe.github.io/pyart/)

    :param nexrad_site: station ID (``'KDTX'``)
    :type nexrad_site: str, required
    :param scan_dt: the date and time of the requested scan (``datetime(2021, 12, 11, 4, 24)``)
    :type scan_dt: datetime obj, required
    :param from_file: whether or not to search the NEXRAD AWS database or look for a local file, default is False
    :type from_file: bool, optional
    :param data_file: the filename of the local radar file to use
    :type data_file: str, optional

    returns a SounderPy 'vad_data' Python dict.

    """

    '''

    st = time.time()

    print(f'> PYART RADAR DATA RETRIEVAL FUNCTION --\n-----------------------------------------')
    print('! NOTE: THIS FUNCTION IS CONSIDERED STILL IN DEVELOPMENT')
    
    if from_file == False:
        class ScanNotFoundError(Exception):
            def __init__(self, message="Scan not found."):
                self.message = message
                super().__init__(self.message)


        # SET UP AWS CONNECTION
        conn = nexradaws.NexradAwsInterface()
        try:
            scans = conn.get_avail_scans_in_range((scan_dt - timedelta(hours=1)),(scan_dt + timedelta(hours=1)), nexrad_site)
        except TypeError:
            raise ScanNotFoundError(f"Could not find the requested scan [{scan_dt} @ {nexrad_site}] in NEXRAD AWS dataset. This may be because the scan does not exist, or perhaps"+
                                    f" there is an internal AWS error. You could try downloading the file here: https://www.ncdc.noaa.gov/nexradinv/")
            pass

        datetime_scans = []
        for i in range(len(scans)):
            datetime_scans.append(datetime(int(str(scans[i]).split('- ')[1][20:24]), int(str(scans[i]).split('- ')[1][24:26]), int(str(scans[i]).split('- ')[1][26:28]), int(str(scans[i]).split('- ')[1][29:31]), int(str(scans[i]).split('- ')[1][31:33])))
            scan = str(scans[find_nearest(datetime_scans,scan_dt)]).split('- ')[1][0:-1]

        print(f" + Found radar file: {scan}")

        radar_file = pyart.io.read_nexrad_archive("s3://noaa-nexrad-level2/"+str(scan), station=nexrad_site)  
        
    else: 
        radar_file = pyart.io.read(data_file)
        scan = f'{data_file[4:8]}/{data_file[8:10]}/{data_file[10:12]}/{data_file[0:4]}/{data_file}'


      
    # GET TIME AND DATE OF FILE FROM SCAN
    rad_time = scan.split('/')[4].split('_')[1]
    date = scan.split('/')[4].split('_')[0][4:]
    timelist = []
    for i in range(0, len(rad_time), 2):
        timelist.append(rad_time[i:i+2])
    datelist = []
    for i in range(0, len(date), 2):
        datelist.append(date[i:i+2]) 
        
    # CREATE GATE FILTER
    warnings.filterwarnings("ignore")
    
    gatefilter = pyart.filters.GateFilter(radar_file)
    gatefilter.exclude_transition()
    gatefilter.exclude_invalid("velocity")
    gatefilter.exclude_invalid("reflectivity")
    gatefilter.exclude_outside("reflectivity", 0, 80)

    # PERFORM DEALIASING OF RADAR FILE
    dealias_data = pyart.correct.dealias_region_based(radar_file, gatefilter=gatefilter)
    try:
        radar_file.add_field("corrected_velocity", dealias_data)
    except ValueError:
        pass
    
    # WRITE CFRADIAL FILE
    pyart.io.write_cfradial(f"CF-RAD_{scan.split('/')[4]}.nc", radar_file, format='NETCDF4')

    # READ THE CFRADIAL FILE
    cfrad_file = pyart.io.read_cfradial(f"CF-RAD_{scan.split('/')[4]}.nc")    
    print(f" + CF-Radial file created: 'CF-RAD_{scan.split('/')[4]}.nc'")
    
    # determine height levels
    zlevels = np.arange(0, 9100, 100) 
    u_allsweeps = []
    v_allsweeps = []

    
    import contextlib
    from io import StringIO

    # Redirect stdout to a StringIO object
    with contextlib.redirect_stdout(StringIO()):
    
        # for radial sweep, create a PyArt VAD 
        for idx in range(cfrad_file.nsweeps):
            radar_1sweep = cfrad_file.extract_sweeps([idx])
            vad = pyart.retrieve.vad_browning(
                radar_1sweep, "corrected_velocity", z_want=zlevels)
            u_allsweeps.append(vad.u_wind)
            v_allsweeps.append(vad.v_wind)    
    
    # LOAD A LIST OF NEXRAD SITE INFORMATION
    nexrad_sites = pd.read_csv('https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/NEXRAD_SITES.txt', skiprows=3, skipinitialspace = True)

    # CREATE A PYTHON DICTIONARY OF VAD DATA AND SITE METADATA
    vad_data = {
        'u': np.nanmean(np.array(u_allsweeps), axis=0)* 1.944,
        'v': np.nanmean(np.array(v_allsweeps), axis=0)* 1.944,
        'z': zlevels,
        'site_info':  {'site-id': radar_file.metadata['instrument_name'],
                       'site-name': str(nexrad_sites[nexrad_sites['ID']==radar_file.metadata['instrument_name']]['NAME'].values[0] + ', ' + nexrad_sites[nexrad_sites['ID']==radar_file.metadata['instrument_name']]['STATE'].values[0]),
                       'site-latlon': [np.round(radar_file.latitude['data'][0], 2), np.round(radar_file.longitude['data'][0], 2)],
                       'elevation': np.round(nexrad_sites[nexrad_sites['ID']==radar_file.metadata['instrument_name']]['ELV'].values[0]/3.281, 2),
                       'vcp': str(radar_file.metadata['vcp_pattern']),
                       'source': 'VAD VWP',
                       'valid-time': [str(datelist[0]+datelist[1]), datelist[2], datelist[3], str(timelist[0]+':'+timelist[1])]}
        }
    

    print('> COMPLETE --------')
    elapsed_time = time.time() - st
    print('> RUNTIME:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))


    return vad_data
#########################################################################    








#################
# DROPSONDE DATA
#########################################################################
class dropsonde_data:
    
    """
    - NOTE: this is a Python ``Class``, not a function like most of the tools above. This class works very similarly to the ``acars_data()`` class
       - This ``Class`` sets up a 'connection' to recent recon dropsondes 
       - Receive a list of available dropsondes ``.list_drops()``
       - Then you may select one of the listed dropsonde 'IDs' and use it as an argument for the class's function, ``.get_drop()``.

       (C) Kyle J Gillett, 2024

       Acknowledgements: Tomer Burg, TroPycal
    """
        
    #################################################################
    ### BASE DATA LOADER FUNCTION ###
    ### load dropsondes and hdobs to return detailed mission data
    ### and dropsonde data for given missions
    #################################################################
    #################################################################  
    
    def load_data(self, hours=24):
        
        # a dict of urls and files to reference later
        file_lists = {
            'hdobs': [f'https://www.nhc.noaa.gov/archive/recon/{datetime.utcnow().year}/AHONT1/', []],
            'dropsondes':  [f'https://www.nhc.noaa.gov/archive/recon/{datetime.utcnow().year}/REPNT3/', []],
        }


        # declare time window to search for dropsonde/hdob files
        start_time_request = datetime.utcnow() - dt.timedelta(hours=hours)
        start_time = datetime.utcnow() - dt.timedelta(hours=hours + 12)

        # for dropsonde and hdobs, get the content from the file URL
        # and create a list of valid files 
        for key in file_lists.keys():
            page = requests.get(file_lists[key][0]).text
            content = page.split("\n")
            file_list = []
            for line in content:
                if ".txt" in line:
                    file_list.append(
                        ((line.split('txt">')[1]).split("</a>")[0]).split("."))
            del content
            file_list = sorted([i for i in file_list if datetime.strptime(
                i[1][:10], '%Y%m%d%H') >= start_time], key=lambda x: x[1])
            file_lists[key][1] = [file_lists[key][0] + '.'.join(l) for l in file_list]

            
        # load active missions, read hdobs content and build a mission-id
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        missions = {}
        for file in file_lists['hdobs'][1]:

            # get hdobs content
            response = http.request('GET', file)
            content = response.data.decode('utf-8')
            content_split = content.split("\n")

            # build mission-ID and build `missions` dict of all data details
            try:
                mission_id = '-'.join(
                    (content_split[3].replace("  ", " ")).split(" ")[:3])
                if mission_id not in missions:
                    missions[mission_id] = {
                        'aircraft': mission_id.split("-")[0],
                        'storm_name': mission_id.split("-")[2],
                        'dropsondes': [], 
                        'hdobs': tropycal.recon.tools.decode_hdob(content),
                        'drop_files': []
                    }
            except:
                pass
        
    
        # load dropsondes from files
        for file in file_lists['dropsondes'][1]:
            # Retrieve content
            response = http.request('GET', file)
            content = response.data.decode('utf-8')
            content_split = content.split("\n")
            
            # build dropsonde mission IDs and decode dropsondes 
            mission_id = ['-'.join(i.split("61616 ")[1].replace("  ", " ").split(" ")[:3])
                          for i in content_split if i[:5] == "61616"][0]
            time = datetime.strptime((file.split('.')[-2])[:8], '%Y%m%d')
            try:
                blank, data = tropycal.recon.tools.decode_dropsonde(content, time)
            except:
                print('decode dropsonde error')
                continue
            # if dropsonde missions are also in hdobs dropsondes, 
            # save the dropsonde data and dropsonde files to the missions dict
            if mission_id in missions.keys():
                missions[mission_id]['dropsondes'].append(data)
                missions[mission_id]['drop_files'].append(file)
            
        # sometimes dropsonde times don't match the "true" time of the obs,
        # the time listed in the file URL is accurate though, so here is a 
        # check of the drop time being the correct time
        for key in missions.keys():
            for drop, file in zip(missions[key]['dropsondes'], missions[key]['drop_files']):
                file_dt_str = re.search(r'(\d{12})\.txt', file).group(1)
                file_dt = datetime.strptime(file_dt_str, '%Y%m%d%H%M')

                if drop['BOTTOMtime'] == file_dt:
                    pass
                else:
                    drop['BOTTOMtime'] = file_dt
                    
    
        # Temporally filter missions
        keys = [k for k in missions.keys()]
        for key in keys:
            end_time = pd.to_datetime(
                missions[key]['hdobs']['time'].values[-1])
            if end_time < start_time_request:
                del missions[key]
        
        # Sort each mission by time
        for key in missions.keys():
            missions[key]['hdobs'].sort_values(['time'], inplace=True)

        all_drops = [] 
        
        # return a list of all dropsondes by missions
        for mission_key in missions.keys():
            for inner_key in missions[mission_key].keys(): 
                if inner_key == 'dropsondes':
                    all_drops.append(missions[mission_key][inner_key])
        
        return all_drops
    #################################################################
    
    
    
    
        

    #################################################################
    ### SORT ALL DROPS BY TIME ###
    #################################################################
    def list_drops(self):
             
        all_drops = dropsonde_data().load_data()
        sorted_drops = sorted([item for sublist in all_drops for item in sublist],
                              key=lambda x: x['BOTTOMtime'])
        
        # add a 'N/A' location value if location key is missing 
        for drop in sorted_drops:
            if 'location' in drop:
                pass
            else:
                drop['location'] = 'N/A'
        
        # create a list of mission "ids" to pick from
        mission_ids = []
        for drop in sorted_drops:
            mission_ids.append(f"{drop['mission_id']}__{drop['BOTTOMtime'].strftime('%H%M')}z__{drop['location']}")

        # create class instance variables of both lists
        self.sorted_drops, self.mission_ids = sorted_drops[::-1], mission_ids[::-1]
        
        # return a reversed list of time sorted dropsonde dicts and mission ids
        return sorted_drops[::-1], mission_ids[::-1]
    #################################################################
    
    
    
    
    
    
    #################################################################
    ### SORT ALL DROPS BY MISSION ###
    #################################################################
    # return a list of lists, each list contains dicts of dropsondes for a specific mission
    # may be useful for composite plots
    def by_mission(self):
        
        all_drops = dropsonde_data().load_data()
        for i in range(0, len(all_drops)):
            for drop in all_drops[i]:
                if 'location' in drop:
                    pass
                else:
                    drop['location'] = 'N/A'

        return all_drops
    #################################################################
    
    
    
    
    
    
    #################################################################
    ### BUILD "CLEAN_DATA" DICT OF DROP DATA ###
    #################################################################
    def build_clean_data(self, drop):
            
            clean_data = {}
            clean_data = {
                    'p':  np.array(drop['levels']['pres'] *units.hPa),
                    'z':  np.array(drop['levels']['hgt']  *units.m),
                    'T':  np.array(drop['levels']['temp'] *units.degC),
                    'Td': np.array(drop['levels']['dwpt'] *units.degC),
                    'wd': np.array(drop['levels']['wdir'] *units.degrees),
                    'ws': np.array(drop['levels']['wspd'] *units.kts),
                    'u':  np.array(-drop['levels']['wspd'] * np.sin(drop['levels']['wdir'] * np.pi / 180)),
                    'v':  np.array(-drop['levels']['wspd'] * np.cos(drop['levels']['wdir'] * np.pi / 180)),

                    'drop-info': {
                        'mission-id'  : drop['mission_id'],
                        'mission-name': drop['mission'],
                        'storm-name'  : drop['stormname'],
                        'obs-number'  : drop['obsnum'],
                        'drop-time'   : drop['BOTTOMtime'],
                        'latlon'      : [drop['lat'], drop['lon']],
                        'drop-lctn'    : drop['location'],
                        'source'    : 'AIRCRAFT RECONNAISSANCE DROPSONDE',
                        'model'     : 'no-model',
                        'fcst-hour' : 'no-fcst-hour',
                        'run-time'  : ['none', 'none', 'none', 'none'],
                        'valid-time': [drop['BOTTOMtime'].strftime('%Y'), drop['BOTTOMtime'].strftime('%m'), 
                                       drop['BOTTOMtime'].strftime('%d'), drop['BOTTOMtime'].strftime('%H:%M')]
                                         },

                    'mand': {

                    }
            }

            # Desired pressure levels
            mand_levels = np.array([1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100])

            old_keys = ['p', 'z', 'T', 'Td', 'ws', 'wd']
            new_keys = ['mand_p', 'mand_z', 'mand_T', 'mand_Td', 'mand_ws', 'mand_wd']

            for old_key, new_key in zip(old_keys, new_keys):
                clean_data['mand'][new_key] = clean_data[old_key][np.isin(clean_data['p'], mand_levels)]


            return clean_data
    #################################################################
    
    
    
    
    
    #################################################################
    ### CREATE FIGURE ###
    #################################################################
    # given a mission id (created and returned above)
    # return a single 'clean_dict' of dropsonde data 
    def get_drop(self, mission_id, new_search=False, drops_by_time=None):
        
        if new_search == True:
            for drop in dropsonde_data().list_drops[0]:
                if f"{drop['mission_id']}__{drop['BOTTOMtime'].strftime('%H%M')}z__{drop['location']}" == mission_id:
                    dropsonde_data().build_clean_data(drop)
                else: 
                    pass
        else:
            if drops_by_time == None:
                raise ValueError("Must provide a list of dropsonde Dicts from `dropsonde_data().list_drops`")
            else:       
                for drop in drops_by_time:
                    if f"{drop['mission_id']}__{drop['BOTTOMtime'].strftime('%H%M')}z__{drop['location']}" == mission_id:
                        return dropsonde_data().build_clean_data(drop)
                        break
                    else:
                        print("get data failed")          
    ###############################################################






#####################
# PLOTTING FUNCTIONS  
#########################################################################

# Soundings 
def build_sounding(clean_data, style='full', color_blind=False, dark_mode=False, storm_motion='right_moving', special_parcels=None, show_radar=True, radar_time='sounding', map_zoom=2, modify_sfc=None, save=False, filename='sounderpy_sounding'):
    
    '''
       Return a full sounding plot of SounderPy data, ``plt`` 

       :param clean_data: the dictionary of data to be plotted (see :doc:`gettingdata`)
       :type clean_data: dict, required
       :param style: may be `simple` or `full`. Default is `full`.
       :type style: str, optional
       :param color_blind: whether or not to change the dewpoint trace line from green to blue for improved readability for color deficient users/readers. Default is ``False``
       :type color_blind: bool, optional
       :param dark_mode: ``True`` will invert the color scheme for a 'dark-mode' sounding. Default is ``False``.
       :type dark_mode: bool, optional
       :param storm_motion: the storm motion used for plotting and calculations. Default is 'right_moving'. Custom storm motions are accepted as a `list` of `floats` representing direction and speed. Ex: ``[270.0, 25.0]`` where '270.0' is the *direction in degrees* and '25.0' is the *speed in kts*. See the :ref:`storm_motions` section for more details.
       :type storm_motion: str or list of floats, optional
       :param special_parcels: a nested list of special parcels from the ``ecape_parcels`` library. The nested list should be a list of two lists (`[[a, b], [c, d]]`) where the first list should include 'highlight parcels' and second list should include 'background parcels'. For more details, see the :ref:`parcels_logic` section.
       :type special_parcels: nested `list` of two `lists`, optional
       :param save: whether to show the plot inline or save to a file. Default is ``False`` which displays the file inline.
       :type save: bool, optional
       :param filename: the filename by which a file should be saved to if ``save = True``. Default is `sounderpy_sounding`.
       :type filename: str, optional
       :return: plt, a SounderPy sounding built with Matplotlib, MetPy, SharpPy, & SounderPy.
       :rtype: plt
    '''
    
    print(f'> SOUNDING PLOTTER FUNCTION --\n---------------------------------')
        
    if style == 'full':
        if save == True:
            __full_sounding(clean_data, color_blind, dark_mode, storm_motion, special_parcels, show_radar, radar_time, map_zoom, modify_sfc).savefig(filename, bbox_inches='tight')
        else:
            __full_sounding(clean_data, color_blind, dark_mode, storm_motion, special_parcels, show_radar, radar_time, map_zoom, modify_sfc).show()
    elif style == 'simple':
        if save == True:
            __simple_sounding(clean_data, color_blind, dark_mode, storm_motion).savefig(filename, bbox_inches='tight')
        else:
            __simple_sounding(clean_data, color_blind, dark_mode, storm_motion).show()








# Hodographs 
def build_hodograph(clean_data, save=False, dark_mode=False, storm_motion='right_moving', sr_hodo=False, filename='sounderpy_hodograph'):
    
    '''
       Return a full sounding plot of SounderPy data, ``plt`` 

       :param clean_data: the dictionary of data to be plotted (see :doc:`gettingdata`)
       :type clean_data: dict, required
       :param save: whether to show the plot inline or save to a file. Default is ``False`` which displays the file inline.
       :type save: bool, optional
       :param filename: the filename by which a file should be saved to if ``save = True``. Default is `sounderpy_sounding`.
       :type filename: str, optional
       :param dark_mode: ``True`` will invert the color scheme for a 'dark-mode' sounding. Default is ``False``.
       :type dark_mode: bool, optional
       :param storm_motion: the storm motion used for plotting and calculations. Default is 'right_moving'. Custom storm motions are accepted as a `list` of `floats` representing direction and speed. Ex: ``[270.0, 25.0]`` where '270.0' is the *direction in degrees* and '25.0' is the *speed in kts*. See the :ref:`storm_motions` section for more details.
       :type storm_motion: str or list of floats, optional
       :param sr_hodo: transform the hodograph from ground relative to storm relative 
       :type sr_hodo: bool, optional, default is ``False``
       :return: plt, a SounderPy sounding built with Matplotlib, MetPy, SharpPy, & SounderPy.
       :rtype: plt
    '''
    
    print(f'> HODOGRAPH PLOTTER FUNCTION --\n-------------------------------')
    
    if save == True:
        __full_hodograph(clean_data, dark_mode, storm_motion, sr_hodo).savefig(filename, bbox_inches='tight')
    else:
        __full_hodograph(clean_data, dark_mode, storm_motion, sr_hodo).show()    









# VAD Hodographs 
def build_vad_hodograph(vad_data, save=False, dark_mode=False, storm_motion='right_moving', sr_hodo=False, filename='sounderpy_hodograph'):
    
    '''
       Return a VAD hodograph plot of SounderPy VAD data, ``plt`` 

       :param vad_data: the dictionary of VAD data to be plotted
       :type vad_data: dict, required
       :param save: whether to show the plot inline or save to a file. Default is ``False`` which displays the file inline.
       :type save: bool, optional
       :param filename: the filename by which a file should be saved to if ``save = True``. Default is `sounderpy_sounding`.
       :type filename: str, optional
       :param dark_mode: ``True`` will invert the color scheme for a 'dark-mode' sounding. Default is ``False``.
       :type dark_mode: bool, optional
       :param storm_motion: the storm motion used for plotting and calculations. Default is 'right_moving'. Custom storm motions are accepted as a `list` of `floats` representing direction and speed. Ex: ``[270.0, 25.0]`` where '270.0' is the *direction in degrees* and '25.0' is the *speed in kts*. See the :ref:`storm_motions` section for more details.
       :type storm_motion: str or list of floats, optional
       :param sr_hodo: transform the hodograph from ground relative to storm relative 
       :type sr_hodo: bool, optional, default is ``False``
       :return: plt, a SounderPy sounding built with Matplotlib, MetPy, SharpPy, & SounderPy.
       :rtype: plt
    '''
    
    print(f'> VAD HODOGRAPH PLOTTER FUNCTION --\n------------------------------------')
    
    if save == True:
        __vad_hodograph(vad_data, dark_mode, storm_motion, sr_hodo).savefig(filename, bbox_inches='tight')
    else:
        __vad_hodograph(vad_data, dark_mode, storm_motion, sr_hodo).show()    








# Composite Soundings 
def build_composite(data_list, shade_between=True, cmap='viridis', colors_to_use='none', ls_to_use='none', alphas_to_use='none',
                    lw_to_use='none', dark_mode=False, save=False, filename='sounderpy_hodograph'):
    '''
       Return a composite sounding plot of multiple profiles, ``plt`` 

       :param data_list: a list of data dictionaries for each profile to be plotted
       :type data_list: list of dicts, required
       :param shade_between: Lightly shade between the dewpoint & temperature trace. In many cases, this improves readability. Default is ``True``.
       :type shade_between: bool, optional
       :param cmap: a linear colormap, may be any custom or matplotlib cmap. Default is 'viridis'. If `colors_to_use` kwarg is provided, `colors_to_use` will be used instead.
       :type cmap: `matplotlib.colors.LinearSegmentedColormap` or `str` representing the name of a matplotlib cmap, optional
       :param colors_to_use: A list of custom matplotlib color name stings. List length must match the number of profiles listed in ``data_list``. Default is 'none'.
       :type colors_to_use: list of strings, optional
       :param alphas_to_use: A list of custom alphas (0.0-1.0). List length must match the number of profiles listed in ``data_list``. Default is 'none'. Default alpha is 1.
       :type alphas_to_use: list of floats, optional
       :param ls_to_use: A list of custom matplotlib linestyles. List length must match the number of profiles listed in ``data_list``. Default is 'none'. Default linestyle is '-'.
       :type ls_to_use: list of stings, optional
       :param lw_to_use: A list of custom linewidths. List length must match the number of profiles listed in ``data_list``. Default is 'none'. Default linewidth is 3.
       :type lw_to_use: list of floats, optional
       :param dark_mode: ``True`` will invert the color scheme for a 'dark-mode' sounding. Default is ``False``.
       :type dark_mode: bool, optional
       :param save: whether to show the plot inline or save to a file. Default is ``False`` which displays the file inline.
       :type save: bool, optional
       :param filename: the filename by which a file should be saved to if ``save = True``. Default is `sounderpy_sounding`.
       :type filename: str, optional
       :return: plt, a SounderPy composite sounding built with Matplotlib, MetPy, SharpPy, & SounderPy.
       :rtype: plt

    '''
    
    print(f'> COMPOSITE SOUNDING FUNCTION --\n-------------------------------')
    
    if save == True:
        __composite_sounding(data_list, shade_between, cmap, colors_to_use, 
            ls_to_use, alphas_to_use, lw_to_use, dark_mode).savefig(filename, bbox_inches='tight')
    else:
        __composite_sounding(data_list, shade_between, cmap, colors_to_use, 
            ls_to_use, alphas_to_use, lw_to_use, dark_mode).show() 
        
        
        
        
# print out data to console
def print_variables(clean_data):
    
    sounding_params(clean_data, storm_motion='right_moving', sfc_correction=None).print_vals()






# Dropsonde Soundings 
def build_dropsonde(drop_data, dark_mode=False, color_blind=False, add_sat=True, save=False, filename='sounderpy_dropsonde'):

    print(f'> DROPSONDE PLOTTER FUNCTION --\n-------------------------------')

    if save == True:
        __dropsonde(drop_data, dark_mode, color_blind, add_sat).savefig(filename, bbox_inches='tight')
    else:
        __dropsonde(drop_data, dark_mode, color_blind, add_sat).show()







    
#############################################################################################################################
    





    
    
##################
# HELPER FUNCTIONS 
#########################################################################

'''
     
     A collection of helper fucntions that users may find useful for processing 
     vertical profile data but are not necessary to use the basic functions of 
     SounderPy.
     
'''
    
#########################
# INTERPOLATE DATA  
#########################################################################    
def interp_data(variable, heights, step=100):
    
    '''
    Interpolate a 1D array of data (such as a temperature profile) over a given interval (step) based on a corresponding array of height values. 

    :param variable: an array of data to be interpolated. Must be same length as height array.
    :type variable: arr, required
    :param heights: heights corresponding to the vertical profile used to interpolate. Must be same length as variable array.
    :type heights: arr, required
    :param step: the resolution of interpolation. Default is 100 (recommended value is 100)
    :type step: int, optional
    :return: interp_var, an array of interpolated data.
    :rtype: arr
    '''
    
    try:
        variable.units
        variable = variable.m
    except:
        variable = variable
    try:
        heights.units
        heights = heights.m
    except:
        heights = heights
        
    levels=np.arange(0,np.max(heights),step)
    varinterp=np.zeros(len(levels))
    for i in range(0,len(levels)):
        lower=np.where(heights-levels[i]<=0,heights-levels[i],-np.inf).argmax()
        varinterp[i]=(((variable[lower+1]-variable[lower])/(heights[lower+1]-heights[lower]))*(levels[i]-heights[lower])+variable[lower])
    return varinterp 

    
#########################
# FIND NEAREST 
#########################################################################     
def find_nearest(array, value):
    
    '''
        search through an array to find the index of the value nearest to a given value
        
    '''
    
    array = np.asarray(array)
    nearest_idx = (np.abs(array - value)).argmin()
    return nearest_idx

    

    
#########################
# GET SFC INDEX
#########################################################################    
def get_sfc_index(height_arr):
    
    """
    Return a value of an index of an array who's value is closest to a define value.

    :param array: an array of data to be searched through
    :type array: arr, required
    :param heights: the value used to compare against the array of data
    :type heights: int or float, required
    :return: nearest_idx, index of the data array that corresponds with the nearest value to the given value
    :rtype: int
    """
    
    i = 0
    # Search the array for the sfc index
    while i < len(height_arr):
        if height_arr[i] >= 0:
            return i
        else:
            i += 1
    # Did not find a positive index
    return -1


####################
# MAKE SURFACE BASED  
#########################################################################    
def make_sfc_based(arr, sfc_val, sfc_index):
    
    """
    takes an array and a valid index in that array, then returns a copy of the
    array beginning at the provided index i.e., chops off below-ground values
    """

    # Initialize an empty numpy array as the modified array
    mod_arr = np.empty(len(arr) - sfc_index)
    # Insert the sfc and higher values into the modified array
    i = 0
    while i < len(mod_arr):
        mod_arr[i] = arr[i + sfc_index]
        i = i + 1
    # Inserts surface values
    mod_arr = np.insert(mod_arr, 0, sfc_val)
    return mod_arr
    

    
#########################
# MAKE SURFACE-BASED 3D 
#########################################################################    
def make_sfc_based_3D(arr, sfc_arr):
    
    '''
    takes a 3D array of mandatory level data and a 2D array of surface data, 
    appends the surface data onto the mandatory level array, and returns a single array
    of both surface and mandatory level data  
    '''
    
    mod_arr = np.zeros((np.shape(arr)[0]+1,np.shape(arr)[1],np.shape(arr)[2]))
    for j in range(np.shape(arr)[1]):
        for k in range(np.shape(arr)[2]):
            mod_arr[0,j,k] = sfc_arr[j,k]
            mod_arr[1:,j,k] = arr[:,j,k]
    return mod_arr


    
    
#########################
# FILE CREATION FUNCTIONS  
#########################################################################        

def to_file(file_type, clean_data, filename=None):
    '''
    Create a file of 'cleaned' SounderPy data

   :param file_type: a `str` representing the file type you'd like to export data to.
   :type file_type: str, required
   :param clean_data: 'cleaned' SounderPy data `dict`
   :type clean_data: dict, required
   :param filename: the name you'd like to give the file
   :type filename: str, required
   :return: a file of SounderPy data.
    '''
    
    
    # set file name 
    if filename == None:
        filename = f'sounderpy_data'
    else:
        filename = filename
        
        
    ####################################### CM1 #######################################
    if file_type == 'cm1':
        '''
        creates CM1 input sounding file for CM1 integration
        
        Derived from Kelton Halbert / Leigh Orf via github: 
        https://github.com/leighorf/LOFS-read/blob/master/bin/sndmod
        '''
            
        # create file    
        outfile = open(filename, 'w')
        num_lines = len(list(clean_data.items())[0][1])
        delimiter=''

        # use metpy to find parameters that CM1 likes
        clean_data['theta'] = mpcalc.potential_temperature(clean_data['p'], clean_data['T'])
        clean_data['relhm'] = mpcalc.relative_humidity_from_dewpoint(clean_data['T'], clean_data['Td'])
        clean_data['mixrt'] = mpcalc.mixing_ratio_from_relative_humidity(clean_data['p'], clean_data['T'], clean_data['relhm'])

        # add data to lines 
        for idx in range(num_lines):
                line_str = ""
                line_str += "%12s" % str(format(np.around(clean_data["z"][idx].m, 6), "0.6f")) + delimiter + str("\t")
                line_str += "%12s" % str(format(np.around(clean_data["theta"][idx].m, 6), "0.6f")) + delimiter + str("\t")
                line_str += "%12s" % str(format(np.around(clean_data["mixrt"][idx].m, 6), "0.6f")) + delimiter + str("\t")
                line_str += "%12s" % str(format(np.around(clean_data["u"][idx].m, 6), "0.6f")) + delimiter + str("\t")
                line_str += "%12s" % str(format(np.around(clean_data["v"][idx].m, 6), "0.6f")) + str("\n")
                outfile.write(line_str)

        outfile.close()
        
        
        
    ####################################### CSV #######################################
    elif file_type == 'csv':
        '''
        creates CSV file of sounding data
        '''

        # remove units from data
        no_units = {}
        for key in ['p', 'z', 'T', 'Td', 'u', 'v']:
                no_units[key] = clean_data[key].m
        # open and write to CSV 
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(no_units.keys())
            writer.writerows(zip(*no_units.values()))   
            
            
            
    ####################################### SHARPPY #######################################    
    elif file_type == 'sharppy':
        '''
        creates NSHARP input sounding file for SharpPy integration

        Derived from Kelton Halbert / Leigh Orf via github: 
        https://github.com/leighorf/LOFS-read/blob/master/bin/sndmod
        '''


        outfile_file = open(filename, 'w')

        outfile_loc = ("****")

        dt = datetime(int(clean_data['site_info']['valid-time'][0]), int(clean_data['site_info']['valid-time'][1]), 
                       int(clean_data['site_info']['valid-time'][2]), int(clean_data['site_info']['valid-time'][3][0:2]))

        outfile_file.write("%TITLE%\n")
        outfile_file.write("%s   %s\n" % (clean_data['site_info']['site-id'], dt.strftime("%y%m%d/%H%M")))
        outfile_file.write("   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD\n")
        outfile_file.write("-------------------------------------------------------------------\n")
        outfile_file.write("%RAW%\n")

        ws = mpcalc.wind_speed(clean_data['u'], clean_data['v'])
        wd = mpcalc.wind_direction(clean_data['u'], clean_data['v'])

        new_data = {
            'p' : clean_data['p'],
            'z' : clean_data['z'],
            'T' : clean_data['T'],
            'Td': clean_data['Td'],
            'wd': wd,
            'ws': ws,
        }

        for idx in range(new_data['p'].shape[0]):
            string = ""
            for col in ['p', 'z', 'T', 'Td', 'wd', 'ws']:
                string += "%12.6f,  " % new_data[col][idx].m

            outfile_file.write(string[:-3] + "\n")
        outfile_file.write("%END%\n")
        outfile_file.close()    

##########################################################################################################################################    
    

    
    
    
    
    

    
#########################
# LAT-LON FINDER FUNCTION
#########################################################################     
 
def get_latlon(station_type, station_id):
    
    '''
    Return a latitude-longitude float pair in a ``list``

    :param station_type: the station 'type' that corresponds with the given station ID
    :type station_type: str, required
    :param station_id: the station ID for the given station type
    :type station_id: str, required
    :return: lat/lon float pair
    :rtype: list
    '''
    
    station_id = str.upper(station_id)
    
    # DMS to decimal degrees
    def dms2dd_min(degrees, minutes, direction):
        dd = float(degrees) + float(minutes) / 60
        if direction == "S" or direction == "W":
            dd *= -1
        return dd
    
    def dms2dd(degrees, direction):
        dd = float(degrees)
        if direction == "S" or direction == "W":
            dd *= -1
        return dd
    

    ############################################### METAR #####################################################
    if station_type.casefold() == 'metar':
        '''
        takes a METAR site id such as 'KMBS', searches over 9000 station IDs  and returns
        a list including the lat/lon for the METAR site
        '''
        # get METAR stations list
        request = requests.get("https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/METAR-STATIONS.txt", 
                               stream=True)
        stations = {}
        for line in request.iter_lines():
            data = line.decode("ascii")
            if data:
                if data[0] == "!" or len(data) != 83:
                    continue
                province = data[0:2]
                station = data[3:19].strip()
                icao = data[20:24].strip()
                lat = dms2dd_min(data[39:41], data[42:44], data[44:45])
                lon = dms2dd_min(data[47:50], data[51:53], data[53:54])
                altitude = int(data[55:59])
                country = data[81:83]

                if icao:
                    stations[icao] = {"name": station, "lat": lat, "lon": lon, "altitude": altitude, "country": country}
        try:
            latlon = [np.round(stations.get(station_id)['lat'],2), np.round(stations.get(station_id)['lon'],2)]
            return latlon
        except:
            raise ValueError(f"The station you requested ({station_id}) doesn't seem to exist\n" +
                              "TIP: most METAR IDs include a 'K' in front, such as 'KMOP'") 

    ############################################### BUFKIT #####################################################    
    elif station_type.casefold() == 'bufkit': 
        '''
        takes a BUFKIT site id such as 'KMOP', searches over 1200 station IDs and returns
        a list including the lat/lon for the BUFKIT site
        '''
        # get BUFKIT stations list
        BUFKIT_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/BUFKIT-STATIONS-MASTER.txt', 
                                      skiprows=7, skipinitialspace = True)
        
        try:
            station = BUFKIT_STATIONS['ID'][np.where(BUFKIT_STATIONS['ID'].str.contains(station_id, na=False, case=True))[0]].values[0]
            lat = (BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['LAT'].values[0])
            lon = (BUFKIT_STATIONS[BUFKIT_STATIONS['ID']==station]['LON'].values[0])
            return [lat, lon]
        except:
             raise ValueError(f"The station you requested ({station_id}) doesn't seem to exist\n" +
                              "TIP: some IDs include a 'K' in front, such as 'KMOP', others are 3 digits, such a 'DTX'") 
            
        
    ############################################### RAOB #####################################################    
    elif station_type.casefold() == 'raob':
        
        '''
        takes a RAOB site id such as 'DTX', searches over 9000 station IDs  and returns
        a list including the lat/lon for the RAOB site
        '''
        # get RAOB stations list
        RAOB_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/RAOB-STATIONS.txt', 
                                    skiprows=7, skipinitialspace = True)

        # find lat-lon from stations list if it exists 
        try:
            station = RAOB_STATIONS['ICAO'][np.where(RAOB_STATIONS['ICAO'].str.contains(station_id, na=False, case=True))[0]].values[0]
            lat = dms2dd(RAOB_STATIONS[RAOB_STATIONS['ICAO']==station]['LAT'].values[0], 
                         RAOB_STATIONS[RAOB_STATIONS['ICAO']==station]['A'].values[0])
            lon = dms2dd(RAOB_STATIONS[RAOB_STATIONS['ICAO']==station]['LON'].values[0], 
                         RAOB_STATIONS[RAOB_STATIONS['ICAO']==station]['B'].values[0])
            return [lat, lon]
        except:
            try: 
                station = RAOB_STATIONS['WMO'][RAOB_STATIONS[RAOB_STATIONS['WMO']==int(station_id)].index[0]]
                lat = dms2dd(RAOB_STATIONS[RAOB_STATIONS['WMO']==station]['LAT'].values[0], 
                             RAOB_STATIONS[RAOB_STATIONS['WMO']==station]['A'].values[0])
                lon = dms2dd(RAOB_STATIONS[RAOB_STATIONS['WMO']==station]['LON'].values[0], 
                             RAOB_STATIONS[RAOB_STATIONS['WMO']==station]['B'].values[0])
                return [lat, lon]
            except:
                 raise ValueError(f"The station you requested ({station_id}) doesn't seem to exist") 
    
    
    ############################################### IGRA #####################################################
    elif station_type.casefold() == 'igra':
        '''
        takes a IGRA2 site id such as 'GMM00010393', searches nearly 3000 station IDs  and returns
        a list including the lat/lon for the IGRA2 site
        '''

        # get IGRA stations list
        IGRA_STATIONS = pd.read_csv(f'https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/IGRA-STATIONS.txt', 
                                    skiprows=7, skipinitialspace = True)

        # find lat-lon from stations list if it exists 
        try:
            station = IGRA_STATIONS['ID'][np.where(IGRA_STATIONS['ID'].str.contains(station_id, na=False, case=True))[0]].values[0]

            lat = np.round(IGRA_STATIONS[IGRA_STATIONS['ID']==station]['LAT'].values[0], 2)
            lon = np.round(IGRA_STATIONS[IGRA_STATIONS['ID']==station]['LON'].values[0], 2)
            return [lat, lon]
        except:
             raise ValueError(f"The station you requested ({station_id}) doesn't seem to exist") 
            
    
    ############################################### BUOY #####################################################
    elif station_type.casefold() == 'buoy':
        '''
        takes a BUOY/CMAN site id such as '41001', searches through a number of station IDs and returns
        a list including the lat/lon for the BUOY/CMAN  site
        '''

        # get buoy stations list
        BUOY_STATIONS = pd.read_csv('https://raw.githubusercontent.com/kylejgillett/sounderpy/main/src/BUOY-STATIONS.txt', 
                                    skiprows=7, skipinitialspace = True)

        # find lat-lon from stations list if it exists
        try:
            station = BUOY_STATIONS['ID'][np.where(BUOY_STATIONS['ID'].str.contains(station_id, na=False, case=True))[0]].values[0]

            lat = dms2dd(BUOY_STATIONS[BUOY_STATIONS['ID']==station]['LAT'].values[0], 
                         BUOY_STATIONS[BUOY_STATIONS['ID']==station]['A'].values[0])
            lon = dms2dd(BUOY_STATIONS[BUOY_STATIONS['ID']==station]['LON'].values[0], 
                         BUOY_STATIONS[BUOY_STATIONS['ID']==station]['B'].values[0])
            return [lat, lon]
        except:
             raise ValueError(f"The station you requested ({station_id}) doesn't seem to exist\n" +
                              "TIP: buoy IDs typically look like this: '41001'") 
    else:
        raise ValueError(f"Incorrect station_type argument. Valid station_type-s are 'metar', 'raob', 'igra', 'bufkit', 'buoy'")  
             