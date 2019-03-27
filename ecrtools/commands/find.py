import click


@click.command()
@click.pass_context
def find(ctx):
    '''Find images in a repo'''
    print('this is the find command')
