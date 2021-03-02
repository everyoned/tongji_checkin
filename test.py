import requests
import json
import datetime
import argparse
import sys


class Checkin:
    def __init__(self, token, locLat, locLng):
        print("🚌 打卡任务启动")
        self.name = 0
        self.location = (locLat, locLng)
        self.debug = not True
        self.base_url = 'https://tjxsfw.chisai.tech/api/school_tjxsfw_student'
        self.info = 0
        self.headers = {
            'Host': 'tjxsfw.chisai.tech',
            'Connection': 'keep-alive',
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx427cf6b5481c866a/54/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        print('✔已新建打卡实例')

    def get_info(self):
        self.info_url = f'{self.base_url}/tblStudentUsers/my'
        print("⏩正在获取个人信息...")
        response = requests.get(self.info_url, headers=self.headers, verify=self.debug)
        try:
            self.info = json.loads(response.text)['data']
            self.name = self.info["studentName"]
            print(f'✔{self.name}同学，你好~')
            return self.info
        except:
            print("❌ 获取个人信息出错，退出！")
            sys.exit()

    def has_done(self):
        print("⏩ 正在检查今日打卡状态...")
        self.has_done_url = f'{self.base_url}/yqfkLogDailyreport/hasDoneToday?studentPid={self.info["studentPid"]}'
        response = requests.get(self.has_done_url, headers=self.headers, verify=self.debug)
        try:
            data = json.loads(response.text)['data']
            # 因为不确定没打卡是不是false，但是打卡之后肯定是true，就先写着
            if data:
                return True
            else:
                return False
        except:
            print("❌ 检查状态出错，退出！")
            sys.exit()

    def checkin(self):
        self.checkin_url = f'{self.base_url}/yqfkLogDailyreport/v3'
        # 注意reportDatetime需要根据实际需求修改，git-action时间是UTC时间，所以打卡需要+8小时
        # 其他环境中根据实际情况调整，实际测试中显示，即使提交空数据也可以自动打卡
        data = {
          'studentPid': self.info['studentPid'],
          'studentName': self.info['studentName'],
          'studentStudentno': self.info['studentStudentno'],
          'studentCollege': self.info['studentCollegeName'],
          'locLat': self.location[0],
          'locLng': self.location[1],
          'locNation': self.info['statusLastreportLocNation'],
          'locProvince': self.info['statusLastreportLocProvince'],
          'locCity': self.info['statusLastreportLocCity'],
          'locDistrict': self.info['statusLastreportLocDistrict'],
          'healthy': '0',
          'source': 'weixin,windows',
          'reportDatetime': (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
          'hasMoved': 'false',
          'leaveReason': '',
          'locNation1': self.info['statusLastreportLocNation'],
          'locProvince1': self.info['statusLastreportLocProvince'],
          'locCity1': self.info['statusLastreportLocCity'],
          'locRiskaddress': '不在范围内',
          'locRisklevelGoverment': '低风险',
          'studentStatusQuarantine': '正常（未隔离）',
          'locStreet': 'null',
          'locStreetno': 'null'
          }
        print('⏩ 正在为您完成打卡')
        try:
            response = requests.post(self.checkin_url, headers=self.headers, data=data, verify=self.debug)
            return json.loads(response.text)
        except:
            print("❌ 打卡失败")
            sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--token', type=str, default=None)
    parser.add_argument('--locLat', type=str, default=None)
    parser.add_argument('--locLng', type=str, default=None)
    args = parser.parse_args()
    print(f'[{(datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}]')
    print("用户信息：", args)
    # 初始化打卡类
    ck = Checkin(args.token, args.locLat, args.locLng)
    # 获取基本信息以及上次数据
    ck.get_info()
    # 检查是否今日已打卡
    if ck.has_done():
        print("✔ 今日已打卡，无须重复打卡")
    else:
        log = ck.checkin()
        print('✔ 打卡完成')
        print(f'log: {log}')
