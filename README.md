**Deployment**
- Make sure you have the following packages installed - apt-get install python-pip python-virtualenv libxml2-dev libxslt-dev python-dev
- git clone https://github.com/pavlov-aleksey/image_search.git
- cd image_search
- virtualenv env --no-site-packages
- . env/bin/activate
- pip install -r ./requirements.txt

**Usage**
- python ./run.py "people emotions anger pictures"
