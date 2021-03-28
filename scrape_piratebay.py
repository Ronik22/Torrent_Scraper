from bs4 import BeautifulSoup
import requests
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
    print("\n------------------ MENU ------------------\n")
    print("1. Normal Search")
    print("2. Recent Torrents")
    print("3. Top 100 in a category\n")
    print("Categories: audio,video,applications,games,other")
    print("\n------------------------------------------\n")

    choice = int(input("Enter choice: "))
    
    if choice == 1:
        search_item = input("Enter search item: ")
        query1 = f'search/{search_item}/1/'
    elif choice == 2:
        query1 = 'recent'
    elif choice == 3:
        search_category = input("Enter category: ")
        marks = {
            "audio":100,
            "video":200,
            "applications":300,
            "games":400,
            "other":600,
        }
        query1 = f'top/{marks[search_category]}'
    else:
        print("Wrong choice")
        exit()

    base_url = f'https://thepiratebay10.org/{query1}'
    # print(base_url)
    print("Please wait till the data has been scraped...")
    get_torrent_link(base_url)

    with open('piratebay_links.txt', 'w') as outfile:
        outfile.write(f"BASE URL: {base_url}\n\n")
        json.dump(mylist, outfile, indent=4)
    
    # print(json.dumps(mylist, indent=4))
    print("Operation completed")


if __name__ == "__main__":
    main()