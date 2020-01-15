import botocore.session
from botocore.stub import Stubber

import ecrtools.main as main
import ecrtools.tests.stubber_responses as sr

ecr = botocore.session.get_session().create_client('ecr')
ctx = {'region': None, 'profile': None, 'ecr': ecr}
stubber = Stubber(ecr)


class TestImages(object):

    def test_images_empty(self, runner):
        expected_params = {'repositoryName': 'repo03'}
        stubber.add_response('describe_images',
                             sr.describe_images_repo03_empty,  expected_params)

        expected_result = 'No images found.\n'

        with stubber:
            result = runner.invoke(main.cli, ['images', 'repo03'], obj=ctx)

        assert result.exit_code == 1
        assert result.output == expected_result

    def test_images_list(self, runner):
        expected_params = {'repositoryName': 'repo01'}
        stubber.add_response('describe_images',
                             sr.describe_images_repo01,  expected_params)

        expected_result = '2016-11-02 00:00:00     0.1MB  1.0, master\n' \
            '2017-03-03 00:00:00    41.0MB  2.0, develop\n' \
            '2018-10-13 00:00:00  8192.0MB  3.0\n\n' \
            'images: 3 untagged: 0 total size: 8.2GB\n'

        with stubber:
            result = runner.invoke(main.cli, ['images', 'repo01'], obj=ctx)

        assert result.exit_code == 0
        assert result.output == expected_result
