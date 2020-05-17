
# Sample projects , Tweeter streaming API processing

## Info
Playing around with twitter sample streaming API.
Python threads to pull and enqueue messages.
Use python circular array indices to store some trends.



## Tweater Sample API Response
Full Response seee Twitter documentation
 - https://developer.twitter.com/en/docs/tweets/sample-realtime/api-reference/get-statuses-sample

Interesting values
```
{
  "created_at": "Mon May 06 20:01:29 +0000 2019",
  "id": 1125490788736032800,
  "id_str": "1125490788736032770",
  "text": "Today's new update means that you can finally add Pizza Cat to your Retweet with comments! Learn more about this ne… https://t.co/Rbc9TF2s5X",
  "display_text_range": [
    0,
    140
  ],
  extended_tweet": {
        "full_text": "It's easy to express yourself by Retweeting with a comment. What if you could take it a step further and include media? Starting today, you can! Retweet with photos, a GIF, or a video to really make your reaction pop. Available on iOS, Android, and https://t.co/AzMLIfU3jB. https://t.co/Oir5Hpkb2F",
        "display_text_range": [
          0,
          273
        ],
        "entities": {
          "hashtags": [],
          "urls": [
            {
              "url": "https://t.co/AzMLIfU3jB",
              "expanded_url": "https://mobile.twitter.com",
              "display_url": "mobile.twitter.com",
              "unwound": {
                "url": "https://mobile.twitter.com",
                "status": 200,
                "title": "Welcome to Twitter",
                "description": null
              },
              "indices": [
                249,
                272
              ]
            }
          ],
          "user_mentions": [],
          "symbols": [],
          "media": [
            {
              "id": 1125478846289985500,
              "id_str": "1125478846289985536",
              "indices": [
                274,
                297
              ],
              "media_url": "http://pbs.twimg.com/tweet_video_thumb/D56BDDNUwAAxsUD.jpg",
              "media_url_https": "https://pbs.twimg.com/tweet_video_thumb/D56BDDNUwAAxsUD.jpg",
              "url": "https://t.co/Oir5Hpkb2F",
              "display_url": "pic.twitter.com/Oir5Hpkb2F",
              "expanded_url": "https://twitter.com/TwitterSupport/status/1125479034513645569/photo/1",
              "type": "animated_gif",
              "video_info": {
                "aspect_ratio": [
                  1,
                  1
                ],
                "variants": [
                  {
                    "bitrate": 0,
                    "content_type": "video/mp4",
                    "url": "https://video.twimg.com/tweet_video/D56BDDNUwAAxsUD.mp4"
                  }
                ]
              },
              "sizes": {
                "thumb": {
                  "w": 150,
                  "h": 150,
                  "resize": "crop"
                },
                "small": {
                  "w": 680,
                  "h": 680,
                  "resize": "fit"
                },
                "medium": {
                  "w": 1080,
                  "h": 1080,
                  "resize": "fit"
                },
                "large": {
                  "w": 1080,
                  "h": 1080,
                  "resize": "fit"
                }
              }
            }
          ]
        },

```

## References
- https://stackabuse.com/accessing-the-twitter-api-with-python/
- https://www.dataquest.io/blog/streaming-data-python/
