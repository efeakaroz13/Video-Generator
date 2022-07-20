from flask import Flask, render_template, request, redirect
import pyttsx3
import requests
from bs4 import BeautifulSoup
import random
from moviepy.editor import *
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import os
import shutil
from google_images_search import GoogleImagesSearch
import subprocess
import moviepy.editor as mp
from moviepy.editor import *
from moviepy.config import change_settings
import shutil
change_settings({"FFMPEG_BINARY": "/opt/local/bin/ffmpeg"})

from security import AUTHMACADDR

# TODO
# AUTH SYSTEM REPORTER - JAVA OR C

myauth = AUTHMACADDR()
myauth.login()

proxiesthing = open("proxy5socks.txt","r").read()
#proxies={"http":proxiesthing,"https":proxiesthing}

engine = pyttsx3.init()
voices = engine.getProperty("voices")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/static/intros"

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/n-tv")
def ntv():
    page = requests.get("https://www.n-tv.de/")
    soup = BeautifulSoup(page.content, "html.parser")
    section_ = soup.find_all("article", {"class": "teaser teaser--wide teaser--hero"})
    out = {"out": []}
    for s in section_:
        data = {
            "img": str(s.find_all("img")[0]),
            "text": s.find_all("p", {"class": "teaser__text"})[0].get_text(),
            "title": s.find_all("span", {"class": "teaser__headline"})[0].get_text(),
            "href": s.find_all("a")[0].get("href"),
        }
        out["out"].insert(0, data)

    return out


@app.route("/video_gen_ntv", methods=["POST"])
def video_gen_ntv():
    try:
        url = request.form.get("url")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        for div in soup.find_all(
            "div", {"class": "article__aside article__aside--right"}
        ):
            div.decompose()
        text = fullarticle = soup.find_all("div", {"class": "article__text"})[
            0
        ].get_text()
        title = soup.find_all("title")[0].get_text()

        return {"done": True, "text": text, "url": url, "title": title}
    except Exception as e:

        print(e)
        return {"done": False}


@app.route("/get_img")
def get_img():
    duration = request.args.get("d")
    keyword = request.args.get("q")
    page = requests.get(f"https://unsplash.com/s/photos/{keyword.replace(' ','-')}")
    soup = BeautifulSoup(page.content, "html.parser")
    out = []
    images = []
    used = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    all_h3 = soup.find_all("img")
    for h in all_h3:
        try:
            width = h.get("width")

            try:

                if width != "32":
                    if h.get("style") == "display:none":
                        pass
                    else:
                        try:
                            h.get("src").split("w=0")[1]
                        except:
                            out.insert(0, h.get("src"))

                else:
                    pass
            except Exception as e:
                print(e)
                try:
                    h.get("src").split("w=0")[1]
                except:
                    out.insert(0, h.get("src"))
        except:
            pass
    s = requests.Session()
    for o in out[:15]:
        try:
            o.split("w=1000")[1]
            filename = f"{random.randint(1,123534546)}.png"
            used.insert(0, o)
            image = s.get(o, headers=headers, stream=True)

            with open(filename, "wb") as file:
                # file.write(image.content)
                shutil.copyfileobj(image.raw, file)
                images.insert(0, filename)
        except:
            pass

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1920)

    concat_clip.write_videofile("static/out.mp4", fps=60, logger=None)
    for i in images:
        os.system("rm {}".format(i))

    return f"""
		<video width="320" height="240" controls>
		  <source src="/static/out.mp4" type="video/mp4">
		  Error Message
		</video>

		<br>
		{used}<br>
		{len(images)}
	"""


@app.route("/image_search_google")
def image_search_google_api():
    duration = 120
    q = request.args.get("q")
    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived
    _search_params = {
        "q": q,
        "num": 10,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }
    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)

        images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images.reverse()]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)
    myauth.login()

    concat_clip.write_videofile("static/out.mp4", fps=30, logger=None, threads=4)
    for i in images:
        os.system("rm '{}'".format(i))
    return str(images)


@app.route("/ntv_video_gen_full")
def video_generator_ntv_withgimages():
    # TEXT AND TITLE
    outfilename = f"IPK{random.randint(1,1000000000000000)}"

    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for div in soup.find_all("div", {"class": "article__aside article__aside--right"}):
        div.decompose()
    text = fullarticle = soup.find_all("div", {"class": "article__text"})[0].get_text()
    title = soup.find_all("title")[0].get_text()

    # TEXT TO SPEECH
    all_v = []
    engine = pyttsx3.init(driverName="nsss")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[4].id)
    newVoiceRate = 145
    engine.setProperty("rate", newVoiceRate)
    engine.save_to_file(text, f"{outfilename}.mp3")

    engine.runAndWait()
    for v in voices:
        all_v.insert(0, f"{v} - {voices.index(v)}")

    # IMAGES
    # duration calculator
    fname = outfilename + ".mp3"
    my_text = str(
        subprocess.check_output(
            "ffmpeg -i ./{} 2>&1 |grep Duration ".format(fname), shell=True
        )
    )

    def calculator(text):
        return text.split(",")[0].split("Duration: ")[1]

    duration = int(calculator(my_text).split(".")[0].split(":")[1]) * 60 + int(
        calculator(my_text).split(".")[0].split(":")[2]
    )

    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived
    _search_params = {
        "q": title,
        "num": 15,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }
    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)
        try:
            images.index(image.path)
        except:
            images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)

    concat_clip.write_videofile(
        f"static/{outfilename}.mp4", fps=30, logger=None, threads=4
    )
    for i in images:
        os.system("rm '{}'".format(i))

    "ffmpeg -i test.mp4 -i ./out/NationalBasketballAssociation.mp3 -map 0:v -map 1:a -c:v copy -shortest ./video/NationalBasketballAssociation.mp4"
    os.system(
        f"ffmpeg -i ./static/{outfilename}.mp4  -i {outfilename}.mp3 -map 0:v -map 1:a -c:v copy -shortest ./static/out/{outfilename}.mp4 "
    )
    os.system(f"rm '{outfilename}.mp3'")
    os.system(f"rm './static/{outfilename}.mp4'")

    return {"done": True, "text": text, "url": url, "title": title}


@app.route("/personaltrainer_scraper_list")
def personaltrainer():
    page = requests.get("https://m.my-personaltrainer.it/farmaci/index.html")
    soup = BeautifulSoup(page.content, "html.parser")
    out = []
    all_articletitles = soup.find_all("li", {"class": "sal-anchor-list-item"})
    for a in all_articletitles:
        title = a.get_text()
        url = a.find_all("a")[0].get("href")
        try:
            url.split("https://")[1]
            out.insert(0, {"title": title, "href": url})
        except:

            out.insert(
                0, {"title": title, "href": "https://m.my-personaltrainer.it" + url}
            )

    return {"done": True, "out": out}


@app.route("/article-personaltrainer")
def artpertrain():
    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    out = soup.find("div", {"id": "toc-hook"})
    out.find_all(
        "div", {"class": "sal-leaf-indice sal-leaf-indice-leaflet sal-mBottom4x"}
    )[0].decompose()
    text = out.get_text()
    title = soup.find_all("title")[0].get_text()

    return {"title": title, "out": str(out.get_text())}


@app.route("/personal_trainer_video_gen_full")
def video_generator_personal_trainer_withgimages():
    # TEXT AND TITLE
    outfilename = f"PT{random.randint(1,1000000000000000)}"

    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    out = soup.find("div", {"id": "toc-hook"})
    out.find_all(
        "div", {"class": "sal-leaf-indice sal-leaf-indice-leaflet sal-mBottom4x"}
    )[0].decompose()
    text = out.get_text()
    title = soup.find_all("title")[0].get_text()

    # TEXT TO SPEECH
    all_v = []
    engine = pyttsx3.init(driverName="nsss")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    newVoiceRate = 145
    engine.setProperty("rate", newVoiceRate)
    myauth.login()
    engine.save_to_file(text, f"{outfilename}.mp3")

    engine.runAndWait()
    for v in voices:
        all_v.insert(0, f"{v} - {voices.index(v)}")

    # IMAGES
    # duration calculator
    fname = outfilename + ".mp3"
    my_text = str(
        subprocess.check_output(
            "ffmpeg -i ./{} 2>&1 |grep Duration ".format(fname), shell=True
        )
    )

    def calculator(text):
        return text.split(",")[0].split("Duration: ")[1]

    duration = int(calculator(my_text).split(".")[0].split(":")[1]) * 60 + int(
        calculator(my_text).split(".")[0].split(":")[2]
    )

    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived
    _search_params = {
        "q": title,
        "num": 10,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }
    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)
        try:
            images.index(image.path)
        except:
            images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)
    myauth.login()

    concat_clip.write_videofile(
        f"static/{outfilename}.mp4", fps=30, logger=None, threads=4
    )
    for i in images:
        os.system("rm '{}'".format(i))

    "ffmpeg -i test.mp4 -i ./out/NationalBasketballAssociation.mp3 -map 0:v -map 1:a -c:v copy -shortest ./video/NationalBasketballAssociation.mp4"
    os.system(
        f"ffmpeg -i ./static/{outfilename}.mp4  -i {outfilename}.mp3 -map 0:v -map 1:a -c:v copy -shortest ./static/out/{outfilename}.mp4 "
    )
    os.system(f"rm '{outfilename}.mp3'")
    os.system(f"rm './static/{outfilename}.mp4'")

    return {"done": True, "text": text, "url": url, "title": title}


@app.route("/thwwomscrappe")
def thewomtextart():
    url = "https://healthy.thewom.it/terapie/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    out = []
    all_titles = soup.find_all("h3", {"class": "entry-title sal-list-item-title"})
    for t in all_titles:
        out.append({"title": t.get_text(), "href": t.find_all("a")[0].get("href")})
    return {"out": out, "done": True}


@app.route("/article/thewom.it")
def art_thewom():
    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article = soup.find("div", {"id": "toc-hook"})

    return {"done": True, "text": article.get_text()}


@app.route("/generate/thewom.it")
def genthewom():

    # TEXT AND TITLE
    outfilename = f"THEWOM{random.randint(1,1000000000000000)}"

    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find("div", {"id": "toc-hook"}).get_text()
    title = soup.find_all("title")[0].get_text()

    # TEXT TO SPEECH
    all_v = []
    engine = pyttsx3.init(driverName="nsss")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    newVoiceRate = 145
    engine.setProperty("rate", newVoiceRate)
    engine.save_to_file(text, f"{outfilename}.mp3")
    myauth.login()

    engine.runAndWait()
    for v in voices:
        all_v.insert(0, f"{v} - {voices.index(v)}")

    # IMAGES
    # duration calculator
    fname = outfilename + ".mp3"
    my_text = str(
        subprocess.check_output(
            "ffmpeg -i ./{} 2>&1 |grep Duration ".format(fname), shell=True
        )
    )

    def calculator(text):
        return text.split(",")[0].split("Duration: ")[1]

    duration = int(calculator(my_text).split(".")[0].split(":")[1]) * 60 + int(
        calculator(my_text).split(".")[0].split(":")[2]
    )

    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived
    _search_params = {
        "q": title,
        "num": 10,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }
    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)
        try:
            images.index(image.path)
        except:
            images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)

    concat_clip.write_videofile(
        f"static/{outfilename}.mp4", fps=30, logger=None, threads=4
    )
    for i in images:
        os.system("rm '{}'".format(i))

    "ffmpeg -i test.mp4 -i ./out/NationalBasketballAssociation.mp3 -map 0:v -map 1:a -c:v copy -shortest ./video/NationalBasketballAssociation.mp4"
    os.system(
        f"ffmpeg -i ./static/{outfilename}.mp4  -i {outfilename}.mp3 -map 0:v -map 1:a -c:v copy -shortest ./static/out/{outfilename}.mp4 "
    )
    os.system(f"rm '{outfilename}.mp3'")
    os.system(f"rm './static/{outfilename}.mp4'")

    return {"done": True, "text": text, "url": url, "title": title}


@app.route("/list/netdoktor")
def netdoktorde():
    page = requests.get("https://www.netdoktor.de")
    soup = BeautifulSoup(page.content, "html.parser")
    infothing = soup.find_all("span", {"class": "title"})
    out = []
    for i in infothing:
        title = i.get_text()
        href = i.parent.parent.parent.parent.find_all("a")[0].get("href")
        out.append({"title": title, "href": href})

    return {"done": True, "out": out}


@app.route("/article/netdoktor")
def articlescrapperfornetdoktor():
    url = request.args.get("q")
    page = requests.get(url)
    myauth.login()
    soup = BeautifulSoup(page.content, "html.parser")
    text = ""
    text_divs = soup.find_all("div", {"class": "widget-text plugin_text_margin"})
    for t in text_divs:
        text = text + "\n" + t.get_text()

    title = soup.find_all("title")[0].get_text().split(":")[0]

    return {"done": True, "title": title, "out": text}


@app.route("/video/gen/netdoktor")
def video_generator_netdoktor_withgimages():
    # TEXT AND TITLE
    outfilename = f"NETDOCTOR{random.randint(1,1000000000000000)}"

    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = ""
    text_divs = soup.find_all("div", {"class": "widget-text plugin_text_margin"})
    for t in text_divs:
        text = text + "\n" + t.get_text()

    title = soup.find_all("title")[0].get_text().split(":")[0]

    # TEXT TO SPEECH
    all_v = []
    engine = pyttsx3.init(driverName="nsss")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[4].id)
    newVoiceRate = 145
    engine.setProperty("rate", newVoiceRate)
    engine.save_to_file(text, f"{outfilename}.mp3")

    engine.runAndWait()
    for v in voices:
        all_v.insert(0, f"{v} - {voices.index(v)}")

    # IMAGES
    # duration calculator
    fname = outfilename + ".mp3"
    my_text = str(
        subprocess.check_output(
            "ffmpeg -i ./{} 2>&1 |grep Duration ".format(fname), shell=True
        )
    )

    def calculator(text):
        return text.split(",")[0].split("Duration: ")[1]

    duration = int(calculator(my_text).split(".")[0].split(":")[1]) * 60 + int(
        calculator(my_text).split(".")[0].split(":")[2]
    )

    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived

    _search_params = {
        "q": title,
        "num": 15,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }

    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)
        try:
            images.index(image.path)
        except:
            images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)

    concat_clip.write_videofile(
        f"static/{outfilename}.mp4", fps=30, logger=None, threads=4
    )
    for i in images:
        os.system("rm '{}'".format(i))

    "ffmpeg -i test.mp4 -i ./out/NationalBasketballAssociation.mp3 -map 0:v -map 1:a -c:v copy -shortest ./video/NationalBasketballAssociation.mp4"
    os.system(
        f"ffmpeg -i ./static/{outfilename}.mp4  -i {outfilename}.mp3 -map 0:v -map 1:a -c:v copy -shortest ./static/out/{outfilename}.mp4 "
    )
    os.system(f"rm '{outfilename}.mp3'")
    myauth.login()
    os.system(f"rm './static/{outfilename}.mp4'")

    return {"done": True, "text": text, "url": url, "title": title}



@app.route("/list/storiestogrowby")
def storiestogrowbyarticle():
	page = requests.get("https://storiestogrowby.org/bedtime-stories-kids-free/")
	soup = BeautifulSoup(page.content,"html.parser")
	out = []
	all_h3 = soup.find_all("h3")
	for h in all_h3:
		try:
			href = h.find_all("a")[0].get("href")
			title = h.get_text()
			out.append({"title":title,"href":href})
		except:
			pass

	return {"done":True,"out":out}

@app.route("/article/storiestogrowby")
def singlearticlescrapper():
	url = request.args.get("q")
	page = requests.get(url)
	soup = BeautifulSoup(page.content,"html.parser")

	text = soup.find_all("div",{"class":"siteorigin-widget-tinymce textwidget"})[0].get_text()
	title = soup.find_all("title")[0].get_text()
	source = soup.find_all("source")[0].get("src")

	return {"audio":source,"done":True,"title":title,"text":text}

@app.route("/video/gen/storiestogrowby")
def video_generator_storiestogrowby_withgimages():
    # TEXT AND TITLE
    outfilename = f"STORIES{random.randint(1,1000000000000000)}"

    url = request.args.get("q")
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")

    text = soup.find_all("div",{"class":"siteorigin-widget-tinymce textwidget"})[0].get_text()
    title = soup.find_all("title")[0].get_text()

    # TEXT TO SPEECH
    #Site voice

    all_v = []
    engine = pyttsx3.init(driverName="nsss")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[7].id)
    newVoiceRate = 145
    engine.setProperty("rate", newVoiceRate)
    #engine.save_to_file(text, f"{outfilename}.mp3")

    #engine.runAndWait()
    for v in voices:
        all_v.insert(0, f"{v} - {voices.index(v)}")

    source = soup.find_all("source")[0].get("src")
    download = requests.get(source)
    with open(outfilename+".mp3","wb") as f:
    	f.write(download.content)

    # IMAGES
    # duration calculator
    fname = outfilename + ".mp3"
    my_text = str(
        subprocess.check_output(
            "ffmpeg -i ./{} 2>&1 |grep Duration ".format(fname), shell=True
        )
    )

    def calculator(text):
        return text.split(",")[0].split("Duration: ")[1]

    duration = int(calculator(my_text).split(".")[0].split(":")[1]) * 60 + int(
        calculator(my_text).split(".")[0].split(":")[2]
    )

    images = []
    key = "AIzaSyD31rz2D0ZgkPZtOYBz3U2J0b0oSNGM5xU"
    gis = GoogleImagesSearch(key, "0cb3ac5a5df2563b5")
    # |cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived

    _search_params = {
        "q": title,
        "num": 15,
        "fileType": "jpg",
        "rights": "",
        "safe": "safeUndefined",  ##
        "imgType": "imgTypeUndefined",  ##
        "imgSize": "imgSizeUndefined",  ##
        "imgDominantColor": "imgDominantColorUndefined",  ##
        "imgColorType": "imgColorTypeUndefined",  ##
    }

    gis.search(search_params=_search_params)
    for image in gis.results():

        url = image.url
        ref = image.referrer_url
        # therandomnum = random.randint(234234,3245345456)
        # image_name = "{}IPKEFE".format(therandomnum)

        image.download("./static/")
        image.resize(1280, 720)
        try:
            images.index(image.path)
        except:
            images.insert(0, image.path)

    dperimg = int(duration) / len(images)

    clips = [ImageClip("./" + m).set_duration(dperimg) for m in images]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # audioclip = AudioFileClip(fname)
    # concat_clip.set_audio(audioclip)
    concat_clip.resize(width=1280, height=720)

    concat_clip.write_videofile(
        f"static/{outfilename}.mp4", fps=30, logger=None, threads=4
    )
    for i in images:
        os.system("rm '{}'".format(i))

    "ffmpeg -i test.mp4 -i ./out/NationalBasketballAssociation.mp3 -map 0:v -map 1:a -c:v copy -shortest ./video/NationalBasketballAssociation.mp4"
    os.system(
        f"ffmpeg -i ./static/{outfilename}.mp4  -i {outfilename}.mp3 -map 0:v -map 1:a -c:v copy -shortest ./static/out/{outfilename}.mp4 "
    )
    os.system(f"rm '{outfilename}.mp3'")
    myauth.login()
    os.system(f"rm './static/{outfilename}.mp4'")

    return {"done": True, "text": text, "url": url, "title": title}

@app.route("/proxy-change",methods=["POST","GET"])
def proxychanger():
	if request.method == "POST":
		try:
			proxyfile = open("proxy5socks.txt","w")
			proxyurl  = request.form.get("socks5proxy")
			proxytester = requests.get("http://ip-api.com/json",proxies={"http":proxyurl,"https":proxyurl})
			proxyfile.write(proxyurl)
				
			return redirect("/proxy-change?q=COMPLETED+TASK&ipinf="+str(proxytester.content))
	
		except Exception as e:
			return redirect("/proxy-change?q=PROXY+IS+NOT+WORKING&ipinf="+str(e))


	q= request.args.get("q")
	if q == None:
		q=""

	ipinf = request.args.get("ipinf")
	if ipinf == None:
		proxycurrent = open("proxy5socks.txt","r")
		thetext = proxycurrent.read()
		if len(thetext)<4:
			ipinf=""
		else:
			try:
				ipinf = str(requests.get("http://ip-api.com/json",proxies={"http":thetext,"https":thetext}).content)

	
			except Exception as e:
				ipinf=str(e)
				

	return """

	<html>
	<head>
		<title>ANTON PROXY CONFIGURATION</title>
		<link rel="shortcut icon" src="https://upload.wikimedia.org/wikipedia/tr/9/95/Seal_of_the_Turkish_Armed_Forces.png">
	</head>
	<body>
		<form action="" method="POST">

			<input type="text" name="socks5proxy" placeholder="Enter Proxy(socks5)">

			<button>SUBMIT</button>
			<p>OUT:"""+q+"""<br>"""+ipinf.replace(',','<br><br>')+"""</p>
		</form>
	</body>
	</html>

	"""

@app.route("/introadder",methods=["POST","GET"])
def addintro():
    allintros=os.listdir("static/intros")
    if request.method == "POST":
        introfile = request.files["introup"]
        introfile.save(os.path.join('static/intros', introfile.filename))
        os.system(f"ffmpeg -y -i static/intros/{introfile.filename} -vf scale=1280:720 -preset slow -crf 18 static/intros/{introfile.filename}")
        return redirect("/introadder")
    allvideos = os.listdir("static/out")
    return render_template("intro.html",generated_videos=allvideos,intros=allintros)
@app.route("/ffmpegvidmerge")
def videomerger():

    introfile = request.args.get("intro")
    videofile = request.args.get("videofile")
    txtfilename = videofile.replace(".mp4",".txt")
    videofilefullpath = f'static/out/{videofile}'
    introfilefullpath = f'static/intros/{introfile}'
    clip = mp.VideoFileClip(videofilefullpath)
    clip_resized = clip.resize((1280,720))
    clip_resized.write_videofile(videofilefullpath, temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac",fps=20)

    open("fileclip.txt","w").write(f"""file '{introfilefullpath}'\nfile '{videofilefullpath}'""")
    os.system(f"ffmpeg -y -f concat -i fileclip.txt -c:a aac -strict experimental {videofile}")
    videos_all=[introfilefullpath,videofilefullpath]
    os.rename(f"./{videofile}",f"./static/yt/{videofile}")
    

    return {"done":True,"outname":f"/static/ytuploadredy/{videofile}"}

@app.route("/ytuploader")
def loaderuploaderthing():
    preparedvideos = os.listdir("static/yt")
    return render_template("YTSTD.html",preparedvideos=preparedvideos)

@app.route("/upload/yt")
def uploadyt():
    filepath = request.args.get("file")
    title=request.args.get("title")
    uploadoption = request.args.get("uploadoption")
    os.system(f"""python3 ytuploadtests.py --file static/yt/{filepath} --title="{title}" --privacyStatus={uploadoption}""")
    return {"done":True}
"""
	1- https://www.n-tv.de/
	2- https://www.netdoktor.de
	3- https://m.my-personaltrainer.it/farmaci/index.html
	4- https://healthy.thewom.it/terapie/
	5- https://storiestogrowby.org/bedtime-stories-kids-free/
"""

if __name__ == "__main__":

    app.run(debug=True,threaded=True)
"""
"""
