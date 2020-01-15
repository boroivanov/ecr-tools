from datetime import datetime

describe_repositories_empty = {
    'repositories': [],
}

describe_repositories_single = {
    'repositories': [
        {
            'repositoryArn': 'arn:aws:ecr:us-east-1:123456789123:repository/repo01',
            'registryId': '123456789123',
            'repositoryName': 'repo01',
            'repositoryUri': '123456789123.dkr.ecr.us-east-1.amazonaws.com/repo01',
            'createdAt': datetime(2015, 1, 1),
            'imageTagMutability': 'MUTABLE',
            'imageScanningConfiguration': {
                'scanOnPush': False
            }
        },
    ],
}

describe_repositories_multiple = {
    'repositories': [
        {
            'repositoryArn': 'arn:aws:ecr:us-east-1:123456789123:repository/repo01',
            'registryId': '123456789123',
            'repositoryName': 'repo01',
            'repositoryUri': '123456789123.dkr.ecr.us-east-1.amazonaws.com/repo01',
            'createdAt': datetime(2015, 1, 1),
            'imageTagMutability': 'MUTABLE',
            'imageScanningConfiguration': {
                'scanOnPush': False
            }
        },
        {
            'repositoryArn': 'arn:aws:ecr:us-east-1:123456789123:repository/repo02',
            'registryId': '123456789123',
            'repositoryName': 'repo02',
            'repositoryUri': '123456789123.dkr.ecr.us-east-1.amazonaws.com/repo02',
            'createdAt': datetime(2015, 1, 1),
            'imageTagMutability': 'MUTABLE',
            'imageScanningConfiguration': {
                'scanOnPush': False
            }
        },
        {
            'repositoryArn': 'arn:aws:ecr:us-east-1:123456789123:repository/repo03',
            'registryId': '123456789123',
            'repositoryName': 'repo03',
            'repositoryUri': '123456789123.dkr.ecr.us-east-1.amazonaws.com/repo03',
            'createdAt': datetime(2015, 1, 1),
            'imageTagMutability': 'MUTABLE',
            'imageScanningConfiguration': {
                'scanOnPush': False
            }
        },
    ],
}

list_images_empty = {
    'imageIds': [],
}

list_images_repo01 = {
    'imageIds': [
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4a6d',
            'imageTag': '1.0'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4a6d',
            'imageTag': 'master'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4123',
            'imageTag': '2.0'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4123',
            'imageTag': 'develop'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4456',
            'imageTag': '3.0'
        },
    ],
}

list_images_repo02 = {
    'imageIds': [
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4a6d',
            'imageTag': '1.0'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4123',
            'imageTag': '<untagged>'
        },
        {
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4456',
            'imageTag': '<untagged>'
        },
    ],
}

describe_images_repo03_empty = {
    'imageIds': [
    ],
}

describe_images_repo01 = {
    'imageDetails': [
        {
            'registryId': '123456789123',
            'repositoryName': 'repo01',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4a6d',
            'imageTags': [
                '1.0',
                'master',
            ],
            'imageSizeInBytes': 123000,
            'imagePushedAt': datetime(2016, 11, 2),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo01:1.0'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2016, 11, 2),
                'vulnerabilitySourceUpdatedAt': datetime(2016, 11, 2),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
        {
            'registryId': '123456789123',
            'repositoryName': 'repo01',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4123',
            'imageTags': [
                '2.0',
                'develop',
            ],
            'imageSizeInBytes': 40960000,
            'imagePushedAt': datetime(2017, 3, 3),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo01:2.0'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2017, 3, 3),
                'vulnerabilitySourceUpdatedAt': datetime(2017, 3, 3),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
        {
            'registryId': '123456789123',
            'repositoryName': 'repo01',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4456',
            'imageTags': [
                '3.0',
            ],
            'imageSizeInBytes': 8192000000,
            'imagePushedAt': datetime(2018, 10, 13),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo01:3.0'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2018, 10, 13),
                'vulnerabilitySourceUpdatedAt': datetime(2018, 10, 13),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
    ],
}

describe_images_repo02 = {
    'imageDetails': [
        {
            'registryId': '123456789123',
            'repositoryName': 'repo02',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4a6d',
            'imageTags': [
                '1.0',
            ],
            'imageSizeInBytes': 1230000,
            'imagePushedAt': datetime(2019, 2, 21),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo02:1.0'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2019, 2, 21),
                'vulnerabilitySourceUpdatedAt': datetime(2019, 2, 21),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
        {
            'registryId': '123456789123',
            'repositoryName': 'repo02',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4123',
            'imageTags': [
                '<untagged>',
            ],
            'imageSizeInBytes': 4096000000,
            'imagePushedAt': datetime(2019, 1, 1),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo02:<untagged> #1'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2019, 1, 1),
                'vulnerabilitySourceUpdatedAt': datetime(2019, 1, 1),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
        {
            'registryId': '123456789123',
            'repositoryName': 'repo02',
            'imageDigest': 'sha256:01125a4ccb76d3e281199ea04ee496a560c636f858df617b67e7d971d17a4456',
            'imageTags': [
                '<untagged>',
            ],
            'imageSizeInBytes': 8192000000,
            'imagePushedAt': datetime(2020, 1, 14),
            'imageScanStatus': {
                'status': 'COMPLETE',
                'description': 'repo02:<untagged> #2'
            },
            'imageScanFindingsSummary': {
                'imageScanCompletedAt': datetime(2020, 1, 14),
                'vulnerabilitySourceUpdatedAt': datetime(2020, 1, 14),
                'findingSeverityCounts': {
                    'string': 123
                }
            }
        },
    ],
}

describe_images_repo03_empty = {
    'imageDetails': []
}
