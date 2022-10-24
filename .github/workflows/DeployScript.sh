sudo su
killall gunicorn
cd GoClimb
git pull
git checkout master
gunicorn GoClimb.wsgi -b 0.0.0.0:80