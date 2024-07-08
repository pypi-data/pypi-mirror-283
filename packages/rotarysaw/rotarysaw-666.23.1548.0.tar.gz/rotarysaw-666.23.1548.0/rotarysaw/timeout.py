

from time import sleep, monotonic

class Timeout():
    def __init__(self, timeout=5, t=None, fn=None, ref=monotonic):
        self.t = None
        self.ref = monotonic
        self.set(t)
        self.timeout = timeout
        assert fn is None or callable(fn)
        self.fn = fn

    def set(self, t=None):
        if t is None:
            self.t = self.ref()
        elif callable(t):
            self.t = t()
        else:
            self.t = t

    def elapsed(self):
        if self.t is None:
            return None

        ref = self.ref()

        return ref - self.t

    def __call__(self, *args, **kwargs):
        timeout = self.timeout
        if callable(timeout):
            timeout = self.timeout()

        if self.elapsed() > timeout:
            if 'set' in kwargs:
                if kwargs['set']:
                    if not isinstance(kwargs['set'], bool):
                        self.set(t=kwargs['set'])
                    else:
                        self.set()

            if self.fn is not None:
                ret = self.fn()
                if ret is not None:
                    return ret

            return True
        else:
            return False



