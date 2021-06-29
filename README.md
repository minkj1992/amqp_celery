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


## Received and deleted unknown message. Wrong destination?!?
> keyword: `multi-broker`, `external rabbitmq`, `consumer only celery worker`

> 에러: Received and deleted unknown message. Wrong destination?!?

icp는 자체로 사용하는 celery worker 설정과, crux 쪽 rabbitmq에서 이벤트를 받아서 처리하는 consumer 전용(crux 이벤트) worker 세팅 총 2개가 존재하며, 따라서 broker가 2개 존재하는데요. celery는 원래 producer/consumer를 동시에 처리해주는게 기본 설정이기 때문에, consumer 전용 워커를 만들기 위해서는 kombu 설정을 만질 수 있는 bootsteps.ConsumerStep를 사용해서 워커를 구현해야 했습니다.  이렇게 구현하고 보니 crux 쪽 이벤트에 대해서 가끔 Received and deleted unknown message. Wrong destination?!? 에러를 발생시켜서 오류를 잡게 되었습니다.

- 원인:
celery가 django와 함께 실행하면서, 셀러리의 bootsteps.ConsumerStep 기능을 사용할 때 발생하는 버그입니다.
위의 상황에서 (consumer 전용)셀러리 워커를 실행하게 되면, 셀러리가 config에 설정된 routing_key를 기반으로 extra consumer(queue)를 추가적으로 생성하게 되는 버그가 있는데, 이렇게 생성된 consumer는 message핸들링해주는 정보가 없기 때문에, 여기로 라우팅되는 모든 메시지는 Received and deleted unknown message. Wrong destination 처리 되게 됩니다.
- 해결책 1
  - consumer 전용 셀러리 config에 설정된 태스크 큐를 None으로 설정(task_queues=None)후, bootsteps.ConsumerStep을 구현하는 class 내부에서 사용하려는 queue & exchange를 구현해줍니다. (주의: 추가로 celery를 실행해주는 명령어에 Queue를 명시하지 말아야 합니다.)
- 해결책 2
  - custom consumer에서 사용하려는 queue를 설정해주는 custom command-line option를 추가 후 실행해주어, 우회해줍니다.
[cli-추가방법](https://docs.celeryproject.org/en/stable/userguide/extending.html#command-line-programs)
- ref 1 (https://github.com/depop/celery-message-consumer/issues/17#issuecomment-458794564)
- ref 2(https://github.com/celery/celery/issues/2979#issuecomment-229506008)


## refs
- [celery best practice](https://gist.github.com/IrSent/5e4820f6b187d3654967b55e27d5d204)
- https://iam.namjun.kim/celery/2018/09/09/celery-routing/
- [셀러리 라우팅](https://stackoverflow.com/questions/28025053/celery-worker-sleep-not-working-correctly)
- [셀러리 공식문서 조합 best practice](http://docs.celeryq.org/en/latest/userguide/tasks.html#task-synchronous-subtasks)
- [stackoverflow celery max retries](https://stackoverflow.com/a/35665039)
- [셀러리 docs 라우팅](https://docs.celeryproject.org/en/stable/userguide/routing.html)