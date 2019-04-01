import click

from ecrtools.lib.ecr import Ecr


@click.command()
@click.argument('names', required=False, nargs=-1)
@click.pass_context
def repos(ctx, names):
    '''List repos'''

    ecr = Ecr(ctx.obj['ecr'])
    params = {}
    if len(names):
        params['repositoryNames'] = [name for name in names]

    repos = ecr.describe_repositories(params)
    click.echo('\n'.join(sorted([r['repositoryName'] for r in repos])))
