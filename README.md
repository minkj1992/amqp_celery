# celery with amqp
> pyhton 3.8.6

## setup
```bash
$ python3 -m venv celery-env
$ source celery-env/bin/activate
$ python3 -m pip install --upgrade pip
$ pip install celery django
$ docker compose up
```

## celery-django setup
```
$ django-admin startproject celery_django .
```


## todo
- [ ] consumer only celery worker
- [ ] multi broker celery structure
- [ ] 
