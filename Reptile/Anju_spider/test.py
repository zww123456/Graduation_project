from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

options = webdriver.ChromeOptions()

options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')

# 禁用谷歌浏览器图片、JavaScript,提升爬取速度

prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript': 2  # 2即为禁用的意思
    }
}
options.add_experimental_option('prefs', prefs)

quyu = ['qingxiu','xixiangtang','jiangnan','xingning','liangqing',
        'yongning','wumingquwumingxian','hengxianz','shanglinxian',
        'longanxianz','binyangxian','mashanxianz']
driver = webdriver.Chrome(chrome_options=options)
# 爬取每一个标题的链接，进入以后获取相应的内容后再返回上一级，重复以上动作
for page in range(1,51):
        for i in range(len(quyu)):
            try:
                driver.get('https://nanning.anjuke.com/sale/'+quyu[i]+'/p' + str(
                    page) + '/?kwid=10507608784&utm_term=%E5%8D%97%E5%AE%81%E6%88%BF%E4%BA%A7#filtersort')  #
                for num in range(1, 61):
                    search = driver.find_element_by_xpath('//*[@id="houselist-mod-new"]/li[' + str(
                        num) + ']/div[2]/div[1]/a')

                    driver.get(search.get_attribute('href'))  # 获取子页面链接

                    # 获取房源详情页面
                    html=driver.page_source

                    # 北纬
                    lat = re.compile('lat : "(.*?)"',re.S)
                    north = lat.findall(html)[0]
                    # 东经
                    lng = re.compile('lng : "(.*?)"',re.S)
                    east = lng.findall(html)[0]

                    #所属区

                    place = driver.find_elements(By.XPATH,
                                                 '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[4]/div[2]/p/a[1]')
                    of_place = ''
                    for i in place:
                        of_place += i.text
                    # 小区名，户型，单价，面积，年份，房屋朝向，楼层，装修程度，有无电梯，坐标
                    village = driver.find_elements(By.XPATH,
                                                   '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[1]/div[2]/a')

                    layout = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[2]/div[2]')
                    price = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[3]/div[2]')


                    area = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[5]/div[2]')

                    year = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[7]/div[2]')

                    orientation = driver.find_element(By.XPATH,
                                                      '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[8]/div[2]')

                    floor = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[11]/div[2]')

                    trim = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[12]/div[2]')

                    elevator = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[14]/div[2]')


                    village_str = ''
                    for i in village:
                        village_str += i.text
                    info = village_str + ',' + of_place + ',' + layout.text + ',' + price.text + ',' \
                           + area.text + ',' + year.text + ',' \
                           + orientation.text + ',' + floor.text + ',' + trim.text + ',' \
                           + elevator.text + ',' + north + ',' + east + '\n'
                    with open('House_Info.csv', 'a', encoding='utf-8') as f:
                        f.write(info)
                    time.sleep(5)
                    driver.back()  # 后退，返回上一级目录页
            except Exception:
                quyu.remove(quyu[i])
                continue
driver.quit()
