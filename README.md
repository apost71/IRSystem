# IRSystem

This project is a search engine to search over the depaul.edu domain.  The code for the search engine resides in the `search/engine` directory.  The rest of the code is a UI for displaying results.

### Running locally

First you need to clone this repository.

`git clone https://github.com/apost71/IRSystem.git`

Next, make sure you are in the top level directory and run:

`pip install -r requirements.txt`

Finally, move to the `search` directory and run:

`python manage.py runserver`

Now you should be able to see the search engine running at `127.0.0.1:8000/search`.
