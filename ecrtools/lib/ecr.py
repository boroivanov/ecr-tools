import sys
import click

from botocore.exceptions import ClientError


class Ecr(object):
    def __init__(self, client, repo):
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

    def list_images(self, params={}):
        response = None
        repos = []
        while True:
            if response:
                if 'NextMarker' not in response:
                    break
                else:
                    params['nextToken'] = response['NextMarker']
            try:
                response = self.client.list_images(**params)
            except ClientError as e:
                e_code = 'RepositoryNotFoundException'
                if e.response['Error']['Code'] == e_code:
                    click.echo('Repository not found.', err=True)
                else:
                    click.echo(e, err=True)
                sys.exit(1)
                click.exit('Repository not found.')
            repos += response['imageIds']
        return repos

    def describe_images(self, params={}):
        response = None
        repos = []
        while True:
            if response:
                if 'NextMarker' not in response:
                    break
                else:
                    params['nextToken'] = response['NextMarker']
            try:
                response = self.client.describe_images(**params)
            except ClientError as e:
                e_code = 'RepositoryNotFoundException'
                if e.response['Error']['Code'] == e_code:
                    click.echo('Repository not found.', err=True)
                else:
                    click.echo(e, err=True)
                sys.exit(1)
                click.exit('Repository not found.')
            repos += response['imageDetails']
        return repos
