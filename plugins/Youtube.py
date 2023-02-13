import requests, json, time, sys, os, random
from os.path import exists

api = "https://ytpp3.com"
language = {}
_select = "mp4"


def getINFO(name):
     x = requests.post(api + '/newp', data={"u": name, "c": "BG"})
     info = x.json()
     if info["status"] == 0:
          return info["message"]
     else:
          return info
     return None

def downloder(file_name, link):
    global language
    if exists('music/') == False:
        os.mkdir('music/')
    with open(r'music/{}'.format(file_name), "wb+") as f:
        print("{} {}".format(language["in_downloading"], file_name))
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:
            f.write(response.content)
            print(language["finish"])
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()
            print(language["finish"])


def init_plugin(x, lan = {}):
     global language, api, _select
     language = lan
     data = getINFO(x)
     print('0) MP4\n1) MP3')
     print(language["select"]);
     if str(input(language["sumbol"])) == "1":
          _select = "mp3"
     else:
          _select = "mp4"
     out = "Title: {title}\n"
     out += "Duration: {duration}\n"
     out += "Type: {_type}"
     out += "Filename: {fname}"
     if _select == "mp4":
          if data["data"][_select] == "":
               dl = data["data"]['{}_cdn'.format(_select)]
          else:
               dl = api + data["data"][_select]
     else:
          if data["data"][_select] == "" or data["data"][_select] == None:
               dl = data["data"]['{}_cdn'.format(_select)][0]["mp3_url"]
          else:
               dl = api + data["data"][_select]
     filename = 'file_{}.{}'.format(random.randint(0,999999999), _select);
     print(out.format(_type=_select, fname=filename, title=data["data"]["title"], duration=data["data"]["duration"]))
     downloder(filename, dl)
     
