import requests, json, time, sys

api = {
    "search": "https://myfreemp3.to/api/search?query={}",
    "download": "https://hub.ilill.li/?id={}"
    }
language = {}

seconds = 60

def getSearchData(name):
    global api
    _tmp = []
    x = requests.get(api["search"].format(name))
    for out in x.json():
        if type(out["id"]) == int:
            _tmp.append(out)
    return _tmp


def selectSearch(d):
    one = 0
    for x in d:
        print('{}. {}'.format(one, x["title"]))
        one = one + 1
    select = input(language["sumbol"])
    return d[int(select)]

def getDownload(data):
    global api, language
    x = requests.get(api["download"].format(data["id"]))
    info = x.json()
    if info["status"] == "starting":
        ot = '{}seconds'.format(seconds)
        print(language["wait"].format(ot))
        time.sleep(seconds)
        return getDownload(data)
    elif info["status"] == "finished":
        return {"filesize": info["filesize"], "filename": info["filename"], "download": info["dlFile"], "live": info["live"]};
    else:
        return info

def downloder(file_name, link):
    global language
    with open(file_name, "wb") as f:
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
    global language
    language = lan
    data = getSearchData(x)
    selected = selectSearch(data)
    download = getDownload(selected)
    out = 'FileName: {filename}\n'
    out += "FileSize: {size}\n"
    out += language["confirm"]
    print(out.format(filename=download["filename"], size=download["filesize"]))
    ask = input(language["sumbol"])
    if ask == "":
        ask = "yes"
    if ask == "yes":
        downloder(download["filename"], download["download"])
    else:
        print(language["cancel"])
        quit()

