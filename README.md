# warbler
Twitter clone built entirely on Flask

**TODO**
  * Implement a messaging system 
  * reach higher testing coverage 
  * double check consistency is ordering of models and views 
  
**This is a work in progress back end of a twitter clone I built** 
The endpoints to this backend are not public at the moment but their is a live demo if the application integrated with a front end doployed [here on this site](http://warbler-kr.herokuapp.com/)

**instillation & startup**
You should be able to clone the repo here - set up a virtual env and pip install the contents of the requirements.txt.

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`(venv) $ pip install -r requirements.txt`

Set up an empty db called 'warbler' & 'warbler-test', the seed file should handle everything else DB related when you run it. 

`(venv) $ createdb warbler`

`(venv) $ python seed.py`

To start the server simply run the command `(venv) $ flask run` and you can make api calls to the endpoints declared in the codebase. Enjoy!
