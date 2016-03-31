'''
Created on Mar 30, 2016

@author: robert
'''
import unittest
from src.tweet_parser import TweetParser
import datetime


class TestTweetParser(unittest.TestCase):


    def test_parse(self):
        line = r'{"created_at":"Thu Nov 05 05:05:39 +0000 2015","id":662133652566835202,"id_str":"662133652566835202","text":"Voto por #Pisteare  de @BANDARECODITOSS en el #elsientometro de @siento5punto1 @ClubBC_RCS @RecoditosPROMO","source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":983741324,"id_str":"983741324","name":"Maggie LM R ","screen_name":"fredycita_maggi","location":"Tlaxcala ","url":null,"description":"Fan No. 1 De Freddy Murillo Tubero de Banda Los Recoditos, Vicepresidenta del Club Bendita Cerveza Tlaxcala \n#SoyRecoditaYEsaSuerteMeToco \n#FredycitaMaggie16","protected":false,"verified":false,"followers_count":247,"friends_count":383,"listed_count":1,"favourites_count":282,"statuses_count":13380,"created_at":"Sun Dec 02 02:30:11 +0000 2012","utc_offset":-21600,"time_zone":"Mexico City","geo_enabled":true,"lang":"es","contributors_enabled":false,"is_translator":false,"profile_background_color":"9AE4E8","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme16\/bg.gif","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme16\/bg.gif","profile_background_tile":false,"profile_link_color":"9E00B3","profile_sidebar_border_color":"BDDCAD","profile_sidebar_fill_color":"DDFFCC","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/631176184886210560\/VXzz9-51_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/631176184886210560\/VXzz9-51_normal.jpg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/983741324\/1443394008","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":{"id":"e9cd17331d4d0d05","url":"https:\/\/api.twitter.com\/1.1\/geo\/id\/e9cd17331d4d0d05.json","place_type":"city","name":"Tlaxcala","full_name":"Tlaxcala, M\u00e9xico","country_code":"MX","country":"M\u00e9xico","bounding_box":{"type":"Polygon","coordinates":[[[-98.295856,19.260740],[-98.295856,19.376095],[-98.197675,19.376095],[-98.197675,19.260740]]]},"attributes":{}},"contributors":null,"is_quote_status":false,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[{"text":"Pisteare","indices":[9,18]},{"text":"elsientometro","indices":[46,60]}],"urls":[],"user_mentions":[{"screen_name":"BANDARECODITOSS","name":"BANDA LOS RECODITOS","id":222291714,"id_str":"222291714","indices":[23,39]},{"screen_name":"siento5punto1","name":"SIENTO 5.1","id":2330737525,"id_str":"2330737525","indices":[64,78]},{"screen_name":"ClubBC_RCS","name":"Club Bendita Cerveza","id":1573506325,"id_str":"1573506325","indices":[79,90]},{"screen_name":"RecoditosPROMO","name":"RecoditosPROMO","id":238339066,"id_str":"238339066","indices":[91,106]}],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"es","timestamp_ms":"1446699939277"}'
        p = TweetParser()
        
        entry = p.parse(line)
        
        self.assertEquals(datetime(2015,11,5,5,5,39), entry[0])
        self.assertEquals({"Pisteare","elsientometro"}, entry[1])


    def test_parse_non_tweet(self):
        line = '{"limit":{"track":1,"timestamp_ms":"1459207521864"}}'
        p = TweetParser()

        entry = p.parse(line)
        
        self.assertTrue(entry is None)
