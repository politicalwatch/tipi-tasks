#!/usr/bin/env python
from tipi_alerts import test
from tipi_alerts import validate


if __name__ == '__main__':
    #task = test.test_task.apply_async((3, 2))
    task = validate.send_validation_emails.apply_async()
