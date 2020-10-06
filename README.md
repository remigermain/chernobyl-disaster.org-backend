<div align="center"><img align="center" width="300" src="https://gitlab.com/chernobyl-disaster.org/frontend/-/raw/master/static/icon.png"/></div><br/>

>  The Chernobyl nuclear disaster is a major nuclear accident that occurred on April 26, 1986 in the V.I. Lenin nuclear power plant, then located in the Ukrainian Soviet Socialist Republic, USSR. It is the most serious nuclear disaster of the 20th century, classified at level 7 (the highest) of the International Nuclear Event Scale (INES), surpassing, according to the Institute for Radiation Protection and Nuclear Safety (IRSN), by its immediate environmental impacts the Fukushima nuclear accident of 2011, classified at the same level. The IRSN mentions for these accidents potential health effects, lasting contamination of territories and important economic and social consequences. This site recounts the events of the accident that led to this disaster and its consequences, illustrated by photo, video and archive document. 


## Getting started

>  in order for it to work properly, you need the frontend server to run, go [frontend](https://gitlab.com/chernobyl-disaster.org/frontend)

```sh
#create virtual environment 
python3 -m venv venv
source ./venv/bin/activate

# install package
pip install --upgrade pip
pip install -r requirements/dev.txt # or common.txt for production

# create local env file
python ./scripts/create_env -e
source .env

./manage.py migrate
./manage.py runserver
```

## Testing

```sh
# need virtual env

./manage.py test
```

## Supporting chernobyl-disaster

chernobyl-disaster is an MIT-licensed open source project with its ongoing development made possible entirely by the support of these awesome backers.

Support us with a donation and help us continue our activities.
[Paypal](https://chernobyl-disaster.org/about), [Buy Me A Coffee](https://www.buymeacoffee.com/rgermain) or [Liberapay](https://liberapay.com/rgermain/donate)

## Contributors

Thank you to all our [contributors](https://chernobyl-disaster.org/about)!


## License

[MIT](https://gitlab.com/chernobyl-disaster.org/frontend/-/blob/master/LICENSE)
