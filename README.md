[![Latest PyPI version](https://img.shields.io/pypi/v/ecrtools.svg)](https://pypi.python.org/pypi/ecrtools)
[![Build Status](https://travis-ci.org/boroivanov/ecr-tools.svg)](https://travis-ci.org/boroivanov/ecr-tools)
[![Maintainability](https://api.codeclimate.com/v1/badges/0dd8340bb879a7969cce/maintainability)](https://codeclimate.com/github/boroivanov/ecr-tools/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/0dd8340bb879a7969cce/test_coverage)](https://codeclimate.com/github/boroivanov/ecr-tools/test_coverage)
[![Downloads](https://pepy.tech/badge/ecrtools)](https://pepy.tech/project/ecrtools)
[![Downloads](https://pepy.tech/badge/ecrtools/month)](https://pepy.tech/project/ecrtools)

# ecrtools

ecrtools is a small cli for listing ECR repos and searching for images in ECR. Easily print repos and images stats


# Install
*NOTE: Python 3 support only.*
```
pip install ecrtools
```

# Examples

```bash
$ ecr repos
my-app               images:   82  untagged:   3  size:  33.9GB
my-app-auto-tests    images:    5  untagged:   0  size:   2.5GB
....

$ ecr images my-app f5f84a5
2019-03-19 14:56:42-07:00  438.7MB  f5f84a5
2019-03-19 14:56:34-07:00  417.2MB  awscp-f5f84a5

images: 2 untagged: 0 total size: 0.9GB

$ ecr images my-app head
2019-04-01 18:14:39-07:00  378.3MB  rev-source-update, 742f07e, head

images: 1 untagged: 0 total size: 0.4GB

$ ecr images my-app
2019-04-01 18:14:39-07:00  378.3MB  rev-source-update, 742f07e, head
2019-04-01 18:14:31-07:00  378.3MB  pr-1376
....

images: 82 untagged: 3 total size: 33.9GB
```
