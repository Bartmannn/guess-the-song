from flask import Blueprint, render_template, redirect, url_for, Response, request
from downloader import download_music 

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        links = request.form.get("link")
        return redirect(url_for(".streamp3", link=links))

    return render_template("index.html")

@views.route("/mp3")
def streamp3():

    links = request.args["link"]
    links = links.replace(" ", "").split(",")
    dest_path = "./website/static/music/"
    ext = "mp3"
    titles = download_music(links, ext, dest_path, 15)
    
    def generate(path=dest_path, titles=titles, ext=ext):
        for title in titles:
            with open(f"{path}{title}.{ext}", "rb") as fmp3:
                data = fmp3.read(1024)
                while data:
                    yield data
                    data = fmp3.read(1024)
    return Response(generate(), mimetype="audio/mp3")
