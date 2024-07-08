import os
import numpy as np
import xarray as xr

"""
The python file gets global predictor data e.g. land cover classification data for the corresponding dimensions as the 
examined data cube (e.g. latitude and longitude coordinates). 
The results will be stored in a '.zarr' dataset.
During the area slicing process the zarr dataset is the source for the data in order to be used as predictors.
Once the global zarr dataset is executed, the dataset can be used for all gapfilling example applications.
This file can be helpful to extract other variables as predictors and match the coordinates.

Example:
```
    # Initializing the xcube datastore for s3 object storage and open the dataset of the variable you want to estimate
    data_store = new_data_store("s3", root="esdl-esdc-v2.1.1", storage_options=dict(anon=True))
    dataset = data_store.open_data('esdc-8d-0.083deg-184x270x270-2.1.1.zarr')
    ds_variable = dataset['land_surface_temperature']

    # Initializing the xcube datastore for s3 object storage and open the dataset of the predictor variable
    predictor = 'lccs_class'
    data_store = new_data_store("s3", root="deep-esdl-public", storage_options=dict(anon=True))
    dataset = data_store.open_data('LC-1x2160x2160-1.0.0.levels')
    ds_predictor = dataset.get_dataset(0)[predictor]

    HelpingPredictor(ds_variable, ds_predictor, predictor).get_predictor_data()
```
"""


class HelpingPredictor:
    """
    Get the predictor data for a specific variable.

    Attributes:
        ds_variable (xarray.DataArray): The dataset with the target variable you want to estimate
        ds_predictor (xarray.DataArray): The dataset with the predictor variable that will help the estimation
        predictor (str): The name of the predictor
    """
    def __init__(self, ds_variable, ds_predictor, predictor_path: str, predictor:str = 'lccs_class', layer_dim=None):
        self.layer_dim = layer_dim
        self.dim1 = None
        self.dim2 = None
        self.initialize_dimensions(layer_dim, list(ds_variable.dims))
        print(self.layer_dim, self.dim1, self.dim2)

        self.ds_variable = ds_variable.isel({self.layer_dim: 0})
        self.ds_predictor = ds_predictor.isel({self.layer_dim: 0})
        self.predictor = predictor
        self.predictor_path = predictor_path

    def initialize_dimensions(self, layer_dim, dims):
        dim1, dim2, dim3 = dims[0], dims[1], dims[2]
        if self.layer_dim is None:
            self.layer_dim = dim1
        layer_coords = [s for s in dims if s != layer_dim]
        self.dim1 = layer_coords[0]
        self.dim2 = layer_coords[1]

    def get_predictor_data(self):

        # Get the coordinates from both dimensions (e.g. lat, lon) from the dataset with variable that you will estimate.
        dim1_coord_variable = self.ds_variable[self.dim1].values
        dim2_coord_variable = self.ds_variable[self.dim2].values

        # Get predictor data for the corresponding coordinates
        predictor_array = self.extract_data(dim1_coord_variable, dim2_coord_variable)

        if self.predictor == 'lccs_class':
            # Function to process LCCS data and remap land cover class to lower the granularity
            predictor_array = self.process_lccs(predictor_array)

        # Save the processed predictor data to a zarr dataset
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(self.predictor_path, 'global_' + self.predictor + '.zarr')
        predictor_array.to_zarr(os.path.join(current_dir, filename), mode="w")
        return filename

    def extract_data(self, dim1_coord_variable, dim2_coord_variable):
        """
        Get predictor data for specified coordinates.

        This function extracts the predictor data for the specified dimensional coordinates (e.g. lat and lon).
        """

        # Extract the coordinates for the predictor data
        dim1_coord_predictor = self.ds_predictor[self.dim1].values
        dim2_coord_predictor = self.ds_predictor[self.dim2].values

        # Find indices for mapping coordinates
        dim1_indices = np.argmax(dim1_coord_predictor[:, None] <= dim1_coord_variable, axis=0) - 1
        dim2_indices = np.argmax(dim2_coord_predictor[:, None] >= dim2_coord_variable, axis=0) - 1

        dim1_indices = np.clip(dim1_indices, 0, len(dim1_coord_predictor) - 1)
        dim2_indices = np.clip(dim2_indices, 0, len(dim2_coord_predictor) - 1)

        # Extract predictor values based on indices
        predictor_array = self.ds_predictor[dim1_indices, dim2_indices]
        return predictor_array

    def process_lccs(self, lcc_array):
        """
        Process and remap LCCS data.

        This function remaps LCCS values based on a mapping dictionary and returns the processed data.
        """
        # The granularity of the Land Cover Classes from the Earth System Data Cube is larger than necessary, e.g.
        # different types of mixed forests. Therefore, multiple types of a main LCC are grouped together as one.
        value_mapping = {
            11: 10, 12: 10, 61: 60, 62: 60, 71: 70, 72: 70, 81: 80, 82: 80, 121: 120, 122: 120,
            151: 150, 152: 150, 153: 150, 201: 200, 202: 200
        }

        # Remap LCCS values based on the mapping dictionary
        for old_value, new_value in value_mapping.items():
            lcc_array = lcc_array.where(lcc_array != old_value, new_value)

        return lcc_array
