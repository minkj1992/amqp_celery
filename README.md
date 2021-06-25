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

## test list
1. how does celery communicate with django server when physically apart from each other?
  - django setting에 작성하는 broker_url을 통해서 물리적으로 떨어져있더라도, celery가 django 관련 task를 진행할 수 있다. (ex. django model CRUD)
  - 이를 확인하기 위해서는, rabbitmq를 하나 띄우고, 서로 떨어진 프로세스로 django와 celery를 동작시킨 다음, django model reference가 sync되는지를 확인한다.
2. celery를 consumer worker로만 사용하고 싶으면 어떻게 동작 시켜야 하는가?
3. celery를 multiple apps로 사용(ex multiple broker_url)하려면 어떤 명령어로 실행시켜야 할까?



## refs
- [celery best practice](https://gist.github.com/IrSent/5e4820f6b187d3654967b55e27d5d204)
- https://iam.namjun.kim/celery/2018/09/09/celery-routing/
- [셀러리 라우팅](https://stackoverflow.com/questions/28025053/celery-worker-sleep-not-working-correctly)
- [셀러리 공식문서 조합 best practice](http://docs.celeryq.org/en/latest/userguide/tasks.html#task-synchronous-subtasks)
- [stackoverflow celery max retries](https://stackoverflow.com/a/35665039)
- [셀러리 docs 라우팅](https://docs.celeryproject.org/en/stable/userguide/routing.html)