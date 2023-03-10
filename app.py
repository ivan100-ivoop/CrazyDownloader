import json, os, importlib
from update_check import checkForUpdates
from os.path import exists, isfile

settings = {
    "lang": "en",
    "authon": "vanko(ivoop)",
    "check": True
    }

language = {
    "wellcome": "Wellcome to CrazyDownloader Version {version}!",
    "ask_url": "Give me Name of Song/video?",
    "sumbol": "> ",
    "type": "Select Suppoty Type:",
    "wait": "Wait {} Creating Download Link!",
    "confirm": "Confirm Download yes/no (default: yes)?",
    "cancel": "Download is a Cancel!",
    "in_downloading": "Downloading",
    "select": "Select:",
    "finish": "Downloading Finish!",
    "check_updates": "Checking For updates!",
    "error":
    {
        "missing_type": "Error This Type Not Support Try Again {times}!",
        "to_many_type": "Error To Many Try Program is auto closing!"
    }
}
plugins = {}

files = {
    "setting": 'settings.json',
    "plugins": "plugins",
    "langs": "lang",
    "func": "init_plugin",
    "version": "0.1"
    }

updateURL = 'https://raw.githubusercontent.com/ivan100-ivoop/CrazyDownloader/main/{}'
maxErrorType = 3

def loadSettings():
    global settings
    if exists(files["setting"]):
        with open(files["setting"], "r") as f:
            settings = json.loads(f.read());
    else:
        json_object = json.dumps(settings, indent=4)
        with open(files["setting"], "w") as outfile:
            outfile.write(json_object)

def loadLang():
    global settings, language, files
    lanFile = '{}/{}.json'.format(files["langs"], settings["lang"])
    if exists(lanFile):
        with open(lanFile, "r") as f:
            language = json.loads(f.read());
    else:
        os.mkdir('{}/'.format(files["langs"]))
        json_object = json.dumps(language, indent=4)
        with open(lanFile, "w") as outfile:
            outfile.write(json_object)

def loadPlugins():
    global plugins, files
    plugin = os.listdir(files["plugins"])
    if len(plugin) != 0:
        for x in plugin:
            file = '{folder}/{filename}'.format(folder=files["plugins"], filename=x)
            if isfile(file):
                updater(file)
                plugins[x.split(".")[0].lower()] = file.split(".")[0]

def startFunction(word, plg):
    global plugins, files
    exec('from {0} import *'.format(plugins[plg].replace('/', '.')))
    exec('{0}("{1}", {2})'.format(files["func"], word, language))

def stepOne():
    global files
    print(language["wellcome"].format(version=files["version"]))
    print(language["ask_url"])
    url = input(language["sumbol"])
    print(language["type"])
    stepTwo(url)

def stepTwo(url):
    global maxErrorType
    _tmp = [];
    one = 0
    for x in plugins:
        _tmp.append(x)
        print('{}) {}'.format(one, x))
        one = one + 1;
    plg = input(language["sumbol"])
    if plg == "":
        quit()
    #plg = plg.lower()
    plgs = _tmp[int(plg)]
    if plgs in plugins:
        startFunction(url, plgs)
    else:
        if maxErrorType == 1:
            print(language["error"]["to_many_type"])
            quit()
        else:
            maxErrorType = maxErrorType - 1;
        print(language["error"]["missing_type"].format(times=maxErrorType))
        stepTwo(url)

def init():
    loadSettings()
    updater('app.py')
    loadLang()
    loadPlugins()
    stepOne()

def updater(file):
    global settings, updateURL
    print(language["check_updates"])
    if settings["check"]:
        
        checkForUpdates(__file__, updateURL.format(file))
        
if __name__ == "__main__":
    init()
    
