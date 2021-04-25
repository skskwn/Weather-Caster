import pygame
import win32com.client
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import urllib.request as req
import time

tts = win32com.client.Dispatch("SAPI.SpVoice")

location = input("지역을 입력하세요>>> ")


music_file = "a.mp3"   



freq = 44100   # 샘플링 속도, 44100(CD), 16000(Naver TTS), 24000(google TTS)
bitsize = -16   
channels = 1   # 1로 설정하면 모노, 2로 설정하면 스테레오
buffer = 2048   



pygame.mixer.init(freq, bitsize, channels, buffer, )
pygame.mixer.music.load(music_file)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()




# 기상청 URL
url = 'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp'
res = req.urlopen(url)
#beautifulsoup 으로 분석
soup = BeautifulSoup(res, 'html.parser')

#데이터 추출
title = soup.find("title").string
wf = soup.find("wf").string.replace('<br /> ', '').replace('<br />○', '').replace('(풍랑)', '풍랑에 대해서 알아보겠습니다.').replace('(주말전망)', '주말전망에 대해서 알아보겠습니다.').replace('(해상)', '해상에 대해서 알아보겠습니다.').replace('○', '').replace(' ', '  ').replace('(강수)', '강수에 대해서 알아보겠습니다. ').replace('(수)', ' 수요일  ').replace('~', ' 에서 ').replace('(화)', ' 화요일  ').replace('(목)', ' 목요일  ').replace('(금)', ' 금요일  ').replace('(토)', ' 토요일  ').replace('(월)', ' 월요일  ').replace('(일)', ' 일요일  ').replace('(기온)', ' 기온에 대해서 살펴보겠습니다.').replace('(건조)', '대기도 건조합니다.').replace('(너울)', '너울도 있습니다.')



print('안녕하세요 오늘도 좋은 하루입니다. 날씨정보 브리핑을 시작하겠습니다. 먼저 전국적인 날씨 한번 알아보겠습니다.')
tts.Speak('안녕하세요 ,  오늘도 좋은하루입니다. , 날씨정보 브리핑을 시작하겠습니다. 먼저 전국적인 날씨 한번 알아보겠습니다.')
print(wf.replace(' ', ''))
tts.Speak(wf)





Finallocation = location + '날씨'
LocationInfo = ""
NowTemp = ""
CheckDust = []

url = 'https://search.naver.com/search.naver?query=' + Finallocation
hdr = {'User-Agent': ('mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
req = requests.get(url, headers=hdr)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

# 오류 체크
ErrorCheck = soup.find('span', {'class' : 'btn_select'})

if 'None' in str(ErrorCheck):
    print("Error!")
else:
    # 지역 정보
    for i in soup.select('span[class=btn_select]'):
        LocationInfo = i.text

    # 현재 온도
    NowTemp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span', {'class' : 'tempmark'}).text[2:]

    # 날씨 캐스트
    WeatherCast = soup.find('p', {'class' : 'cast_txt'}).text

    # 오늘 오전온도, 오후온도, 체감온도
    TodayMorningTemp = soup.find('span', {'class' : 'min'}).text
    TodayAfternoonTemp = soup.find('span', {'class' : 'max'}).text
    TodayFeelTemp = soup.find('span', {'class' : 'sensible'}).text[5:]

    # 자외선 지수
    TodayUV = soup.find('span', {'class' : 'indicator'}).text[4:-2] + " " + soup.find('span', {'class' : 'indicator'}).text[-2:]

    # 미세먼지, 초미세먼지, 오존 지수
    CheckDust1 = soup.find('div', {'class': 'sub_info'})
    CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
    for i in CheckDust2.select('dd'):
        CheckDust.append(i.text)
    FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
    UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
    Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]

    # 내일 오전, 오후 온도 및 상태 체크
    tomorrowArea = soup.find('div', {'class': 'tomorrow_area'})
    tomorrowCheck = tomorrowArea.find_all('div', {'class': 'main_info morning_box'})

    # 내일 오전온도
    tomorrowMoring1 = tomorrowCheck[0].find('span', {'class': 'todaytemp'}).text
    tomorrowMoring2 = tomorrowCheck[0].find('span', {'class' : 'tempmark'}).text[2:]
    tomorrowMoring = tomorrowMoring1 + tomorrowMoring2

    # 내일 오전상태
    tomorrowMState1 = tomorrowCheck[0].find('div', {'class' : 'info_data'})
    tomorrowMState2 = tomorrowMState1.find('ul', {'class' : 'info_list'})
    tomorrowMState3 = tomorrowMState2.find('p', {'class' : 'cast_txt'}).text
    tomorrowMState4 = tomorrowMState2.find('div', {'class' : 'detail_box'})
    tomorrowMState5 = tomorrowMState4.find('span').text.strip()
    tomorrowMState = tomorrowMState3 + " " + tomorrowMState5

    # 내일 오후온도
    tomorrowAfter1 = tomorrowCheck[1].find('p', {'class' : 'info_temperature'})
    tomorrowAfter2 = tomorrowAfter1.find('span', {'class' : 'todaytemp'}).text
    tomorrowAfter3 = tomorrowAfter1.find('span', {'class' : 'tempmark'}).text[2:]
    tomorrowAfter = tomorrowAfter2 + tomorrowAfter3

    # 내일 오후상태
    tomorrowAState1 = tomorrowCheck[1].find('div', {'class' : 'info_data'})
    tomorrowAState2 = tomorrowAState1.find('ul', {'class' : 'info_list'})
    tomorrowAState3 = tomorrowAState2.find('p', {'class' : 'cast_txt'}).text
    tomorrowAState4 = tomorrowAState2.find('div', {'class' : 'detail_box'})
    tomorrowAState5 = tomorrowAState4.find('span').text.strip()
    tomorrowAState = tomorrowAState3 + " " + tomorrowAState5

    print("=========================================")
    print(LocationInfo + "의 오늘 날씨 알아보겠습니다.")
    tts.Speak(LocationInfo + "의 오늘 날씨 알아보겠습니다.")
    print("=========================================")
    print("현재온도는 " + NowTemp + '이며')
    tts.Speak("현재온도는 " + NowTemp + '이며')
    print("체감온도는 " + TodayFeelTemp + '입니다.')
    tts.Speak("체감온도는 " + TodayFeelTemp + '도 입니다.')
    print("오전/오후 온도도 살펴보겠습니다." +'오전에 온도는' + TodayMorningTemp + "이며" + ' 오후에 온도는'+ TodayAfternoonTemp + '입니다.')
    tts.Speak("오전 과 오후 온도도 살펴보겠습니다." +', 오전에 온도는' + TodayMorningTemp + "도 이며" + ', 오후에 온도는'+ TodayAfternoonTemp + '도 입니다.')
    print("현재 상태는 " + WeatherCast.replace('높아요', '높습니다.').replace('낮아요', '낮습니다.'))
    tts.Speak("현재 상태는 " + WeatherCast.replace('높아요', '도 높습니다.').replace('낮아요', '도 낮습니다.'))
    print("현재 자외선 지수는 " + TodayUV + '입니다.')
    tts.Speak("현재 자외선 지수는 , " + TodayUV + '입니다.')
    print("현재 미세먼지 농도는 " + FineDust + '입니다.')
    tts.Speak("현재 미세먼지 농도는 , " + FineDust.replace('/', '마이크로그램 퍼 세제곱미터 ,') + ' 입니다.')
    print("현재 초미세먼지 농도는 " + UltraFineDust + '입니다.')
    tts.Speak("현재 초미세먼지 농도는 , " + UltraFineDust.replace('/', '마이크로그램 퍼 세제곱미터 ,') + ' 입니다.')
    print("현재 오존 지수는 " + Ozon + '입니다.')
    tts.Speak("현재 오존 지수는 , " + Ozon.replace('ppm', 'ppm , ') + '입니다.')
    print("=========================================")
    print(LocationInfo + "의 내일 날씨 알아보겠습니다.")
    tts.Speak(LocationInfo + "의 내일 날씨 알아보겠습니다.")
    print("=========================================")
    print("내일 오전 온도는 " + tomorrowMoring + '입니다.')
    tts.Speak("내일 오전 온도는 " + tomorrowMoring + '입니다.')
    print("내일 오전 상태는 " + tomorrowMState + '입니다.')
    tts.Speak("내일 오전 상태는 " + tomorrowMState + '입니다.')
    print("내일 오후 온도는 " + tomorrowAfter + '입니다.')
    tts.Speak("내일 오후 온도는 " + tomorrowAfter + '입니다.')
    print("내일 오후 상태는 " + tomorrowAState + '입니다.')
    tts.Speak("내일 오후 상태는 " + tomorrowAState + '입니다.')
    print("이상 날씨정보 알려드렸습니다. 감사합니다.")
    tts.Speak("이상 날씨정보 알려드렸습니다. 감사합니다.")









clock = pygame.time.Clock()
while pygame.mixer.music.get_busy():
    clock.tick(30)
    pygame.mixer.quit()
