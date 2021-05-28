import threading


def threaded(fn):
    """
    Permet de lancer un fonction en mode thread avec un décorateur
    @param fn: la focnition a threader
    @return: wrapper du thread
    """

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return wrapper
