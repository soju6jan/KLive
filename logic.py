# -*- coding: utf-8 -*-
#########################################################
# python
import os
import datetime
import traceback
import logging
import subprocess
import time
import re
import json
import requests
import urllib
import urllib2
import lxml.html
import threading
from enum import Enum

# third-party
from sqlalchemy import desc
from sqlalchemy import or_, and_, func, not_
from telepot import Bot, glance
from telepot.loop import MessageLoop
from time import sleep
import telepot

# sjva 공용
from framework.logger import get_logger
from framework import app, db, scheduler, path_app_root
from framework.job import Job
from framework.util import Util
from system.logic import SystemLogic

# 패키지
from .model import ModelSetting, ModelChannel
import plex 
from .logic_klive import LogicKlive

# 로그
package_name = __name__.split('.')[0]
logger = get_logger(package_name)

#########################################################

class Logic(object):
    db_default = {
        'db_version' : '1',
        'use_wavve' : 'True',
        'wavve_id' : '',
        'wavve_pw' : '',
        'wavve_quality' : 'HD',
        'wavve_streaming_type' : '1',
        'wavve_use_proxy' : 'False',
        'wavve_proxy_url' : '',

        'use_tving' : 'False',
        'tving_id' : '',
        'tving_pw' : '',
        'tving_quality' : 'HD',
        'tving_use_proxy' : 'False',
        'tving_proxy_url' : '',

        'use_videoportal' : 'True',

        'use_everyon' : 'True',

        'use_youtubedl' : 'False',
        'youtubedl_use_proxy' : 'False',
        'youtubedl_proxy_url' : '',
        'youtubedl_list' : u'1|한국프로야구1|https://twitch.tv/kbo1\n2|한국프로야구2|https://twitch.tv/kbo2\n3|한국프로야구3|https://twitch.tv/kbo3\n4|한국프로야구4|https://twitch.tv/kbo4\n5|한국프로야구5|https://twitch.tv/kbo5\n6|YTN|https://youtube.com/watch?v=U_sYIKWhJvk\n7|맛있는 녀석들|https://youtube.com/watch?v=VykycecFVoc\n8|THE K-POP|https://youtube.com/watch?v=0Cs_o3daYR8\n9|장군의 아들|https://youtube.com/watch?v=EidX2DPPSBw\n',

        'use_streamlink' : 'False',
        'streamlink_quality' : 'best',
        'streamlink' : 'False',
        'streamlink_list' : u'1|한국프로야구1|https://twitch.tv/kbo1\n2|한국프로야구2|https://twitch.tv/kbo2\n3|한국프로야구3|https://twitch.tv/kbo3\n4|한국프로야구4|https://twitch.tv/kbo4\n5|한국프로야구5|https://twitch.tv/kbo5\n6|2010년 히트곡|https://dailymotion.com/video/x77q22e',

        'use_navertv' : 'False',
        'navertv_list' : u'1|연합뉴스TV|https://tv.naver.com/l/44267\n2|TBS|https://tv.naver.com/l/43164|720',

        'use_kakaotv' : 'False',
        'kakaotv_list' : u'1|KBS24|https://tv.kakao.com/channel/3193314/livelink/7742194\n2|추억의 90년대 가요|https://tv.kakao.com/channel/3112354/livelink/7836404',

    }

    @staticmethod
    def db_init():
        try:
            for key, value in Logic.db_default.items():
                if db.session.query(ModelSetting).filter_by(key=key).count() == 0:
                    db.session.add(ModelSetting(key, value))
            db.session.commit()
            Logic.migration()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
        
    @staticmethod
    def plugin_load():
        try:
            Logic.db_init()
            from plugin import plugin_info
            Util.save_from_dict_to_json(plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))   

            def func():
                LogicKlive.channel_load_from_site()
            t = threading.Thread(target=func, args=())
            t.setDaemon(True)
            t.start()
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    
    @staticmethod
    def plugin_unload():
        try:
            pass
        except Exception as e: 
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    

    @staticmethod
    def migration():
        try:
            pass
            #db_version = ModelSetting.get('db_version')
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    
