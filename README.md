# Virtual Credit Card Backend
A REST-API based backend for issuing virtual credit cards through facial recognition. This API has been made using the Django REST Framework.
This API utilises a pre-trained Inception ResNet V2 found [here](https://github.com/R4j4n/Face-recognition-Using-Facenet-On-Tensorflow-2.X/tree/master).

>**Note:** This repo only contains the backend. As of now, a frontend has not been implemented. However, in the `templates` folder you can find `new_frontend.html` which is a representation of how a basic frontend can look like, it can also interact with the backend using the Fetch API.

## Setup
It is assumed that you have already set up the database (for Django to use) for the project.
_Optionally you can set up the project in a [virtual environment](https://docs.python.org/3/library/venv.html)_.

1. Clone the repo via `git clone https://github.com/B4S1C-Coder/Virtual-Credit-Card-Backend.git`
2. Install dependencies via (make sure you are in the same directory as `manage.py`) `pip install -r requirements.txt`
3. The repo has `scale91backend_creditcardDB.DEVELOPMENT.sqlite3`, which is a small sqlite database that contains some dummy data. You can use this database or if you'd like to use MySQL, PostgreSQL etc. then you'll need to update the database credentials in `scale91backend/creds.py` and set `SCALE91_DB_USE_SQLITE = False` in `scale91backend/settings.py` (dont't forget to install the relevant clients)

>**Note:** The data pertianing to user photos (for facial recognition) in the sqlite3 db provided may not work since those photos are not in the repo (for privacy reasons).

4. Don't forget to `makemigrations` and `migrate`
5. You should be now good to go.

>**Note:** If you encounter any issues with the facial recognition model try using an older version of tensorflow 2.x

## Known issues
The camera will work in the browser only if the connection is secure (_https:// or file://_). Also whenever the django server is running (on my machine) the camera is unable to turn on. So if this issue happens with you, try keeping the backend on a separate machine (or deploy it on the cloud).