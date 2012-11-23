from settings import settings
import time

def nice_print(args):
    if not settings['log-to-console']:
        return
    base = time.strftime("%H:%M:%S: ")
    for arg in args:
        base += '{:<33}'.format(arg)
    print base
