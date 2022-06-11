from src.monitor.monitor import TwitterMonitor


class MonitorFacade(object):

    def __init__(self):
        self._monitor = TwitterMonitor()

    def run(self):
        try:
            print('Running Monitor...')
            self._monitor.run()
            print('Monitor finished.')
        except:
            raise
