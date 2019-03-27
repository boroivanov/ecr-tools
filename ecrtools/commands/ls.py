import click


@click.command()
@click.pass_context
def ls(ctx):
    '''List repos'''
    print('this is the ls command')
