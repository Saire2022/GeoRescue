# GeoRescue
DSL creation for tracking people during disasters.

## API
The Application Programming Interface (API) documentation is available [here](https://documenter.getpostman.com/view/27080186/2s9YkgEkzd).

**API URL:** [https://apirest-qywgms5y2q-ue.a.run.app](https://apirest-qywgms5y2q-ue.a.run.app/?fbclid=IwAR0IbPBfwr7tippjae8Ug3jlF4qv1g8hSJwK9D63o4XkopMzikZ2A_TN55c)

The API runs on a Google Cloud Platform (GCP) server, allowing us to connect to the application and make requests to retrieve information from the database. Additionally, the database is deployed on GCP Cloud SQL.

If you want to run the API locally, follow these steps:
1. Clone this repository to your desired directory.
2. Create a virtual environment in the directory (e.g., `.\Venv\Scripts\activate`).
3. Activate the virtual environment (`.\Venv\Scripts activate`).
4. Run the `apirest.py` file using the command `python apirest.py`.

## SCRIPTS

You can run the script both locally and in an instance of Colab or Jupyter Notebook using the following command:

### `Draw_points.py`

1. Enter administrator username and password:
   - Enter your username: `1234567890`
   - Enter your password: `******`
2. The following menu will be displayed:

   `1.- Per user \
   2.- By time interval and user \
   3.- All points \
   Please select one: 2`
3. In this case, we have selected `2`, and we will be asked to enter the data in the required format:
- Draw points with Path? (Y/N): `n`
- Please enter the id: `1050440799`
- Please start date (yy-mm-dd): `2023-11-26`
- Please start time (hh:mm:ss): `13:00:00`
- Please end date (yy:mm:dd): `2023-11-26`
- Please end time (hh:mm:ss): `15:00:00`

Number of points: `4`
