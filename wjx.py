import requests
import time
from urllib.parse import urlencode


class WenJuanXing(object):
    def __init__(self, q_num, q_data):
        self.base_url = 'https://www.wjx.cn/jq/%s.aspx'
        self.base_submit = 'http://www.sojump.com/handler/processjq.ashx?'
        self.base_spam = 'https://www.wjx.cn/AntiSpamImageGen.aspx?'
        self.sess = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.curID = q_num
        self.submitdata = q_data
        self.submittype = '1'
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.html = ''
        self.validate_text = ''
        self.rn = 0

    def getHtml(self):
        response = self.sess.get(self.base_url % self.curID)
        self.html = response.text

    def getRandNum(self):
        self.rn = 0
        self.getHtml()
        rnd_part = self.html[self.html.find('rndnum=') + 8:]
        self.rn = rnd_part[:rnd_part.find('"')]

    def stringParams(self):
        return {
            'submittype': self.submittype,
            'curID': self.curID,
            't': self.t,
            'starttime':self.starttime,
            'rn': self.rn,
            'validate_text': self.validate_text
        }

    def antiSpam(self):
        url = self.base_spam + urlencode({'t': self.t, 'q': self.curID})
        response = self.sess.get(url)
        with open('tmp_img.gif', 'wb') as f:
            f.write(response.content)
        # TODO: recognize characters in image
        self.validate_text = 'something'

    def submitForm(self):
        self.getRandNum()
        self.t = str(int(time.time() * 1000))
        self.starttime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        url = self.base_submit + urlencode(self.stringParams())
        self.sess.post(url, data={'submitdata': self.submitdata})

    def clearCookie(self):
        self.sess.cookies.clear()


def main():
    q_num = input('问卷号：')
    q_data = input('submitdata（自行理解）：')
    wjx = WenJuanXing('', '')
    # for i in range(100):
    #     wjx.submitForm()
    #     wjx.clearCookie()


if __name__ == '__main__':
    main()
