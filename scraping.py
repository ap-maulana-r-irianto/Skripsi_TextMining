# import library yang dibutuhkan
import requests
from bs4 import BeautifulSoup
import csv

# url website yang akan di scraping
base_url = 'https://repository.unej.ac.id/handle/123456789/175/recent-submissions?offset='

# deklarasi list pages
pages = ['0']
page = 0
data = []

# looping untuk mengisi list pages
for p in range(1,20):
	page = page + 20
	pages.append(str(page))

# looping scraping website sebanyak list pages
for url in pages:
	# mengakses url website dengan requests
	r = requests.get(base_url+url)
	# mengakses url requests dengan beautifulsoup
	soup = BeautifulSoup(r.text, 'html.parser')
	# mencari div dengan nama class artifact-description pada url
	items = soup.findAll('div', 'artifact-description')

	# looping 
	for item in items :
		# menyimpan judul skripsi yaitu dengan mencari h4 dengan nama class artifact-title 
		title = item.find('h4', 'artifact-title').text.strip()
		# menyimpan penulis skripsi yaitu dengan mencari span dengan nama class author h4 
		author = item.find('span', 'author h4').text.strip()
		# menyimpan tahun skripsi yaitu dengan mencari span dengan nama class date 
		year = item.find('span', 'date').text.split('-')[0]	
		# menyimpan link url detail skripsi yaitu dengan mencari h4 dengan nama class artifact-title 
		link_abstract = item.find('h4', 'artifact-title').find('a')['href']
		detail_url = 'https://repository.unej.ac.id'+link_abstract
		r2 = requests.get(detail_url)
		soup2 = BeautifulSoup(r2.text, 'html.parser')
		elemen_abstract = soup2.findAll('div', 'simple-item-view-description item-page-field-wrapper table')
		for abstracts in elemen_abstract:
			abstract = abstracts.find('div').text
		full_url = detail_url+'?show=full'
		r3 = requests.get(full_url)
		soup3 = BeautifulSoup(r3.text, 'html.parser')
		table = soup3.findAll('tr', 'ds-table-row odd')
		n = 1
		for td in table:
			detail = td.find('td', 'word-break').text
			n = n + 1
			if n == 5:
				nim = detail
				try:
					print(author)
					kode = nim[8]
				except:
					kode = ''
				if kode == '1':
					minor = 'Sistem Informasi'
				elif kode == '2':
					minor = 'Teknologi Informasi'
				elif kode == '3':
					minor = 'Informatika'
				else:
					minor = 'Tidak Diketahui'
				break
		data.append([title, author, year, abstract, nim, minor])

headers = ['Judul', 'Mahasiswa', 'Tahun', 'Abstract', 'NIM', 'Jurusan']
writer = csv.writer(open('skripsi_fasilkom.csv', 'w', encoding='utf-8', newline=''))
writer.writerow(headers)
for d in data:
	writer.writerow(d)
