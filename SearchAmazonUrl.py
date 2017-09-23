#適当なページからamazonのページを発見するまでクローリングするプログラム。

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import difflib

def ShowScore(ScoreCheck, GoodUrl, TargetUrl):
	print(ScoreCheck)
	print(GoodUrl)
	print(TargetUrl)
	SuitUrl = GoodUrl
	page = ReadPage(SuitUrl)
	ahreflist = ReadHref(page)
	get_content(ahreflist, TargetUrl)


# a hrefの中身を取り出し、類似度の高いURLを出力する。
def get_content(ahreflist, TargetUrl):
	ScoreCheck = 0
	GoodUrl = ""
	for ahref in ahreflist:
		start_link = ahref.find('<a href=')
		if start_link == -1:
			continue
		start_quote = ahref.find('"',start_link)
		end_quote = ahref.find('"',int(start_quote) + 1)
		content = ahref[start_quote + 1:end_quote]
		if content != None or content[0] != '/' or content[0] != '#' or content[0] != '?':
			AlanogyScore = difflib.SequenceMatcher(None, TargetUrl, content).ratio()
		if ScoreCheck < AlanogyScore:
			ScoreCheck = AlanogyScore;
			GoodUrl = content
	ShowScore(ScoreCheck, GoodUrl, TargetUrl)


# 大まかにa href属性を集める。
# page : urlのページの内容(文字列)
# count : 文字列の長さ分のcount
# start : リンク先の先頭index
# end : リンク先の最後index
# alist : リンクの配列
def ReadHref(page):
	count = 0
	start = 0
	end = 0
	AhrefList = []

	while len(page) != count:
		if count == 0:
			count += 1
			continue
		if page[count-1] == '<' and page[count] == 'a':
			start = count-1
			while page[count] != '>':
				count += 1
			end = count
			AhrefList.append(page[start:end] + '>')
		count += 1
	return AhrefList


# ページの読み込みを行う。
def ReadPage(url):
	response = urllib.request.urlopen(url)
	html = response.read()
	page = BeautifulSoup(html, "html.parser")
	page = str(page)
	return page


if __name__ == '__main__':
	SuitUrl = "http://blog.mudatobunka.org/entry/2016/05/08/154934"
	TargetUrl = "https://www.amazon.co.jp/"
	page = ReadPage(SuitUrl)
	ahreflist = ReadHref(page)
	get_content(ahreflist, TargetUrl)	

