import datetime
import typing as t
import uuid
from abc import abstractmethod

import superduperdb as s
from superduperdb import CFG, logging
from superduperdb.jobs.tasks import callable_job, method_job

if t.TYPE_CHECKING:
    from superduperdb.base.datalayer import Datalayer


def job(f):
    """
    Decorator to create a job from a function.

    :param f: function to be decorated
    """

    def wrapper(
        *args,
        db: t.Any = None,
        dependencies: t.Sequence[Job] = (),
        **kwargs,
    ):
        j = FunctionJob(callable=f, args=args, kwargs=kwargs)
        return j(db=db, dependencies=dependencies)

    return wrapper


class Job:
    """
    Base class for jobs. Jobs are used to run functions or methods on.

    :param args: positional arguments to be passed to the function or method
    :param kwargs: keyword arguments to be passed to the function or method
    :param identifier: Job identifier.
    :param db: A datalayer instance.
    """

    callable: t.Optional[t.Callable]

    def __init__(
        self,
        args: t.Optional[t.Sequence] = None,
        kwargs: t.Optional[t.Dict] = None,
        identifier: t.Optional[str] = None,
        db: t.Optional['Datalayer'] = None,
    ):
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.identifier = identifier or str(uuid.uuid4())
        self.time = datetime.datetime.now()
        self.callable = None
        self.db = None
        self.future = None
        self.job_id = None
        self.db = db

    def watch(self):
        """Watch the stdout of the job."""
        return self.db.metadata.watch_job(identifier=self.identifier)

    @abstractmethod
    def submit(self, compute, dependencies=(), update_job=True):
        """Submit job for execution.

        :param compute: compute engine
        :param dependencies: list of dependencies
        """
        raise NotImplementedError

    def dict(self):
        """Return a dictionary representation of the job."""
        return {
            'identifier': self.identifier,
            'time': self.time,
            'status': 'pending',
            'args': self.args,
            'kwargs': self.kwargs,
            'stdout': [],
            'stderr': [],
            'job_id': self.job_id,
        }

    def __call__(self, db: t.Any = None, dependencies=()):
        """
        Run the job.

        :param db: DB instance to be used
        :param dependencies: list of dependencies
        """
        raise NotImplementedError


class FunctionJob(Job):
    """Job for running a function.

    :param callable: function to be called
    :param args: positional arguments to be passed to the function
    :param kwargs: keyword arguments to be passed to the function
    :param db: A datalayer instance.
    """

    def __init__(
        self,
        callable: t.Callable,
        args: t.Optional[t.Sequence] = None,
        kwargs: t.Optional[t.Dict] = None,
        db: t.Optional['Datalayer'] = None,
    ):
        super().__init__(args=args, kwargs=kwargs, db=db)
        self.callable = callable

    def dict(self):
        """Return a dictionary representation of the job."""
        d = super().dict()
        path = self.callable.__module__ + ';' + self.callable.__name__
        d['_path'] = f'superduper/jobs/job/FunctionJob/{path}'
        return d

    def submit_remote(self, dependencies=()):
        """Submit job for remote execution.

        :param dependencies: list of dependencies
        """
        self.job_id = self.db.compute.submit(self.identifier, dependencies=dependencies)
        self.db.metadata.update_job(self.identifier, 'job_id', self.job_id)
        self.future = self.job_id
        return

    def submit(self, dependencies=(), update_job=True):
        """Submit job for execution.

        :param dependencies: list of dependencies
        """
        self.future, self.job_id = self.db.compute.submit(
            callable_job,
            cfg=s.CFG.dict(),
            function_to_call=self.callable,
            job_id=self.identifier,
            args=self.args,
            kwargs=self.kwargs,
            dependencies=dependencies,
            db=self.db if self.db.compute.type == 'local' else None,
        )
        if update_job and self.future:
            self.db.metadata.update_job(self.identifier, 'job_id', self.future)
        return

    def __call__(self, db: t.Union['Datalayer', None], dependencies=()):
        """Run the job.

        :param db: Datalayer instance to use
        :param dependencies: list of dependencies
        """
        if db is None:
            from superduperdb.base.build import build_datalayer

            db = build_datalayer()

        self.db = db
        db.metadata.create_job(self.dict())

        if db.compute.remote is True:
            self.submit_remote(dependencies=dependencies)
        else:
            self.submit(dependencies=dependencies)

        return self


class ComponentJob(Job):
    """
    Job for running a class method of a component.

    :param component_identifier: unique identifier of the component
    :param type_id: type of the component
    :param method_name: name of the method to be called
    :param args: positional arguments to be passed to the method
    :param kwargs: keyword arguments to be passed to the method
    :param compute_kwargs: Arguments to use for model predict computation
    :param db: A Datalayer instance.
    """

    def __init__(
        self,
        component_identifier: str,
        type_id: str,
        method_name: str,
        args: t.Optional[t.Sequence] = None,
        kwargs: t.Optional[t.Dict] = None,
        compute_kwargs: t.Dict = {},
        db: t.Optional['Datalayer'] = None,
    ):
        self.compute_kwargs = compute_kwargs or CFG.cluster.compute.compute_kwargs

        super().__init__(args=args, kwargs=kwargs, db=db)

        self.component_identifier = component_identifier
        self.method_name = method_name
        self.type_id = type_id
        self._component = None

    @property
    def component(self):
        """Get the component."""
        return self._component

    @component.setter
    def component(self, value):
        """Set the component.

        :param value: component to set
        """
        self._component = value
        self.callable = getattr(self._component, self.method_name)

    def submit_remote(self, dependencies=()):
        """Submit job for remote execution.

        :param dependencies: list of dependencies
        """
        self.job_id = self.db.compute.submit(
            self.identifier,
            dependencies=dependencies,
            compute_kwargs=self.compute_kwargs,
        )
        self.db.metadata.update_job(self.identifier, 'job_id', self.job_id)
        self.future = self.job_id
        return

    def submit(self, dependencies=(), update_job=True):
        """Submit job for execution.

        :param dependencies: list of dependencies
        """
        self.future, self.job_id = self.db.compute.submit(
            method_job,
            cfg=s.CFG.dict(),
            type_id=self.type_id,
            identifier=self.component_identifier,
            method_name=self.method_name,
            job_id=self.identifier,
            args=self.args,
            kwargs=self.kwargs,
            dependencies=dependencies,
            db=self.db if self.db.compute.type == 'local' else None,
        )
        if update_job and self.future:
            self.db.metadata.update_job(self.identifier, 'job_id', self.future)
        return self

    def __call__(self, db: t.Union['Datalayer', None] = None, dependencies=()):
        """Run the job.

        :param db: Datalayer instance to use
        :param dependencies: list of dependencies
        """
        if db is None:
            from superduperdb.base.build import build_datalayer

            db = build_datalayer()

        self.db = db

        db.metadata.create_job(self.dict())
        if self.component is None:
            self.component = db.load(self.type_id, self.component_identifier)

        if db.compute.remote is True:
            self.submit_remote(dependencies=dependencies)
        else:
            self.submit(dependencies=dependencies)
        return self

    def dict(self):
        """Return a dictionary representation of the job."""
        d = super().dict()
        d.update(
            {
                'method_name': self.method_name,
                'component_identifier': self.component_identifier,
                'type_id': self.type_id,
                '_path': 'superduperdb/jobs/job/ComponentJob',
            }
        )
        return d


def remote_job(identifier, dependencies=(), compute_kwargs: t.Union[str, t.Dict] = ""):
    """
    Remote Job to execute remote tasks.

    :param identifier: Job identifier.
    :param dependencies: List of dependencies.
    :param compute_kwargs: Compute kwargs.
    """
    # Connect to remote cluster
    import json

    from superduperdb import CFG
    from superduperdb.base.build import build_compute

    logging.info(f"Running remote job {identifier}")
    logging.info(f"Dependencies: {dependencies}")
    logging.info(f"Compute kwargs: {compute_kwargs}")

    if isinstance(compute_kwargs, str) and compute_kwargs:
        compute_kwargs = json.loads(compute_kwargs)

    compute = build_compute(CFG.cluster.compute)

    assert compute.remote is True, "Compute is not a distributed backend type."

    compute.execute_task(
        identifier, dependencies=dependencies, compute_kwargs=compute_kwargs
    )


def remote_task(identifier, dependencies=()):
    """
    Load job from job metadata and schedule it on remote cluster.

    :param identifier: Job identifier.
    :param dependencies: List of dependencies.
    """
    from superduperdb import CFG
    from superduperdb.base.build import build_datalayer

    # TODO: Make this run a predict job with multiple
    # chunks as tasks.
    db = build_datalayer(CFG, cluster__compute___path=None)

    info = db.metadata.get_job(identifier)

    args = info['args']
    kwargs = info['kwargs']
    path = info['_path']
    logging.info(f"Running remote task: {info}")

    if 'ComponentJob' in path:
        component_identifier = info['component_identifier']
        method_name = info['method_name']
        type_id = info['type_id']
        job = ComponentJob(
            args=args,
            kwargs=kwargs,
            method_name=method_name,
            component_identifier=component_identifier,
            type_id=type_id,
            db=db,
        )
    elif 'FunctionJob' in path:
        import importlib

        function = path.split('/')[-1]
        import_path, function = function.split(';')
        callable = getattr(importlib.import_module(import_path), function)

        job = FunctionJob(args=args, kwargs=kwargs, callable=callable, db=db)
    else:
        raise TypeError
    job.submit(dependencies=dependencies, update_job=True)
    return
