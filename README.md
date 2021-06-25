# celery with amqp
> pyhton 3.8.6

## setup
```bash
$ pyenv virtualenv celery-env
$ pyenv activate celery-env
$ python3 -m pip install --upgrade pip
$ pip install celery django sqlalchemy
$ docker compose up
```

## celery-django setup
```
$ django-admin startproject celery_django .
$ django-admin startapp demoapp
$ python manage.py makemigrations
$ python manage.py migrate
$ celery -A celery_django worker -l INFO
```


## todo
- [ ] consumer only celery worker
- [ ] multi broker celery structure
- [ ] 


## refs
- [celery best practice](https://gist.github.com/IrSent/5e4820f6b187d3654967b55e27d5d204)
- https://iam.namjun.kim/celery/2018/09/09/celery-routing/
- [셀러리 라우팅](https://stackoverflow.com/questions/28025053/celery-worker-sleep-not-working-correctly)
- [셀러리 공식문서 조합 best practice](http://docs.celeryq.org/en/latest/userguide/tasks.html#task-synchronous-subtasks)
- [stackoverflow celery max retries](https://stackoverflow.com/a/35665039)
- [셀러리 docs 라우팅](https://docs.celeryproject.org/en/stable/userguide/routing.html)