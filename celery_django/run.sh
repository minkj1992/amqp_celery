input=$1
# 0: none
# 1: demo app
# 2~: account

if [ "$#" -eq  0 ]
  then
    echo "No arguments supplied"
elif [ $input -eq 1 ]
  then
    echo "Demo start";
    celery -A celery_django.demo_app worker -l debug;
else
    echo "Account start";
    celery -A celery_django.account_app worker -l debug;
fi
