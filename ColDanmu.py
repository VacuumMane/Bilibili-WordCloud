import re
import requests
import jieba
import wordcloud
import imageio
import json
import random

#输入所需弹幕对应的bv号和截止时间
BV = input("输入视频的BV号：")
date = input("输入截止日期（格式XXXX-XX-XX）：")
pic = input("输入背景图片名（放置在ColDanmu文件夹下,jpg格式）:")

#准备工作
mask = imageio.imread(pic)
cookie = "DedeUserID__ckMd5=f9bb2cc3d66e5c25; _uuid=4B750FEF-30B5-7D47-BE50-8CEE290BA8F220365infoc; sid=4giy46eu; buvid3=79790E02-BB09-491B-B734-09045FE1C2B4155831infoc; DedeUserID=11822281; rpdid=|(k||RmY|)Rk0J'ulmk~mu~|Y; CURRENT_FNVAL=16; bili_jct=7f7f8908ada8d657020f42d41c50f67a; PVID=2; SESSDATA=3cbe9cd1%2C1611326464%2Ce639e*71; LIVE_BUVID=AUTO9615957722435339; bfe_id=7b6a677b97d4786cd8b2f807c787d88b"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041","Cookie":cookie
}

#获取cid
cid_url = "https://api.bilibili.com/x/player/pagelist?bvid=" + BV + "&jsonp=jsonp"
response = requests.get(cid_url,headers = headers).content.decode("utf-8")
res_dict = json.loads(response)
values = res_dict["data"]
cid = str(values[0]["cid"])
#print(cid)

#爬取数据
url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid=" + cid +"&date=" + date
response = requests.get(url,headers = headers).content.decode("utf-8")
f = open("../raw_danmu.txt","w",encoding = "utf-8") #保存原始弹幕
f.write(response)
f.close()
find_danmu = r'<d p=.*?.>(.*?)</d>' #用正则获取弹幕
danmu = re.findall(find_danmu,response,re.S) #列表形式
f = open("../list_danmu.txt","w",encoding = "utf-8") #保存正则弹幕
f.write("\n".join(danmu))
f.close()

#绘制词云
danmu_word = jieba.lcut(" ".join(danmu))
danmu_str = " ".join(danmu_word)
w = wordcloud.WordCloud(font_path = "msyh.ttc",background_color = "white",width = 1000,height = 650,mask = mask)
w.generate(danmu_str)
w.to_file("../danmu.png")

if input("输入回车退出") == "\n":
    exit