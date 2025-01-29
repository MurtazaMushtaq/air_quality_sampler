# Air Quality Sampler

Author: Murtaza Mushtaq
Intended for use by: Farzad Panahi
Date Published: 2025-01-29
Date Available till: 2025-02-07

A Python module to sample and calculate average PM2.5 levels within a specified map bound.

## Installation

Using command line (cmd/bash), type the following command

pip install git+https://github.com/MurtazaMushtaq/air_quality_sampler.git

## Input

The module provides API to accept the following data:
    1. latitude_1, longitude_1, latitude_2, longitude_2: coordinates which represent a map bound
    2. sampling_period: in minutes (default = 5)
    3. sampling_rate: in samples per minute (default = 1)

## Output

The module provides API to get the following data:
    1. sampling_status: IDLE | RUNNING | DONE | FAILED | STOPPED
    2. avg_pm25_all_sites: Average PM2.5 of all stations over the sampling_period. This value should be valid when sampling_status is DONE.

## Actions

The module provides API to perform the following actions:
    1. Start/Stop sampling

## Sample Usage

See tests/test_sampler.py for examples
