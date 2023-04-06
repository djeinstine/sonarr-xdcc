import requests,bs4,logging
from typing import List, Dict
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.IrcServer import IrcServer


def find_subsplease_packs_from_nibl(search_phrase: str) -> List[XDCCPack]:
    """
    Method that conducts the xdcc pack search for subsplease.org from the Nibl.co.uk website

    :return: the search results as a list of XDCCPack objects
    """
    if not search_phrase:
        return []

    search_query = search_phrase.replace(" ", "+")
    search_query = search_query.replace("!", "%21")


    website= f"https://nibl.co.uk/search?query={search_phrase}"

    raw_html = requests.get(website)#, timeout=30)
    response = raw_html.status_code

    #bad web response
    if response.status_code >= 300:
        logging.warning("Failed to load data from nibl.co.uk. "
                        "Check your VPN or proxy")
        return []

    bs4_soup = bs4.BeautifulSoup(raw_html.text,'html5lib')

    #find anime data
    ##note, if this class changes, this will break the code!
    data= bs4_soup.findAll("td",{"class":"border-dashed border-t border-gray-200 px-3 py-2 dark:border-gray-700"}) 

    #html tag and class changed
    if data is None:
        logging.warning("Failed to successfully scrape data from nibl.co.uk. "
                        "Check the html tags and classes!")
        return []
    
    nibl_columns = ['bot_name','pack_num','size_mb','file_name','empty_space']
    num_cols = len(nibl_columns)
    num_results = len(data)


    #data must be divisible by number of columns specified
    number_of_results = len(data)/num_cols

    #number of columns has changed
    if len(data)%num_cols > 0:
        logging.warning("Failed to successfully scrape data from nibl.co.uk. "
                        "Number of item columns have changed!")
        return []

    packs = []
    result_idx = 0
    for idx in range(0,int(number_of_results),1):
        #index
        result_idx = idx*num_cols

        #bot
        botname = data[result_idx+0].a.text
        #pack #
        packnumber = data[result_idx+1].text
        #size
        filesize = data[result_idx+2].text
        #item
        filename = data[result_idx+3].text

        pack = XDCCPack(IrcServer("irc.rizon.net"), botname, packnumber)
        pack.set_filename(filename)
        pack.set_size(filesize * 1000 * 1000)
        packs.append(pack)
        #print(results)

    for result in results:

        try:
            result = parse_result(result)
            botname = result["b"]
            filename = result["f"]
            filesize = int(result["s"])
            packnumber = int(result["n"])
            pack = XDCCPack(IrcServer("irc.rizon.net"), botname, packnumber)
            pack.set_filename(filename)
            pack.set_size(filesize * 1000 * 1000)
            packs.append(pack)

        except IndexError:  # In case the line is not parseable
            pass

    return packs