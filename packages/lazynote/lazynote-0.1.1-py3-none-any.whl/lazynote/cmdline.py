import importlib
import sys
from pathlib import Path

import click
from click import Context

from lazynote import __version__
from lazynote.config import settings
from lazynote.log import init_log
from lazynote.manager import SimpleManager


def import_module_or_package(name_or_path):
    path = Path(name_or_path)
    if path.is_dir():
        # Assume it's a package path
        package_name = path.name
        package_dir = str(path.resolve().parent)
        sys.path.append(package_dir)
        module_or_package = importlib.import_module(package_name)
    else:
        # Assume it's a module name
        module_or_package = importlib.import_module(name_or_path)
    return module_or_package

def run_function(module_or_package, pattern, skip_modules):
    manager = SimpleManager(pattern=pattern)
    manager.traverse(module_or_package, skip_modules=skip_modules)

@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '-V',
    '--version',
    is_flag=True,
    help='Show version and exit.'
)  # If it's true, it will override `settings.VERBOSE`
@click.option('-v', '--verbose', is_flag=True, help='Show more info.')
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug.'
)  # If it's true, it will override `settings.DEBUG`
def main(ctx: Context, version: str, verbose: bool, debug: bool):
    """Main commands"""
    if version:
        click.echo(__version__)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        # Manually invoke the help of the run command
        click.echo('\nRun command help:')
        click.echo(ctx.command.get_command(ctx, 'run').get_help(ctx))
    else:
        if verbose:
            settings.set('VERBOSE', True)
        if debug:
            settings.set('DEBUG', True)

@main.command()
@click.argument('name_or_path')
@click.option('--pattern', default='fill', help='Pattern for SimpleManager')
@click.option('--skip-modules', default='', help='Comma-separated list of modules to skip')
def run(name_or_path, pattern, skip_modules):
    """Run command"""
    init_log()
    click.echo(f'Running with {name_or_path}')
    skip_modules_list = skip_modules.split(',') if skip_modules else []
    try:
        module_or_package = import_module_or_package(name_or_path)
        run_function(module_or_package, pattern, skip_modules_list)
        click.echo('Run completed successfully.')
    except Exception as e:
        click.echo(f'Error: {e}')


if __name__ == "__main__":
    main()
