import argparse
import jzai
import site

def argcli():
    parser = argparse.ArgumentParser(description="jzai api cli")
    parser.add_argument("--botname", type=str, help="The Bot's Name")
    parser.add_argument("--fileorweb", type=str, help="File or website to train bot on.")
    args = parser.parse_args()

def createAPIKEY(apikey):
    try:
        sitepackages = site.getsitepackages()
        site_packages = sitepackages[1]
        jzaisitepackage = site_packages + "\jzai\\apikey.txt"
        with open(jzaisitepackage, "w+") as file:
            file.write(apikey)
            file.close()
    except SyntaxWarning:
        with open(jzaisitepackage, "w+") as file:
            file.write(apikey)
            file.close()

createAPIKEY("aoihasdkfhaksjdfhukasdhf")