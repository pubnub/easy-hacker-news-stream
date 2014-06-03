# The Easiest Way to Create a Hacker News Feed using Python and JavaScript


We’ve all been sitting in the back of a CS lecture or class and looked up from our laptop to actually listen and taken a quick peek around at everyone’s laptops. More likely than not, quite a few of those screens were displaying the all too familiar Hacker News orange. While maybe we should all pay more attention to the speaker, it seems new, cool news always takes precedence. So what if you were determined to never miss a single article? Or what if you wanted to get every update from the site and automate based off that new information? By leveraging the power of PubNub’s real time global network, and scraping a little RSS, everyone will never miss a new Hacker News article again. If you want to see it working live, there is a quick and dirty [demo you can see here.][2] It uses the JavaScript Pubnub SDK and will display the updates to the Hacker News feed. Just clone the [source from Github][3] and run the Python scraper locally.

## RSS Scraping

The first task is to grab the RSS feed from Hacker News. There is a plethora of ways to do this and you can quickly write your own rss scraper if you want, but I decided to use Python and feedparser. With a quick “pip install feedparser” we have our RSS. 


    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    // Get Hacker News Rss
    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def current_hn(rss):
	    return feedparser.parse(rss)


There is lots of information you will get in this feed and if you want, take it all. However, I decided the most interesting information was the rank of the post, title of the post, the link to the article, and the comments link. 

    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    // Store interesting information
    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    message = []
    for index, entry in enumerate(rss.entries):
    	post = {}
    	post["rank"] = index + 1
    	post["title"] = entry.title
    	post["link"] = entry.link
    	post["comments"] = entry.comments
    	message.append(post)

## Go Global

Now that we have the information that is important to us, it's time to make it global. PubNub provides our incredibly simple API to publish the message. Quickly “pip install Pubnub” and publish our information from Hacker News.  

    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    // Publish to PubNub
    // -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    pubnub.publish({
		"channel": "hacker-news",
		"message": message
		})


Now it’s up to you. [PubNub offers over 50 different SKD’s for your use. Take your pick.][1] When trying to consume the information simply subscribe to the channel (in our case “hacker-news”) and you’re off. There are publically available demo publish and subscribe keys to use. The Python module even gives you options for specifying how often you want to poll Hacker News for changes, and if you want to get a new page after every change to the site or just the new posts that appear on the site. 



![My Hacker News][4]


## Additional Resources

If you want to dive further into PubNub, we have lots of [tutorials and walkthroughs.][5] Happy Hacking. 


  [1]: http://www.pubnub.com/developers/
  [2]: http://pubnub.github.io/easy-hacker-news-stream/
  [3]: https://github.com/pubnub/easy-hacker-news-stream/
  [4]: http://i.imgur.com/8rvUgcb.png
  [5]: http://www.pubnub.com/demos/
