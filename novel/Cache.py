#Cache.py
import urllib.request
import re,os
import pickle,requests
from urllib.parse import quote

os.chdir("E:/爬虫数据")
#这个模块可以当作模板来使用，不怎么用修改		
		
class Downloader:
	def	__init__(self,cache):
		self.cache=cache
		
	def __call__(self,url):
		result=None
		if self.cache:
			try:
				result=self.cache[url]
				# print("已调入数据")
				
			except:
				pass
		if result==None:
			result=self.download(url)
			if self.cache:
				# print(type(url))
				self.cache[url]=result
		return result
		
	def download(self,url,num_retry=2):
		# print('下载中：',url)
		headers={'User-agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'}
		req=requests.get(url=url,headers=headers)
		req.encoding='gbk'
		html=req.text
		return(html)
				
		
	
class DiskCache:
	def __init__(self,cache_dir='Cache'):
		self.cache_dir=cache_dir
	def __getitem__(self,url):
		path=self.url_to_path(url)
		if os.path.exists(path):
			with open(path,'rb') as fp:
				return pickle.load(fp)
		
	def __setitem__(self,url,result):
		path=self.url_to_path(url)
		folder=os.path.dirname(path)
		if  not os.path.exists(folder):
			os.makedirs(folder)
		with open(path,'wb') as fp:
			fp.write(pickle.dumps(result))
			
	def url_to_path(self,url):
		components=urllib.parse.urlsplit(url)
		path=components.path
		if not path:   #即path为空
			path='nihao'
		elif path.endswith('/'):
			path+='index.html'
		filename=components.netloc+path+components.query
		filename=re.sub('[^/0-9a-zA-Z\-.,;_]','_',filename)
		filename='/'.join(segment[:255] for segment in filename.split('/'))
		return(os.path.join(self.cache_dir,filename))
		

			
			
if __name__=='__main__':
	a=Downloader(DiskCache())
	a.download('https://book.douban.com/subject/1059336/')
