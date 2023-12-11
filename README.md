# GeoRescue
DSL creation for tracking people on disasters.

## API
The Aplication Program Interface (API) is available in the following Documentation \

API URL: https://apirest-qywgms5y2q-ue.a.run.app/?fbclid=IwAR0IbPBfwr7tippjae8Ug3jlF4qv1g8hSJwK9D63o4XkopMzikZ2A_TN55c \

DPCUMENTATION URL: https://documenter.getpostman.com/view/27080186/2s9YkgEkzd 

The API runs on a Google Cloud Platform (GCP) server that allows us to connect to the application and make requests to get the information from the database. In addition, the database is deployed in GCP Cloud SQL.

If you want to run the API locally, you must follow these steps:
- Clone this repository in the desired directory.
- Create a virtual environment in the directory, for example: \
.\Venv\Scripts\activate. 
- Activate the virtual environment: \
.\Venv\Scripts activate
- Run the file apirest.py: \ 
python apirest.py

## SCRIPTS

You can run the script both locally and in an instance of Colab or Jupyter Notebook, using the following command:
Draw_points.py
- Enter administrator username and password: \
Enter your username: 1234567890 \
Enter your password: ****** 
- The following menu will be displayed: \
   1.- Per user \
   2.- By time interval and user \
   3.- All points \
   Please select one: 2 \
- In this case we have selected 2 and we will be asked to enter the data with the required format as shown below: \

   Draw points with Path? (Y/N): n  \
   Please enter the id: 1050440799  \
   Please start date (yy-mm-dd): 2023-11-26  \
   Please start time (hh:mm:ss): 13:00:00  \
   Please end date (yy:mm:dd): 2023-11-26  \
   Please end time (hh:mm:ss): 15:00:00   \
   Number of points: 4  \
