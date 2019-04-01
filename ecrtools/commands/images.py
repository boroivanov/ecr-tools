import click

from ecrtools.lib.ecr import Ecr
from ecrtools.lib.utils import convert_bytes


@click.command()
@click.argument('repo')
@click.argument('image', default='', type=str, required=False)
@click.option('-c', '--count', type=int, default=None,
              help='Number of images to list.')
@click.option('-u', '--units', default='MB',
              type=click.Choice(['B', 'MB', 'GB']), help='Size units.')
@click.option('-w', '--exact-match', is_flag=True, help='Exact match.')
@click.pass_context
def images(ctx, repo, image, count, units, exact_match):
    '''List images in a repo'''

    ecr = Ecr(ctx.obj['ecr'], repo)
    image_ids = ecr.get_image_ids(image, exact_match)
    images = ecr.get_images(image_ids)
    images = sorted(images, reverse=True, key=lambda k: k['imagePushedAt'])

    total_size = 0
    total_untagged = 0
    for i in images[:count]:
        try:
            tags = ', '.join(i['imageTags'])
        except KeyError:
            tags = '<untagged>'
            total_untagged += 1
        total_size += i['imageSizeInBytes']
        size = convert_bytes(i['imageSizeInBytes'], units)
        click.echo(f'{i["imagePushedAt"]}  {size["value"]:.1f}{size["units"]}'
                   f'  {tags}')

    total_size = convert_bytes(total_size, 'GB')
    click.echo(f'\nimages: {len(images[:count])}'
               f' untagged: {total_untagged}'
               f' total size: {total_size["value"]:.1f}{total_size["units"]}')
