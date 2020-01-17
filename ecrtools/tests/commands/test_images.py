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
            '2017-03-03 00:00:00  4096.0MB  2.0, develop\n' \
            '2018-10-13 00:00:00  8192.0MB  3.0\n\n' \
            'images: 3 untagged: 0 total size: 12.3GB\n'

        with stubber:
            result = runner.invoke(main.cli, ['images', 'repo01'], obj=ctx)

        assert result.exit_code == 0
        assert result.output == expected_result

    def test_images_list_with_image(self, runner):
        # list_images
        expected_params = {
            'repositoryName': 'repo01',
            'maxResults': 100,
            'filter': {
                'tagStatus': 'ANY'
            },
        }
        stubber.add_response('list_images',
                             sr.list_images_repo01,  expected_params)

        # describe_images
        ids = [i for i in sr.list_images_repo01['imageIds']
               if i['imageTag'] == 'develop']
        expected_params = {
            'repositoryName': 'repo01',
            'imageIds': ids,
        }
        imageDetails = [i for i in sr.describe_images_repo01['imageDetails']
                        if 'develop' in i['imageTags']]
        response = {'imageDetails': imageDetails}
        stubber.add_response('describe_images', response,  expected_params)

        expected_result = '2017-03-03 00:00:00  4096.0MB  2.0, develop\n\n' \
            'images: 1 untagged: 0 total size: 4.1GB\n'

        with stubber:
            result = runner.invoke(main.cli, ['images', 'repo01', 'develop'],
                                   obj=ctx)

        assert result.output == expected_result
        assert result.exit_code == 0
