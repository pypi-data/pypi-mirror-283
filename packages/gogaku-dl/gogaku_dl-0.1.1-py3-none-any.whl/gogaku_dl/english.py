#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .gogaku_dl import (
    get_program_hls as _get_program_hls,
    get_programs)

TOP_URL = 'https://www.nhk.or.jp/gogaku/english/'


def get_program_titles():
    return list(get_programs(TOP_URL).keys())


def get_hls(title):
    return _get_program_hls(TOP_URL, title)


if __name__ == "__main__":
    print(get_program_hls(TOP_URL,
                          'エンジョイ・シンプル・イングリッシュ'))

