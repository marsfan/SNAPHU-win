from os import pardir
import requests
import re



downloadRegex = re.compile(r"Download the full source distribution here: *\n<A NAME=\"SNAPHU\" HREF=\"(snaphu-v[\d\.]+tar\.gz)\">snaphu-v[\d\.]+tar\.gz</A>")

url = "https://web.stanford.edu/group/radar/softwareandlinks/sw/snaphu/"
homePage = requests.get(url).text

fileToDownload = downloadRegex.search(homePage).group(1)

downloadLink = url + fileToDownload





with open("snaphu.tar.gz", "wb") as fileObj:
    fileObj.write(requests.get(downloadLink).content)
