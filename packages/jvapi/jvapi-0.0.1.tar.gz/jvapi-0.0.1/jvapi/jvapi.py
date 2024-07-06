import json
import requests

class JVAPIError(Exception):
    """Exception raised for errors in JVAPI interactions."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class JVAPI:
    def __init__(self, apikey):
        self.base_url = "https://jvapi.online"
        self.apikey = apikey
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/51.0.2704.106",
            "apikey": self.apikey
        }

    def _request(self, method, path, headers=None, data=None, files=None, json_data=None):
        url = self.base_url + path
        headers = headers or {}
        headers.update(self.headers)
        response = None
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, data=data, files=files, json=json_data)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JVAPIError(f"Request failed: {e}")

    def status(self):
        return self._request('GET', '/status')

    def youtube_search(self, query):
        return self._request('GET', f'/youtube?query={query}')

    def download_youtube_video(self, video_url):
        data = {'url': video_url}
        return self._request('POST', '/youtubedl', json_data=data)

    def joox(self, query):
        return self._request('GET', f'/joox?query={query}')

    def lyric(self, query):
        return self._request('GET', f'/lyric?query={query}')

    def chord(self, query):
        return self._request('GET', f'/chord?query={query}')

    def smule(self, username):
        return self._request('GET', f'/smule?username={username}')

    def smuledl(self, url):
        return self._request('GET', f'/smuledl?url={url}')

    def tiktok(self, username):
        return self._request('GET', f'/tiktok?username={username}')

    def tiktokdl(self, url):
        return self._request('GET', f'/tiktokdl?url={url}')

    def instagram(self, username):
        return self._request('GET', f'/instagram?username={username}')

    def instapost(self, url):
        return self._request('GET', f'/instapost?url={url}')

    def instastory(self, username):
        return self._request('GET', f'/instastory?username={username}')

    def twitter(self, username):
        return self._request('GET', f'/twitter?username={username}')

    def twitterdl(self, url):
        return self._request('GET', f'/twitterdl?url={url}')

    def facebookdl(self, url):
        return self._request('GET', f'/facebookdl?url={url}')

    def pinterest(self, url):
        return self._request('GET', f'/pinterest?url={url}')

    def github(self, username):
        return self._request('GET', f'/github?username={username}')

    def playstore(self, query):
        return self._request('GET', f'/playstore?query={query}')

    def translate(self, lang, text):
        return self._request('GET', f'/translate/{lang}?text={text}')

    def image(self, query):
        return self._request('GET', f'/image?query={query}')

    def wallpaper(self, query):
        return self._request('GET', f'/wallpaper?query={query}')

    def porn(self, query):
        return self._request('GET', f'/porn?query={query}')

    def pornstar(self):
        return self._request('GET', '/pornstar')

    def hentai(self):
        return self._request('GET', '/hentai')

    def kamasutra(self):
        return self._request('GET', '/kamasutra')

    def dick(self):
        return self._request('GET', '/dick')

    def tits(self):
        return self._request('GET', '/tits')

    def vagina(self):
        return self._request('GET', '/vagina')

    def meme(self, text1, text2, url):
        return self._request('GET', f'/meme/{text1}/{text2}/url={url}')

    def movie(self, query):
        return self._request('GET', f'/movie?query={query}')

    def movie_quotes(self):
        return self._request('GET', '/movie/quotes')

    def cinema(self, city):
        return self._request('GET', f'/cinema?city={city}')

    def tinyurl(self, url):
        return self._request('GET', f'/tinyurl?url={url}')

    def bitly(self, url):
        return self._request('GET', f'/bitly?url={url}')

    def kbbi(self, query):
        return self._request('GET', f'/kbbi?query={query}')

    def topnews(self):
        return self._request('GET', '/topnews')

    def wikipedia(self, query):
        return self._request('GET', f'/wikipedia?query={query}')

    def urban(self, query):
        return self._request('GET', f'/urban?query={query}')

    def zodiac(self, sign):
        return self._request('GET', f'/zodiac?sign={sign}')

    def alquran(self):
        return self._request('GET', '/alquran/list')

    def alquranQS(self, query):
        return self._request('GET', f'/alquran?query={query}')

    def bible(self):
        return self._request('GET', '/bible')

    def adzan(self, city):
        return self._request('GET', f'/adzan?city={city}')

    def cuaca(self, city):
        return self._request('GET', f'/cuaca?city={city}')

    def bmkg(self):
        return self._request('GET', '/bmkg')

    def corona(self):
        return self._request('GET', '/corona')

    def karir(self):
        return self._request('GET', '/karir')

    def cellular(self, query):
        return self._request('GET', f'/cell?query={query}')

    def lahir(self, date):
        return self._request('GET', f'/lahir?date={date}')

    def jadian(self, date):
        return self._request('GET', f'/jadian?date={date}')

    def nama(self, name):
        return self._request('GET', f'/nama?name={name}')

    def mimpi(self, query):
        return self._request('GET', f'/mimpi?query={query}')

    def acaratv(self):
        return self._request('GET', '/acaratv/now')

    def acaratv_channel(self, channel):
        return self._request('GET', f'/acaratv?channel={channel}')

    def cctv_code(self):
        return self._request('GET', '/cctv/code')

    def cctvSearch(self, code):
        return self._request('GET', f'/cctv/search/id={code}')

    def mangaSearch(self, query):
        return self._request('GET', f'/manga/search?query={query}')

    def mangaChapter(self, chapterId):
        return self._request('GET', f'/manga/chapter?chapterId={chapterId}')

    def timeline(self, url):
        return self._request('GET', f'/timeline?url={url}')

    def resi(self, query, code):
        return self._request('GET', f'/resi/{query}={code}')

    def screenshot(self, url):
        return self._request('GET', f'/screenshot?url={url}')

    def imgurl(self, path):
        return self._request('POST', '/imgurl', files={"file": open(path, "rb")})

    def gif(self, query):
        return self._request('GET', f'/gif?query={query}')

    def search(self, query):
        return self._request('GET', f'/search?query={query}')

    def calc(self, query):
        return self._request('GET', f'/calc?query={query}')

    def language(self):
        return self._request('GET', '/language/code')

    def lineapp(self):
        return self._request('GET', '/line')
