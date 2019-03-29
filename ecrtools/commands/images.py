import sys
import click
from botocore.exceptions import ClientError


@click.command()
@click.argument('repo')
@click.argument('image', default='', type=str, required=False)
@click.pass_context
def images(ctx, repo, image):
    '''List images in a repo'''
    params = {
        'repositoryName': repo,
        'maxResults': 100,
        'filter': {
            'tagStatus': 'ANY'
        },
    }

    images = list_images(ctx, params)
    print('\n'.join(sorted([img['imageTag'] for img in images
                            if image in img['imageTag']])))


def list_images(ctx, params={}):
    response = None
    repos = []
    while True:
        if response:
            if 'NextMarker' not in response:
                break
            else:
                params['nextToken'] = response['NextMarker']
        try:
            response = ctx.obj['ecr'].list_images(**params)
        except ClientError as e:
            if e.response['Error']['Code'] == 'RepositoryNotFoundException':
                click.echo('Repository not found.', err=True)
            else:
                click.echo(e, err=True)
            sys.exit(1)
            click.exit('Repository not found.')
        repos += response['imageIds']
    return repos
