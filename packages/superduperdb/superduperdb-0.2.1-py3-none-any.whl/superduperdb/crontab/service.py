from superduperdb import CFG
from superduperdb.server import app as superduperapp

from .daemon import Daemon

assert isinstance(
    CFG.cluster.crontab.uri, str
), "cluster.crontab.uri should be set with a valid uri"
port = int(CFG.cluster.crontab.uri.split(':')[-1])


def _set_daemon(db):
    return {'daemon': Daemon(db)}


app = superduperapp.SuperDuperApp('crontab', port=port, init_hook=_set_daemon)


def build_service(app: superduperapp.SuperDuperApp):
    """Build the crontab service.

    :param app: SuperDuperApp instance.
    """

    @app.add('/crontab/remove', method='post')
    def crontab_remove(identifier: str):
        app.daemon.scheduler.remove_job(identifier)

    @app.add('/crontab/add', method='post')
    def crontab_add(identifier: str):
        app.daemon.add_job(identifier)

    @app.add('/crontab/show', method='get')
    def crontab_show():
        return app.daemon.list_jobs()

    return app


build_service(app)
