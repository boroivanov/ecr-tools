import sys
import click
from botocore.exceptions import ClientError


@click.command()
@click.argument('repo')
@click.argument('image', default='', type=str, required=False)
@click.option('-c', '--count', type=int, default=None,
              help='Number of images to list')
@click.option('-w', '--exact-match', is_flag=True, help='Exact match')
@click.pass_context
def images(ctx, repo, image, count, exact_match):
    '''List images in a repo'''

    image_ids = get_image_ids(ctx, repo, image, exact_match)
    images = get_images(ctx, repo, image_ids)
    images = sorted(images, reverse=True, key=lambda k: k['imagePushedAt'])

    for i in images[:count]:
        tags = ', '.join(i['imageTags'])
        size = convert_bytes(i['imageSizeInBytes'], 'MB')
        click.echo(f'{i["imagePushedAt"]}  {size["value"]:.2f}{size["metric"]}'
                   f'  {tags}')


def get_image_ids(ctx, repo, image, exact_match):
    params = {
        'repositoryName': repo,
        'maxResults': 100,
        'filter': {
            'tagStatus': 'ANY'
        },
    }
    images_ids = list_images(ctx, params)

    if exact_match:
        return [i for i in images_ids if image == i['imageTag']]
    return [i for i in images_ids if image in i['imageTag']]


def get_images(ctx, repo, images_ids):
    params = {
        'repositoryName': repo,
        'imageIds': images_ids
    }
    return describe_images(ctx, params)


def convert_bytes(n, metric='MB'):
    if metric == 'GB':
        return {'value': n / 1000 / 1000 / 1000, 'metric': 'GB'}
    elif metric == 'MB':
        return {'value': n / 1000 / 1000 / 1000, 'metric': 'MB'}
    else:
        return {'value': n, 'metric': 'B'}


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


def describe_images(ctx, params={}):
    response = None
    repos = []
    while True:
        if response:
            if 'NextMarker' not in response:
                break
            else:
                params['nextToken'] = response['NextMarker']
        try:
            response = ctx.obj['ecr'].describe_images(**params)
        except ClientError as e:
            if e.response['Error']['Code'] == 'RepositoryNotFoundException':
                click.echo('Repository not found.', err=True)
            else:
                click.echo(e, err=True)
            sys.exit(1)
            click.exit('Repository not found.')
        repos += response['imageDetails']
    return repos
