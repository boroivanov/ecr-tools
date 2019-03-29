import click


@click.command()
@click.argument('names', required=False, nargs=-1)
@click.pass_context
def repos(ctx, names):
    '''List repos'''
    params = {}
    if len(names):
        params['repositoryNames'] = [name for name in names]

    repos = describe_repositories(ctx, params)
    print('\n'.join(sorted([r['repositoryName'] for r in repos])))


def describe_repositories(ctx, params={}):
    response = None
    repos = []
    while True:
        if response:
            if 'NextMarker' not in response:
                break
            else:
                params['nextToken'] = response['NextMarker']
        response = ctx.obj['ecr'].describe_repositories(**params)
        repos += response['repositories']
    return repos
