# MemberAudit Dashboard Addon module for AllianceAuth.<a name="aa-memberaudit-dashboard"></a>

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Geuthur/aa-memberaudit-dashboard/master.svg)](https://results.pre-commit.ci/latest/github/Geuthur/aa-memberaudit-dashboard/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checks](https://github.com/Geuthur/aa-memberaudit-dashboard/actions/workflows/autotester.yml/badge.svg)](https://github.com/Geuthur/aa-memberaudit-dashboard/actions/workflows/autotester.yml)
[![codecov](https://codecov.io/gh/Geuthur/aa-memberaudit-dashboard/graph/badge.svg?token=yPAkMfj3cD)](https://codecov.io/gh/Geuthur/aa-memberaudit-dashboard)

- [AA MemberAudit Dashboard](#aa-memberaudit-dashboard)
  - [Features](#features)
  - [Upcoming](#upcoming)
  - [Installation](#features)
    - [Step 1 - Install the Package](#step1)
    - [Step 2 - Configure Alliance Auth](#step2)
    - [Step 3 - Migration to AA](#step3)
  - [Highlights](#highlights)

## Features<a name="features"></a>

- Show not registred Characters on Dashboard

## Upcoming<a name="upcoming"></a>

- More Information in Dashboard

## Installation<a name="installation"></a>

> \[!NOTE\]
> AA MemberAudit Dashboard needs at least Alliance Auth v4.0.0
> Please make sure to update your Alliance Auth before you install this APP

### Step 1 - Install the Package<a name="step1"></a>

Make sure you're in your virtual environment (venv) of your Alliance Auth then install the pakage.

```shell
pip install aa-memberaudit-dashboard
```

### Step 2 - Configure Alliance Auth<a name="step2"></a>

Configure your Alliance Auth settings (`local.py`) as follows:

- Add `'memberaudit',` to `INSTALLED_APPS`
- Add `'madashboard',` to `INSTALLED_APPS`

### Step 3 - Migration to AA<a name="step3"></a>

```shell
python manage.py collectstatic
python manage.py migrate
```

## Highlights<a name="highlights"></a>

![Screenshot 2024-06-09 164402](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/5bf9eb99-1d61-4562-9bb3-02f9d3ae3ac2)
![Screenshot 2024-06-09 164408](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/5a79ca79-145a-4558-befc-2b0529675712)
![Screenshot 2024-06-09 164431](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/b79f1519-0a70-483b-9def-3ec120e4cd46)
![Screenshot 2024-06-09 164502](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/1249d415-9d72-4cf0-8c62-d1ac4db72986)
![Screenshot 2024-06-09 164516](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/66608190-42db-4780-9b10-c8832d96cb2d)
![Screenshot 2024-06-09 164508](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/c989d2ed-6602-441b-b903-b7f22ecf69c0)
![Screenshot 2024-06-10 235804](https://github.com/Geuthur/aa-memberaudit-dashboard/assets/761682/e0c816e6-2b5b-421f-add3-57628ad05004)

> \[!NOTE\]
> Contributing
> You want to improve the project?
> Just Make a [Pull Request](https://github.com/Geuthur/aa-memberaudit-dashboard/pulls) with the Guidelines.
> We Using pre-commit
