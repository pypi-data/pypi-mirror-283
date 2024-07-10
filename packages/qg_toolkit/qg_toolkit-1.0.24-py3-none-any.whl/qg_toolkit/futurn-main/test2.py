import requests


def main():
    solveUrl = "http://118.193.37.214:9092/v1/solve"

    sitekey = "0x4AAAAAAAaHm6FnzyhhmePw"
    url = "https://pioneer.particle.network/"
    query_data = {"sitekey": sitekey, "url": url}
    response = requests.get(solveUrl, json=query_data)
    res = response.text
    print(res)


if __name__ == '__main__':
    main()


