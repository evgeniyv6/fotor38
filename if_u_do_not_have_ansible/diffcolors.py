#!/usr/bin/env python

class PrintColor:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def header(cls, s, *args, **kwargs):
        print(cls.HEADER + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def green(cls, s, *args, **kwargs):
        print(cls.GREEN + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def blue(cls, s, *args, **kwargs):
        print(cls.BLUE + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def warning(cls, s, *args, **kwargs):
        print(cls.WARNING + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def fail(cls, s, *args, **kwargs):
        print(cls.FAIL + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def bold(cls, s, *args, **kwargs):
        print(cls.BOLD + s + cls.ENDC, *args, **kwargs)

    @classmethod
    def underline(cls, s, *args, **kwargs):
        print(cls.UNDERLINE + s + cls.ENDC, *args, **kwargs)