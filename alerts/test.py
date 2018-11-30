from celery import shared_task


@shared_task
def test_task(x, y):
    print(f"Test ok, {x} + {y} = {x+y}")
    return x + y
