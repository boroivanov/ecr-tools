import queue
import sys
import threading

import click
import click_spinner

from ecrtools.lib.ecr import Ecr
from ecrtools.lib.utils import convert_bytes


@click.command()
@click.argument('names', required=False, nargs=-1)
@click.option('-a', '--all_stats', is_flag=True, default=True,
              help='Toggle stats (Default: True).')
@click.pass_obj
def repos(ctx, names, all_stats):
    '''List repos'''

    ecr = Ecr(ctx['ecr'])
    params = {}
    if len(names):
        params['repositoryNames'] = [name for name in names]

    repos = ecr.describe_repositories(**params)

    if not repos:
        sys.exit('No repositories found.')

    if not all_stats:
        click.echo('\n'.join(sorted([r['repositoryName'] for r in repos])))
        sys.exit(0)

    with click_spinner.spinner():
        stats = bulk_repo_stats(ctx, repos)
        stats = sorted(stats, key=lambda x: x['repositoryName'])
    print_repo_stats(ctx, stats)


def print_repo_stats(ctx, stats):
    repo_name_pad = len(max([r['repositoryName'] for r in stats], key=len))
    for repo in stats:
        total_size = 0
        total_untagged = 0
        click.echo(f"{repo['repositoryName']:{repo_name_pad}}", nl=False)
        if repo['stats']:
            for image in repo['stats']:
                if 'imageTags' not in image:
                    total_untagged += 1
                total_size += image['imageSizeInBytes']

        total_size = convert_bytes(total_size, 'GB')
        click.echo(f'  images: {len(repo["stats"]):4}'
                   f'  untagged: {total_untagged:3}'
                   f'  size: {total_size["value"]:5.1f}'
                   f'{total_size["units"]}')


def bulk_repo_stats(ctx, repos):
    q = queue.Queue()
    threads = []
    for repo in repos:
        t = threading.Thread(target=get_repo_stats, args=(ctx, repo, q))
        t.start()
        threads.append(t)

    [t.join() for t in threads]

    return [q.get(t) for t in threads]


def get_repo_stats(ctx, repo, q):
    ecr = Ecr(ctx['ecr'], repo['repositoryName'])
    image_ids = ecr.get_image_ids(image='', exact_match=False)

    stats = []
    if image_ids:
        stats = ecr.get_images(image_ids)

    q.put({
        'repositoryName': repo['repositoryName'],
        'stats': stats,
    })
