import os
from argparse import ArgumentParser

from argcomplete import autocomplete


def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('install', help='install packages')
    subparser.set_defaults(func='install')
    subparser.add_argument('pkgs', nargs='+', metavar='pkg')

    subparser = subparsers.add_parser('update', help='update all packages in the workspace to the latest version')
    subparser.set_defaults(func='update')

    subparser = subparsers.add_parser('list', help='list all installed packages')
    subparser.set_defaults(func='list_installed')

    subparser = subparsers.add_parser('remove', help='remove packages')
    subparser.set_defaults(func='remove')
    subparser.add_argument('pkgs', nargs='+', metavar='pkg')

    # workspace commands
    subparser = subparsers.add_parser(
        'ws-create',
        help='create a new workspace',
        description='Create a new catkin workspace where the packages are managed by ros-get')
    subparser.set_defaults(func='create')
    subparser.add_argument(
        'rosdistro_index_url',
        help='Custom rosdistro database url. This can be either a web url (http://) or local file url (file://).')
    subparser.add_argument(
        'extend_path',
        metavar='extend',
        help='Explicitly extend the result-space of another catkin workspace. Example: /opt/ros/kinetic')
    subparser.add_argument(
        '--dir',
        default=os.getcwd(),
        help='The directory to create the workspace in. Defaults to the current working directory')
    subparser.add_argument(
        '--name', help='give a name to the workspace, if not given, the name '
        'will be inferred by the directory name')

    subparser = subparsers.add_parser('ws-switch', help='switch to a workspace')
    subparser.set_defaults(func='switch')
    subparser.add_argument('name')

    subparser = subparsers.add_parser('ws-save', help='Saves the current workspace')
    subparser.set_defaults(func='save')
    subparser.add_argument('dir')
    subparser.add_argument(
        '--name', help='give a name to the workspace, if not given, the name will be inferred by the directory name')

    subparser = subparsers.add_parser('ws-list', help='list all saved workspaces')
    subparser.set_defaults(func='list_workspaces')

    subparser = subparsers.add_parser('ws-locate', help='prints the path to the current workspace')
    subparser.set_defaults(func='locate')

    subparser = subparsers.add_parser('ws-name', help='prints the name of the current workspace')
    subparser.set_defaults(func='name')

    subparser = subparsers.add_parser('ws-rosdistro-url', help='Prints the current rosdistro_index_url')
    subparser.set_defaults(func='rosdistro_url')

    autocomplete(parser)
    args = parser.parse_args()

    # computation has to be avoided before the 'autocomplete(parser)' call

    import logging.config
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s[%(levelname)s] %(name)s: %(message)s",
            }
        },
        'handlers': {
            'stream': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
            },
        },
        'loggers': {
            'vcstool.executor': {
                'level': 'INFO',
            }
        },
        'root': {
            'handlers': ['stream'],
            'level': 'INFO',
        },
    })

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    from . import (install, update, list_installed, remove, create, switch, save, list_workspaces, locate, name,
                   rosdistro_url)

    # remove func from the namespace
    func = args.func
    del args.func

    # execute the function given in 'func'
    func = {
        'install': install,
        'update': update,
        'list_installed': list_installed,
        'remove': remove,
        'create': create,
        'switch': switch,
        'save': save,
        'list_workspaces': list_workspaces,
        'locate': locate,
        'name': name,
        'rosdistro_url': rosdistro_url,
    }[func]
    exit(func(**vars(args)))


if __name__ == '__main__':
    main()
