import multiprocessing as mp
from threading import Thread, active_count


class AppService:
    """
    starting / stopping apps in another threads
    """
    target_list = []

    def __init__(self, apps, use_process=True):

        self.use_process = True if use_process else False
        if use_process:
            context = mp.get_context('spawn')
            for name, app in apps.items():
                target = context.Process(target=app, name=name)
                self.target_list.append(target)
        else:
            for name, app in apps.items():
                target = Thread(target=app, name=name)
                self.target_list.append(target)

    def start(self):
        for p in self.target_list:
            p.start()

    def stop(self):
        if self.use_process:
            for p in self.target_list:
                p.close()

    def active_count(self):
        return active_count() if not self.use_process else len(self.target_list)
