import requests
from bs4 import BeautifulSoup
from win32com.client import Dispatch
import time


"""
用于下载某一年的SST nc文件
"""


def cbk(a, b, c):
    """
    :param a: 已经下载的数据块
    :param b: 数据块的大小
    :param c: 远程文件的大小
    :return:
    """
    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(a*b*50 / c), float(a*b / c * 100)), end=' ')


if __name__ == '__main__':
    root_path = 'http://data.remss.com'
    http_path = 'http://data.remss.com/SST/daily/mw_ir/v05.0/netcdf/2018/'
    html = requests.get(http_path)
    html_text = html.text
    soup = BeautifulSoup(html_text, 'html.parser')
    items = soup.find_all('a')
    thunder = Dispatch('ThunderAgent.Agent64.1')
    for i in range(1, len(items)):
        temp = items[i]
        href_path = temp.attrs['href']
        name = temp.contents[0][:8]  # 保存的文件名
        file_path = root_path + href_path
        thunder.AddTask(file_path, f'{name}.nc')
        if (i + 1) % 5 == 0:
            thunder.CommitTasks()
            time.sleep(10)
        # file = requests.get(url=file_path, stream=True)
        # file.raise_for_status()
        # with open(f'SST/{name}.nc', 'wb') as f:
        #     total_length = int(file.headers.get('content-length'))
        #     count = 0
        #     for data in file.iter_content(100000):
        #         if data:
        #             f.write(data)
        #             count = count + len(data)
        #             print('\r' + '[下载进度]:%s%.2f%%' % ('>' * int(count*50 / total_length),
        #                                               float(count / total_length * 100)), end=' ')
        print(f'{name}.nc save successful')

    print('finish')
