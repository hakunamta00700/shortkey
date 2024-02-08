from .start import console
from .ui import MyIcon
import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        run_console()
    

@cli.command('ui', short_help="with ui")
def run_ui():
    '''run shortkey with ui'''
    icon = MyIcon()
    icon.run()


@cli.command('console', short_help="with console")
def run_console():
    '''run shortkey with console'''
    console()


@cli.command('list', short_help="show shortkey list")
def show_list():
    '''show configured shortkey list'''
    print("list")
