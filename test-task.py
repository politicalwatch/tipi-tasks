#!/usr/bin/env python
from alerts import test


if __name__ == '__main__':
    task = test.test_task.apply_async((3, 2))
