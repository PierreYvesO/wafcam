config = {
    'user': '',
    'password': '',
    'host': '2z2tz.myd.infomaniak.com',
    'database': '2z2tz_patcam_prod',
    'raise_on_warnings': True
}

user_config = {
    'user': 'waf',
    'password': 'cam',
    'host': '127.0.0.1',
    'database': 'wafcam',
    'raise_on_warnings': True
}


def read_env():
    db_dict = {}
    f = open("../../.env.local", "r")
    for x in f:
        tmp = x.split(":")
        db_dict[tmp[0].strip()] = tmp[1].strip()
    f.close()
    db_dict['raise_on_warnings'] = True
    return db_dict


if __name__ == '__main__':
    read_env()
