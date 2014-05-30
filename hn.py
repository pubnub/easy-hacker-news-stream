import feedparser
from Pubnub import Pubnub
import time
from argparse import ArgumentParser
import sys


def current_hn(rss):
	return feedparser.parse(rss)

def create_message(rss):
	message = []
	for index, entry in enumerate(rss.entries):
		post = {}
		post["rank"] = index + 1
		post["title"] = entry.title
		post["link"] = entry.link
		post["comments"] = entry.comments
		message.append(post)
	return message

def publish(pubnub, message):
	pubnub.publish({
		"channel": "hacker-news",
		"message": message
		})

def check_for_change(mode, hn, rss):
	new_hn = current_hn(rss)
	if mode == "entire":
		if str(new_hn) != str(hn):
			return create_message(new_hn)
	elif mode == "new":
		new_hn = create_message(new_hn)
		hn = create_message(hn)
		hn_titles = []
		[hn_titles.append(topic["title"]) for topic in hn]
		message = []
		for new_title in new_hn:
				if new_title["title"] not in hn_titles:
					message.append(new_title)
		return message 
	else:
		return None


if __name__ == "__main__":
	parser = ArgumentParser(description="Options to parse RSS Feed")
	parser.add_argument("-r", "--rsslink", dest="rss_link", type=str, default="https://news.ycombinator.com/rss", help="This is a link to the rss feed desired to scrape.")
	parser.add_argument("-t", "--time", dest="time_to_wait", type=int, default=10, help="In seconds how long do you want to wait between checking the rss feed.")
	parser.add_argument("-m", "--mode", dest="mode", type=str, default="entire", help="Set the mode in which to poll for feeds. Either 'entire' which will publish an entire new feed every update. Or 'new' which will only pulish new changes.")

	argv = sys.argv[1:]
	try:
		argp = parser.parse_args(argv)
	except SystemExit as ex:
		print("Eception when parsing args because of => " + str(ex))
		sys.exit()

	try:
		rss_link = argp.rss_link
		time_to_wait = argp.time_to_wait
		mode = argp.mode
	except Exception as ex:
		print("Something went wrong because of => " + str(ex))


	sub_key = "sub-c-dc6bc448-89af-11e3-baad-02ee2ddab7fe"
	pub_key = "pub-c-cc479bc5-bfa2-412c-826f-f8e05f702a03"
	pubnub = Pubnub(pub_key, sub_key)

	fp = current_hn(rss_link)

	while True:
		message = check_for_change(mode, fp, rss_link)
		if message is not None:
			publish(pubnub, message)
			fp = current_hn(rss_link)
		time.sleep(time_to_wait)
