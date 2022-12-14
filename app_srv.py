import multiprocessing as mp


class AppService:
    """
    starting / stopping apps in another threads
    """
    proc_list = []

    def __init__(self, apps):

        context = mp.get_context('spawn')
        for name, app in apps.items():
            p = context.Process(target=app)
            p.name = name
            self.proc_list.append(p)

    def start(self):
        for p in self.proc_list:
            p.start()

    def stop(self):
        for p in self.proc_list:
            p.close()
