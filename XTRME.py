from bs4 import BeautifulSoup
import multiprocessing
from functools import partial
import time
import requests
import urllib  
import os
# import bs4.builder._lxml

''' define global variables'''

url_list = {
    '5070':'https://papers.xtremepape.rs/CAIE/O%20Level/Chemistry%20(5070)/',
    '5040':'https://papers.xtremepape.rs/CAIE/O%20Level/Physics%20(5054)/',
    '2210':'https://papers.xtremepape.rs/CAIE/O%20Level/Computer%20Science%20(2210)/',
    '4024':'https://papers.xtremepape.rs/CAIE/O%20Level/Mathematics%20D%20(4024)/',
}
online_url = 'https://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/'

url_online = {}

def down_paper(href,folder_p):
	
	''' given url, download the pdf at that url '''

	time.sleep(0.5)  # please do not delete this
	filename = href.split('/')[-1]
	# print(href,filename,sep='-----') # test only

	# if the file already exists
	try:
		with open(folder_p+filename, 'r') as code:
			print('file already exists {}'.format(filename))
			return 1
	# otherwise creating new file
	except FileNotFoundError:
		print('detected new file.',end=' ')
		try:
			# try to open new file
			with open(folder_p+filename, 'wb') as code:
				r = requests.get(href)
				code.write(r.content)
				print('successfully downloaded {}'.format(filename))
				return 0
		# if cannot open/download
		except Exception:
			print('lost connections to the file {} or cannot i/o in the directory provided.'.format(filename))
			return -1


def get_code():

	''' get the syllabus code for every subject on xtremepaper'''

	html = requests.get(online_url)
	soup = BeautifulSoup(html.text,'html.parser')
	datas = soup.select('td.autoindex_td > a ')
	if datas != []:
		# get rid of parent dir
		datas.pop(0)
		# 
		for data in datas:
			# multi = 0
			href_code = data.get('href')
			code = str (data.get_text().split('(')[-1].strip(')'))
			if not code.isdigit():
				# multi = 1
				url_online[code[:4]] = 'http://papers.xtremepapers.com'+ href_code
				url_online[code[-4:]] = 'http://papers.xtremepapers.com'+ href_code
			else:
				url_online[code] = 'http://papers.xtremepapers.com' + href_code 

		# print(url_online)
	else:
		print('NetWork error')
		return -1

def get_papers(url_key):
	url = url_list[url_key]
	'''download all the files at the url provided'''
	new_hrefs = []
	# obatin url
	html = requests.get(url)
	soup = BeautifulSoup(html.text,'html.parser')
	hrefs = soup.select('td.autoindex_td > a')

	if hrefs == []:
		print('wrong url provided')
		return -1
	hrefs.pop(0)
	print('Now starts to download, this may (definitely) take some time so you may want to let this program run alone.')
	
	#create folder
	folder_path = url.split('/')[-2]+'/'
	if os.path.isdir(folder_path):
			print('folder {} already exists'.format(folder_path))
			pass
	else:
		print('creating new folder {}'.format(folder_path))
		os.mkdir(folder_path)

	for href in hrefs:
		href = url_list[url_key]+href.get('href').strip('/.')
		new_hrefs.append(href)
	# print(new_hrefs)
	
	# dowload file	
	with multiprocessing.Pool() as pool:
		results = pool.map(partial(down_paper, folder_p = folder_path), new_hrefs)

	print('1 - already downloaded, -1 - cannot download, 0 - successfully download.')

	print(results)

	print('successfully downloaded all the files available at {}'.format(url))
	return 0
