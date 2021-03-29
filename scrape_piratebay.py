from bs4 import BeautifulSoup
import requests
import argparse
import json

mylist = {}


def get_torrent_link(base_url):
    try:
        pinfo = requests.get(base_url).content
        soup = BeautifulSoup(pinfo, 'html.parser')
        trs = soup.find_all("tr")
    except Exception as e:
        print(e)
        exit()

    c = -1
    for tds in trs:
        c += 1
        if c==0:
            continue
        if c==31:
            break
        target = tds.find_all("td")
        namediv = target[1].find("div", class_="detName").find_all("a")[0]
        text = namediv.text
        link = namediv.get("href")
        rhref = target[1].find_all("a")[1].get("href")

        mlink = rhref
        mylist[c] = {}
        mylist[c]["Name"] = text
        mylist[c]["Torrent_Link"] = link
        mylist[c]["Magnet_Link"] = mlink
        


def main():

    parser = argparse.ArgumentParser(description='Scrapes piratebay and provides 1st 30 torrent links along with their magnet links')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--normal", type=str, help="Normal Search query", metavar='')
    group.add_argument("-r", "--recent", action="store_true", help="Recent Search")
    group.add_argument("-t", "--top", type=str, help="Top 100 Search (category as a query)", choices=['audio', 'video', 'applications', 'games', 'other'])
    args = parser.parse_args()
    
    if args.normal:
        query1 = f'search/{args.normal}/1/'
    elif args.recent:
        query1 = 'recent'
    elif args.top:
        catg_choice = {
            "audio":100,
            "video":200,
            "applications":300,
            "games":400,
            "other":600,
        }
        query1 = f'top/{catg_choice[args.top]}'
    else:
        parser.print_help()
        exit()

    base_url = f'https://thepiratebay10.org/{query1}'
    # print(base_url)
    print("Please wait till the data has been scraped...")
    get_torrent_link(base_url)

    with open('piratebay_links.json', 'w') as outfile:
        # outfile.write(f"BASE URL: {base_url}\n\n")
        json.dump(mylist, outfile, indent=4)
    
    # print(json.dumps(mylist, indent=4))
    print(f"Operation completed considering base url as '{base_url}'")


if __name__ == "__main__":
    main()