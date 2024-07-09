import os
import subprocess
import sys
import time
import typing as t

SESSION_NAME = 'superduperdb-local-cluster-session'


def create_tmux_session(session_name, commands):
    """Create a tmux local cluster.

    :param session_name: name of the tmux session
    :param commands: list of commands to run
    """
    for ix, cmd in enumerate(commands, start=0):
        window_name = f'{session_name}:{ix}'
        run_tmux_command(['send-keys', '-t', window_name, cmd, 'C-m'])
        time.sleep(1)

    print('You can attach to the tmux session with:')
    print(f'tmux a -t {session_name}')


def run_tmux_command(command):
    """Run a tmux command.

    :param command: command to run
    """
    print('tmux ' + ' '.join(command))
    subprocess.run(["tmux"] + command, check=True)


def up_cluster(
    notebook_token: t.Optional[str] = None,
    num_workers: int = 0,
    attach: bool = True,
    cdc: bool = False,
):
    """Start the local cluster.

    :param notebook_token: token to use for the jupyter notebook
    """
    print('Starting the local cluster...')

    CFG = os.environ.get('SUPERDUPERDB_CONFIG')
    assert CFG, 'Please set SUPERDUPERDB_CONFIG environment variable'
    python_executable = sys.executable
    python_executable_dir = os.path.dirname(python_executable)
    ray_path = os.popen('which ray').read().split('\n')[0].strip()
    ray_executable = os.path.join(os.path.dirname(python_executable), ray_path)
    run_tmux_command(
        [
            'new-session',
            '-d',
            '-s',
            SESSION_NAME,
        ]
    )

    run_tmux_command(['rename-window', '-t', f'{SESSION_NAME}:0', 'ray-head'])
    run_tmux_command(['new-window', '-t', f'{SESSION_NAME}:1', '-n', 'vector-search'])
    run_tmux_command(['new-window', '-t', f'{SESSION_NAME}:2', '-n', 'rest'])
    run_tmux_command(['new-window', '-t', f'{SESSION_NAME}:3', '-n', 'jupyter'])
    for i in range(num_workers):
        run_tmux_command(
            ['new-window', '-t', f'{SESSION_NAME}:{4 + i}', '-n', f'ray-worker-{i}']
        )
    if cdc:
        run_tmux_command(
            ['new-window', '-t', f'{SESSION_NAME}:{4 + num_workers}', '-n', 'cdc']
        )

    cmd = (
        f"export PATH={python_executable_dir}:$PATH; "
        f"SUPERDUPERDB_CONFIG={CFG} PYTHONPATH=$(pwd):. {ray_executable} start"
        " --head --dashboard-host=0.0.0.0 --disable-usage-stats --block"
    )
    run_tmux_command(['send-keys', '-t', f'{SESSION_NAME}:ray-head', cmd, 'C-m'])
    time.sleep(10)
    cmd = (
        f"SUPERDUPERDB_CONFIG={CFG} "
        "RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1 PYTHONPATH=$(pwd)"
        f":. {ray_executable} start --address=localhost:6379  --block"
    )
    for i in range(num_workers):
        run_tmux_command(
            ['send-keys', '-t', f'{SESSION_NAME}:ray-worker-{i}', cmd, 'C-m']
        )
    cmd = f"SUPERDUPERDB_CONFIG={CFG} {python_executable} -m superduperdb vector-search"
    run_tmux_command(['send-keys', '-t', f'{SESSION_NAME}:vector-search', cmd, 'C-m'])
    if cdc:
        cmd = f"SUPERDUPERDB_CONFIG={CFG} {python_executable} -m superduperdb cdc"
        run_tmux_command(['send-keys', '-t', f'{SESSION_NAME}:cdc', cmd, 'C-m'])
    cmd = f"SUPERDUPERDB_CONFIG={CFG} {python_executable} -m superduperdb rest"
    run_tmux_command(['send-keys', '-t', f'{SESSION_NAME}:rest', cmd, 'C-m'])
    cmd = (
        f"SUPERDUPERDB_CONFIG={CFG} {python_executable} -m jupyter lab "
        f"--no-browser --ip=0.0.0.0 --NotebookApp.token={notebook_token} --allow-root"
        if notebook_token
        else (
            f"SUPERDUPERDB_CONFIG={CFG} {python_executable} -m "
            "jupyter lab --no-browser --ip=0.0.0.0"
        )
    )
    run_tmux_command(['send-keys', '-t', f'{SESSION_NAME}:jupyter', cmd, 'C-m'])

    print('You can attach to the tmux session with:')
    print(f'tmux a -t {SESSION_NAME}')
    print(f'local cluster started with tmux session {SESSION_NAME}')

    if attach:
        attach_cluster()


def down_cluster():
    """Stop the local cluster."""
    print('Stopping the local cluster...')
    run_tmux_command(['kill-session', '-t', SESSION_NAME])
    print('local cluster stopped')


def attach_cluster():
    """Attach to the tmux session."""
    run_tmux_command(['attach-session', '-t', SESSION_NAME])
