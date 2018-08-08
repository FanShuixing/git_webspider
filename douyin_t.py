#douyin_t.py
import json,os
import requests
def response(flow):
	url='https://api.amemv.com/aweme/v1/aweme/post/'
	#筛选出以上面url为开头的url
	if flow.request.url.startswith(url):
		text=flow.response.text
		#将已经编码的json字符串解码为python对象
		data=json.loads(text)
		# print(data)
		#在fiddler中刚刚看到每一个视频的所有信息
		# 都在aweme_list中
		video_url=data['aweme_list']
		path='E:/爬虫数据/douyin'
		if not os.path.exists(path):
			os.mkdir(path)
			
		for each in video_url:
			#视频描述
			desc=each['desc']
			url=each['video']['play_addr']['url_list'][0]
			# print(desc,url)
			filename=path+'/'+desc+'.mp4'
			# print(filename)
			req=requests.get(url=url,verify=False)
			with open(filename,'ab') as f:
				f.write(req.content)
				f.flush()
				print(filename,'下载完毕')