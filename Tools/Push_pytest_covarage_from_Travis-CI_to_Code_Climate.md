# Push pytest covarage from Travis-CI to Code Climate

## .travis.yml

```
language: python

env:
  global:
    - CC_TEST_REPORTER_ID=test_reporter_id

python:
  - "3.6"

install:
  - pip install pytest pytest-cov

before_script:
  - curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
  - chmod +x ./cc-test-reporter
  - ./cc-test-reporter before-build

script:
  - python -m pytest --cov-report=xml --cov=module_or_package_name test_dir

after_script:
  - ./cc-test-reporter after-build --exit-code $TRAVIS_TEST_RESULT
```


## Pipenv

When you generate the test environment by `pipenv`, you may not have to
