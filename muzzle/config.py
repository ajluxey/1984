import os

basedir = os.path.abspath(os.path.dirname(__file__))

all_links = {'Образы': {'Образы': '/images',
                        'Управление': '/images/management',
                        'Раздача': '/images/distribute'},
             'Пользователи': {'Пользователи': '/users',
                              'Вход': '/users/login',
                              'Регистрация': '/users/registration',
                              'Группы': '/users'},
             'Выход': {'Выход': '/users/logout'}
             }

macs = ['f4:6d:04:e7:81:a9',
        'f4:6d:04:e5:1c:65',
        '20:cf:30:b0:b5:cc',
        'f4:6d:04:e7:81:8f',
        'f4:6d:04:e8:8c:2b',
        'f4:6d:04:e5:1b:03',
        '20:cf:30:b0:b5:bb',
        'f4:6d:04:e5:1c:59',
        'f4:6d:04:e5:1b:7c',
        'f4:6d:04:e7:81:9c',
        'f4:6d:04:e7:80:c5',
        '20:cf:30:b0:b5:cb',
        'f4:6d:04:e7:81:87']

groups = ['Nothing',
          'ККСО-01-17',
          'ККСО-02-17',
          'ККСО-03-17',
          'ККСО-04-17',
          'ККСО-05-17',
          'ККСО-06-17']

map = [
    [macs[0], 0, 0, 0],
    [macs[1], 0, 0, macs[2]],
    [0, 0, 0, macs[3]],
    [0, macs[4], macs[5], 0],
    [0, 0, 0, macs[6]],
    [0, 0, macs[7], macs[8]],
    [macs[9], macs[10], macs[11], macs[12]]
]

base_image_conf = '''SERVER_ADDR="10.0.3.2"
SERVER_PORT=8000
IMAGE_FILE="{imagename}"
CYPOL_TARGET_LINK="$SERVER_ADDR:$SERVER_PORT/$IMAGE_FILE"

wget $CYPOL_TARGET_LINK -O - | dd of=/dev/sda
sleep 2 && /bin/sh /cypol/scripts/reboot.sh'''


flask_config = {'DEBUG': True,
                'IMAGES': 'E:/allImages',
                'IMAGE_FOLDER': 'E:/TestImages/',
                'MASTER_CONFIG': 'E:/master_config/masterconfig.json',
                'ALL_LINKS': all_links,
                'SECRET_KEY': 'b89d67e8e8a5e23c91407c8f2cb808e8da423e14db0c70d8abd4ac2eb6eb11ff',
                'MACS': macs,
                'GROUPS': groups,
                'BASE_CONFIG': base_image_conf,
                'MAP': map,
                'HOST': '127.0.0.1',
                'PORT': '5000'}
