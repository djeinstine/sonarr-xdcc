
from xdcc_dl.xdcc import download_packs
from xdcc_dl.pack_search import SearchEngines
from xdcc_dl.entities import XDCCPack, IrcServer

# Generate packs
#/msg CR-HOLLAND|NEW xdcc send #15
#manual = XDCCPack(IrcServer("irc.rizon.net"), "CR-HOLLAND|NEW", 1)
from_message = XDCCPack.from_xdcc_message("/msg CR-HOLLAND|NEW xdcc list")
search_results = SearchEngines.NIBL.value.search("Boruto")
#combined = [manual] + from_message + search_results

# Start download
#download_packs(from_message)