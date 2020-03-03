import os
import string
import sys

import boto3
import click
from botocore.exceptions import NoRegionError, ProfileNotFound

version = '0.0.7'


class Subcommand(click.MultiCommand):
    plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

    def list_commands(self, ctx):
        rv = []
        alpha = string.ascii_letters
        for filename in os.listdir(self.plugin_folder):
            if filename.startswith(tuple(alpha)) and filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(self.plugin_folder, name + '.py')
        if not os.path.isfile(fn):
            click.echo('Command not found: %s' % name)
            sys.exit(1)
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns[name]


@click.group(cls=Subcommand)
@click.pass_context
@click.version_option(version=version, message=version)
@click.option('-p', '--profile', help='AWS profile')
@click.option('-r', '--region', help='AWS region')
def cli(ctx, region, profile):
    '''AWS ECR tools'''
    try:
        sess = boto3.session.Session(profile_name=profile, region_name=region)
    except ProfileNotFound as e:
        click.echo(e, err=True)
        sys.exit(1)

    try:
        ecr = sess.client('ecr')
    except NoRegionError as e:
        click.echo(e, err=True)
        sys.exit(1)

    if not ctx.obj:
        ctx.obj = {
            'region': region,
            'profile': profile,
            'ecr': ecr,
        }


if __name__ == '__main__':
    cli()
