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
