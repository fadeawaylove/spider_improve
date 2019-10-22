from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_free_proxies():
    """获取免费的代理"""
    url = "http://www.goubanjia.com/"
    driver = webdriver.Remote(command_executor="http://192.168.219.3:4444/wd/hub",
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    trs = soup.find_all("tr")
    ip_list = {"http": [], "https": []}
    for tr in trs[1:]:
        td_list = tr.find_all("td")
        td1 = td_list[0]
        td3 = td_list[2]
        ip_type = td3.string
        for t in td1:
            if t.name:
                style = t.attrs.get("style")
                if style and "none" in style:
                    t.decompose()
        ip = "".join([x.string for x in td1 if x.string is not None])
        ip_list[ip_type].append(ip)
    return ip_list


if __name__ == '__main__':
    get_free_proxies()
