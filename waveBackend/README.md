# Wave 1.0 backend setup guide

This is an setup guide to get the backend and frontend up and running.

## Installation

Start by navigating to the backend folder.
```bash
cd waveBackend/
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements for the backend system.

```bash
pip install -r requirements.txt
```
Once the required modules are installed, create the database by running the following commands.
```bash
python manage.py makemigrations

python manage.py migrate
```
When the database has been created, start the server by running the following command.
```bash
python manage.py runserver 127.0.0.1:8000
```
### Load initial data
To load the initial data start by navigating to the backend services folder
```bash
cd BackendServices/
```
Then run the test_db_init.py script.
```bash
python test_db_init.py
```

### Start the broker service
The broker service is the service that connects the mqtt broker and the REST API. 
Run the following command to start the broker service.

Note: The django server must be running before starting the broker service.
```bash
python mqtt-http-client.py
```

Once that is done, the backend is ready to receive data from the simulator.

## Simulator

To start the simulator, simply run the following command:
```bash
python ship_simulator.py
```



## License

[MIT](https://choosealicense.com/licenses/mit/)