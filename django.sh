source personalVenv/bin/activate
cd carenback
git stash
git pull origin final
python manage.py runserver 0.0.0.0:8181