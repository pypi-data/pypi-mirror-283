#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
from random import randrange
from time import sleep
from datetime import datetime


API_URL_HINT = 'ondemand_detail.js'
MIN_SLEEP_SECONDS = 1
MAX_SLEEP_SECONDS = 5


def _mitigating_sleep():
    sleep_seconds = randrange(MIN_SLEEP_SECONDS, MAX_SLEEP_SECONDS)
    sleep(sleep_seconds)


def get_programs(topurl):
    _mitigating_sleep()

    programs = {}

    response = requests.get(topurl)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    programs_elements = soup.css.select('#listRadio .boxbody')
    for program in programs_elements:
        url = program.find(
            'a',
            attrs={'href': re.compile(r'radio/ondemand/detail.html\?p=')})
        if url is None:
            continue
        title = program.find(attrs={'class': 'programtitle'}).text
        programs[title] = url['href']

    return programs


def _get_api_url(url):
    _mitigating_sleep()

    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    relurl = soup.find(attrs={'src': re.compile(API_URL_HINT)})

    jscode = requests.get(urljoin(url, relurl['src']))
    jscode.encoding = 'utf-8'
    uris = re.search(r'rapiuri="(https:.*?)";', jscode.text, re.M)

    return uris[1]


def get_program_details(topurl):
    programs = get_programs(topurl)
    api_url = _get_api_url(
        list(programs.values())[0])

    program_details = {}
    for title, url in programs.items():
        program_info = re.search(r'p=(\d+)_(\d+)', url)
        program_details[title] = api_url.format(
            siteid=program_info[1],
            cornerid=program_info[2])

    return program_details


def _get_fiscal_year(onair_date, close_date):
    fiscal_year = int(close_date[:4])
    onair_month = int(re.search(
        r'(\d+)月', onair_date)[1])

    if 1 <= onair_month < 4:
        fiscal_year = onair_month - 1

    return fiscal_year


def _get_length_in_sec(contents_id: str) -> int:
    time_token = contents_id.split(';')[-1]
    times = [x.replace('+09:00', '') for x in time_token.split('_')]

    start_time = datetime.strptime(
        times[0], '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime(
        times[1], '%Y-%m-%dT%H:%M:%S')

    return (end_time - start_time).total_seconds()


def get_program_hls(topurl, title):
    programs = get_program_details(topurl)
    if title not in programs:
        raise RuntimeError(f'{title} does not exist')
    program_detail_url = programs[title]
    program_hls = {}
    program_hls['title'] = title
    program_hls['detail_url'] = program_detail_url
    program_hls['episodes'] = []

    _mitigating_sleep()
    response = requests.get(program_detail_url)
    response.encoding = 'utf-8'
    program_data = response.json()

    for datum in program_data['episodes']:
        if 'fiscal_year' not in program_hls:
            program_hls['fiscal_year'] = _get_fiscal_year(
                datum['onair_date'],
                datum['closed_at'])

        program_hls['episodes'].append({
            datum['program_title']: {
                'onair': datum['onair_date'],
                'len_in_sec': _get_length_in_sec(
                    datum['aa_contents_id']),
                'hls': datum['stream_url']
            }})

    return program_hls
