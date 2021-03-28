from bs4 import BeautifulSoup
import requests
import json
import time

mylist = {}


def get_torrent_link(base_url):
    try:
        pinfo = requests.get(base_url).content
        soup = BeautifulSoup(pinfo, 'html.parser')
        tds = soup.find_all("td", class_="coll-1 name")
    except Exception as e:
        print(e)
        exit()

    c = 1
    for td in tds:
        target = td.find_all('a')[1]
        link = 'https://www.1377x.to'+target.get("href")
        text = target.text
        mylist[c] = {}
        mylist[c]["Name"] = text
        mylist[c]["Torrent_Link"] = link
        get_magnet_link(c,link)
        time.sleep(0.4)
        c += 1


def get_magnet_link(sn,turl):
    try:
        pinfo2 = requests.get(turl).content
        soup2 = BeautifulSoup(pinfo2, 'html.parser')
        magnet_link = soup2.find("a", class_="l3426749b3b895e9356348e295596e5f2634c98d8 la1038a02a9e0ee51f6e4be8730ec3edea40279a2 l0d669aa8b23687a65b2981747a14a1be1174ba2c")
        link = magnet_link.get("href")
        mylist[sn]["Magnet_Link"] = link
    except Exception as e:
        print(e)


def main():
    print("\n------------------ MENU ------------------\n")
    print("1. Normal Search")
    print("2. All Trending")
    print("3. Trending in a catagory")
    print("4. Top 100 in a catagory\n")
    print("Categories: movies,television,games,applications,music,documentaries,anime,other")
    print("\n------------------------------------------\n")

    choice = int(input("Enter choice: "))
    
    if choice == 1:
        search_item = input("Enter search item: ")
        query1 = f'search/{search_item}/1/'
    elif choice == 2:
        query1 = 'trending'
    elif choice == 3:
        search_category = input("Enter category: ")
        query1 = f'trending/d/{search_category}'
    elif choice == 4:
        search_category = input("Enter category: ")
        query1 = f'top-100-{search_category}'
    else:
        print("Wrong choice")
        exit()

    base_url = f'https://www.1377x.to/{query1}'
    print("Please wait till the data has been scraped...")
    get_torrent_link(base_url)

    with open('1337x_links.txt', 'w') as outfile:
        outfile.write(f"BASE URL: {base_url}\n\n")
        json.dump(mylist, outfile, indent=4)
    
    # print(json.dumps(mylist, indent=4))
    print("Operation completed")


if __name__ == "__main__":
    main()