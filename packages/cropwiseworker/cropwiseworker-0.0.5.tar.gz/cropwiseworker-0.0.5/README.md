
# cropwiseworker

## Description
The `Cropwise Worker` module is designed to work with the Cropwise Operations digital agricultural enterprise management platform API. The module allows you to interact with various platform data, facilitating the integration and automation of tasks.

## Installing
Install module using pip:

```bash
pip install cropwiseworker
```

## Module functions

### Mass download of data from the Cropwise Operations account

```python
data_downloader(endpoint, token, params=None, data_format=None, version=None)
```

- **endpoint (required)** – entry your endpoint from Cropwise Operations API documentation (https://cropwiseoperations.docs.apiary.io/)
- **token (required)** – entry your TOKEN from Cropwise Operations account
- **params** – entry your endpoint parameters using array format (default None)
- **data_format** – entry suggested data format (default pd.DataFrame(), also supported 'json')
- **version** – entry your Cropwise Operations API version using str data type (default 'v3')

### Create a massive dataset with soil test, crop rotation, agro operation and yield data for analysis named Agrimatrix

```python
agrimatrix_dataset(enterprise, token, season)
```

- **enterprise (required)** – entry a name of your enterprise
- **token (required)** – entry your TOKEN from Cropwise Operations account
- **season (required)** – entry an interested value of season using int data type

### Create a kml-file with several orchard rows inside of quarter kml-file

```python
create_orchard_rows(file_path, quarter_name, number_of_rows, direction, crop, download_directory)
```

- **file_path** – entry a directory of your quarter kml-file using str data type
- **quarter_name** – entry a name of quarter
- **number_of_rows** – entry the relevant number of orchard rows to create using int data type
- **direction** – choose one of the two variables of orchard rows direction: 'west_east' (horizontal), 'south_north' (vertical)
- **crop** – entry a name of crop which grows in your quarter using str data type
- **download_directory** – entry a directory to download result file using str data type

## Workflow examples

```python
import cropwiseworker as cw

token = 'YOUR_TOKEN'

params = {'created_at_gt_eq':'2023-01-01'}

fields = cw.data_downloader('fields', token=token, params=params)
print(fields)

my_2023_analysis = cw.agrimatrix_dataset('YOUR_ENTERPRISE_NAME', token=token, season=2023)
print(my_2023_analysis)

cw.create_orchard_rows('path/to/your/file.kml', 'QuarterName', 50, direction='south_north', 'Apple', 'path/to/download/directory')
```

## License
This package is distributed under the Apache License 2.0.
