from splinter import Browser
from dateutil import parser
import re

def main():
    br = Browser()
    name, password = open('login.txt').read().rstrip().split(',')
    br = login(br, name, password)
    song = {'lyrics' : 'yo its kesha,\n do cocaine',
            'genre' : 'pop',
            'primary_artist' : 'Ke$ha',
            'title' : 'kesha loves coke',
            'release_date' : '19880809',
            'featured_artists': 'wayne coyne, nick f',
            'producers': 'kanye, will smith',
            'soundcloud_url' : 'soundcloud.com/kesha/song',
            'youtube_url' : 'youtube.com/keshahash',
            'albums' : 'album1,album2,album3'}
    post_song(song, br)
    song_keys = ['raw_lyrics',
                 'genre',
                 'primary_artist',
                 'title',
                 'release_date, #yyyymmd'
                 'featured_artists',
                 'producers',
                 'soundcloud_url',
                 'youtube_url',
                 'albums']

def post_song(song, browser):
    """ Posts a song to rapgenius through its front end.
    """
    song = transform_song_dict(song)
    print song
    
    browser.visit('http://rapgenius.com')
    browser.click_link_by_text('Add New Song')
    browser.click_link_by_text('Add Additional Metadata')
    
    for key, value in song.iteritems():
        print "key: " + key
        print "value: " + str(value)
        # First check for non form fill-in cases
        # Genre
        if key == 'genre':
            genre_xpath = "id('new_song')/p[1]/label[%s]" % value
            g = browser.find_by_xpath(genre_xpath)
            g.click()
        elif key == 'song_release_date_1i':
            browser.select("song[release_date(1i)]", value)
        elif key == 'song_release_date_2i':
            browser.select("song[release_date(2i)]", value)
        elif key == 'song_release_date_3i':
            browser.select("song[release_date(3i)]", value)
        else:
            if re.match('song_album_appearances.*',key):
                while browser.is_element_not_present_by_id(key):
                    browser.click_link_by_text("Add Album [ + ]")
            browser.find_by_id(key)[0].fill(value)

def transform_song_dict(song):
    """ Convert easily readable key names to ids used in RG's html
    """
    rg_song = {}
    for key, value in song.iteritems():
        if key == 'genre':
            genre_dict = {'rap':'2',
                          'rock':'3',
                          'sports':'4',
                          'pop':'5',
                          'news':'6',
                          'literature':'7',
                          'screen':'8',
                          'history':'9',
                          'misc':'10'}
            rg_song['genre'] = genre_dict[value]
        if key == 'primary_artist':
            rg_song['song_primary_artist'] = value
        if key == 'title':
            rg_song['song_title'] = value
        if key == 'release_date':
            dt = parser.parse(value)
            rg_song['song_release_date_1i'] = dt.year
            rg_song['song_release_date_2i'] = dt.month
            rg_song['song_release_date_3i'] = dt.day
        if key == 'featured_artists':
            rg_song['song_featured_artists'] = value
        if key == 'producers':
            rg_song['song_producer_artists'] = value
        if key == 'soundcloud_url':
            rg_song['song_soundcloud_url'] = value
        if key == 'youtube_url':
            rg_song['song_youtube_url'] = value
        if key == 'albums':
            for i, album in enumerate(value.split(',')):
                if i==0:
                    rg_song['song_album_appearances_attributes_0_album_name'] \
                        = album
                else:
                    rg_song['song_album_appearances_attributes_ + %s + '\
                    '_album_name' % str(i)] = album
        if key == 'lyrics':
            rg_song['song_lyrics'] = value
    return rg_song

def login(browser, name, password):
    """ Logs a user in to rap genius to post songs.
    """
    browser.visit('http://rapgenius.com/login')
    browser.find_by_id('user_session_login').fill(name)
    browser.find_by_id('user_session_password').fill(password)
    login_button = browser.find_by_id('user_session_submit')
    login_button.click()
    browser.visit('http://rapgenius.com')
    return browser

if __name__ == "__main__":
    main()
