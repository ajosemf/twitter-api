from dotenv import load_dotenv
from src.monitor.facade import MonitorFacade


if __name__ == '__main__':
    load_dotenv('.env')
    MonitorFacade().run()
