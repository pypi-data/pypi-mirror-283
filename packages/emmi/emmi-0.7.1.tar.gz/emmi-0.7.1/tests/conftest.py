#!/usr/bin/python3

import pytest, os, random, string
import emmi.app
import multiprocessing as mp
mp.set_start_method("spawn", force=True)


@pytest.fixture(scope='session')
def session_prefix():
    p = ''.join(random.choice(string.ascii_lowercase) \
                for i in range(6))
    sp = os.environ.get('EMMI_TEST_SESSION_PREFIX', p)
    print(f'Session IOC prefix: "{sp}"')
    return str(sp)


def make_app(*args, Type=None, **kwargs):
    if Type is None:
        Type = emmi.app.IocApplication
    aobj = Type(*args, **kwargs)
    aobj.setupIoc()
    aobj.runIoc()


@pytest.fixture(scope='class')
def ioc_prefix(session_prefix):
    p = f'{session_prefix}:{"".join(random.choice(string.ascii_lowercase))}:'
    print(f'AppSync ioc_prefix: {p}')
    return p

@pytest.fixture(scope='class')
def emmi_app_ioc(ioc_prefix, emmi_app_class):
    p = mp.Process(target=make_app, kwargs={'prefix': ioc_prefix,
                                            'Type': emmi_app_class})
    p.start()
    yield ioc_prefix
    p.kill()
    p.join()
