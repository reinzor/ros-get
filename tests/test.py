#!/usr/bin/env python
import os

from mock import patch

p = None
def setup():
    global p
    p = patch.dict(os.environ, {'XDG_CONFIG_HOME': 'mock_config'})
    p.start()


def teardown():
    p.stop()


def test_list_workspaces():
    from ros_get.workspace import list_workspaces
    list_workspaces(verbose=True)

def test_locate():
    from ros_get.workspace import locate
    locate(verbose=True)
