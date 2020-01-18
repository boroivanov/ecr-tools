import botocore.session
from botocore.stub import Stubber

import ecrtools.main as main
import ecrtools.tests.stubber_responses as sr

ecr = botocore.session.get_session().create_client('ecr')
ctx = {'region': None, 'profile': None, 'ecr': ecr}
stubber = Stubber(ecr)


class TestRepos(object):

    def test_repos_empty(self, runner):
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_empty)

        expected_result = 'No repositories found.\n'

        with stubber:
            result = runner.invoke(main.cli, ['repos'], obj=ctx)

        assert result.exit_code == 1
        assert result.output == expected_result

    def test_repos_not_found(self, runner):
        expected_params = {'repositoryNames': ['missing']}
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_empty, expected_params)

        expected_result = 'No repositories found.\n'

        with stubber:
            result = runner.invoke(main.cli, ['repos', 'missing', '-a'],
                                   obj=ctx)

        assert result.exit_code == 1
        assert result.output == expected_result

    def test_repos_single_no_stats(self, runner):
        expected_params = {'repositoryNames': ['repo01']}
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_single,  expected_params)

        expected_result = 'repo01\n'

        with stubber:
            result = runner.invoke(main.cli, ['repos', 'repo01', '-a'],
                                   obj=ctx)

        assert result.exit_code == 0
        assert result.output == expected_result

    def test_repos_multiple_no_stats(self, runner):
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_multiple)

        expected_result = 'repo01\nrepo02\nrepo03\n'

        with stubber:
            result = runner.invoke(main.cli, ['repos', '-a'],
                                   obj=ctx)

        assert result.exit_code == 0
        assert result.output == expected_result

    def test_repos_single_with_stats(self, runner):
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_single)

        responses = {
            'list': sr.list_images_repo01,
            'desc': sr.describe_images_repo01,
        }

        self.stubber_image_stats('repo01', responses)

        with stubber:
            result = runner.invoke(main.cli, ['repos', 'repo01'],
                                   obj=ctx)

        expected_result = 'repo01  images:    3  untagged:   0  size:  12.3GB\n'

        assert result.exit_code == 0
        assert result.output == expected_result

    def test_repos_multiple_with_stats(self, runner):
        stubber.add_response('describe_repositories',
                             sr.describe_repositories_single)

        repos = {
            'repo01': {
                'list': sr.list_images_repo01,
                'desc': sr.describe_images_repo01,
            },
            # 'repo02': {
            #     'list': sr.list_images_repo02,
            #     'desc': sr.describe_images_repo02,
            # },
            # 'repo03': {
            #     'list': sr.list_images_repo03_empty,
            #     'desc': sr.describe_images_repo03_empty,
            # },
        }

        for k, v in repos.items():
            self.stubber_image_stats(k, v)

        with stubber:
            result = runner.invoke(main.cli, ['repos'],
                                   obj=ctx)

        expected_result = 'repo01  images:    3  untagged:   0  size:  12.3GB\n'

        assert result.exit_code == 0
        assert result.output == expected_result

    @staticmethod
    def stubber_image_stats(repo, response):
        # list images
        expected_params = {
            'repositoryName': repo,
            'maxResults': 100,
            'filter': {
                'tagStatus': 'ANY'
            },
        }
        stubber.add_response(
            'list_images', response['list'],  expected_params)

        # describe images
        ids = [i for i in response['list']['imageIds']]
        expected_params = {
            'repositoryName': 'repo01',
            'imageIds': ids,
        }
        imageDetails = [i for i in response['desc']['imageDetails']
                        if 'imageTags' in i]
        response = {'imageDetails': imageDetails}

        stubber.add_response('describe_images', response,  expected_params)
