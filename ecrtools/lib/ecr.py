import sys
import click
import functools

from botocore.exceptions import ClientError


def ecr_api_call(key, error_code='RepositoryNotFoundException',
                 error_message='Repository not found.'):
    def ecr_api_call_decorator(func):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            response = None
            repos = []
            while True:
                if response:
                    if 'NextMarker' not in response:
                        break
                    else:
                        kwargs['nextToken'] = response['NextMarker']
                try:
                    response = func(*args, **kwargs)
                except ClientError as e:
                    if e.response['Error']['Code'] == error_code:
                        click.echo(error_message, err=True)
                    else:
                        click.echo(e, err=True)
                    sys.exit(1)
                    click.exit(error_message)
                repos += response[key]
            return repos
        return wrapper_decorator
    return ecr_api_call_decorator


class Ecr(object):
    def __init__(self, client, repo=None):
        self.client = client
        self.repo = repo

    def get_image_ids(self, image, exact_match):
        params = {
            'repositoryName': self.repo,
            'maxResults': 100,
            'filter': {
                'tagStatus': 'ANY'
            },
        }
        images_ids = self.list_images(params)

        if exact_match:
            return [i for i in images_ids
                    if image == i.get('imageTag', '<untagged>')]
        return [i for i in images_ids
                if image in i.get('imageTag', '<untagged>')]

    def get_images(self, images_ids):
        params = {
            'repositoryName': self.repo,
            'imageIds': images_ids
        }
        return self.describe_images(params)

    @ecr_api_call('imageIds')
    def list_images(self, params):
        return self.client.list_images(**params)

    @ecr_api_call('imageDetails')
    def describe_images(self, params):
        return self.client.describe_images(**params)

    @ecr_api_call('repositories')
    def describe_repositories(self, **params):
        return self.client.describe_repositories(**params)
