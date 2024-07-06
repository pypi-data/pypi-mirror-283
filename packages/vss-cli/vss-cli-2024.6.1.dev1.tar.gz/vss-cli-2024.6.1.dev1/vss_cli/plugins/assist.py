"""AI assistant."""
import logging

import click

from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.utils.emoji import EMOJI_UNICODE

_LOGGING = logging.getLogger(__name__)

ej_robot = EMOJI_UNICODE.get(':robot_face:')

we_message = f"""Hello, I’m UTORcloudy {ej_robot}, the ITS
Private Cloud virtual agent.I can help with account, virtual
machine management, billing questions and more. 🚀"""


@click.command('assist', short_help='VSS AI Assistant')
@click.option(
    '--no-load', is_flag=True, default=False, help='do not load config'
)
@click.argument(
    "message",
    required=False,
)
@pass_context
def cli(ctx: Configuration, no_load: bool, message: str):
    """Manage your VSS account."""
    with ctx.spinner(disable=ctx.debug) as spinner_cls:
        if not no_load:
            ctx.load_config(spinner_cls=spinner_cls)
        if not message:
            spinner_cls.stop()
            ctx.secho(we_message)
            message = click.prompt("How may I assist you?", type=str)
            ctx.echo("")
            spinner_cls.start()
        ctx.ask_assistant(spinner_cls=spinner_cls, message=message)
