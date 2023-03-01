from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import extract
from flask_apscheduler import APScheduler
from merge_video import merge
import config
from delete_videos import delete_older_videos
from YtVideo import YtVideo


class Config:
    ''' Configuration class for '''
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route("/", methods=['GET', 'POST'])
def index():
    ''' Main page '''
    if request.method == "POST":
        url = request.form.get('video_url', 0)
        id = extract.video_id(url)
        return redirect(url_for('video_options', id=id), code=302)

    return render_template('base.html')


@app.route("/video/<id>")
def video_options(id):
    ''' Page with video info, available video options and download links. '''
    video = YtVideo(id)
    data = video.get_options()
    return render_template('download_video.html', data = data)


@app.route("/download/<id>/<itag>/")
def download(id, itag):
    ''' Endpoint for downloading the video with provided itag and trim timestamps (Optional). '''

    video = YtVideo(id)
    video.download_video_and_audio(itag)

    start = request.args.get('start')
    end = request.args.get('end')

    filename = id + '.mp4'

    print('Merging audio and video...')
    merged_video = merge(filename, start, end)

    return send_file(
        merged_video,
        as_attachment=True,
        download_name=video.title + '.mp4',
        mimetype="video/mp4")


@scheduler.task('interval', id='do_job_1', seconds=config.FILE_DELETE_TIME, misfire_grace_time=900)
def video_cleaner_schedule():
    ''' Scheduled task for removing old downloaded videos from files folder. '''
    deleted_files = delete_older_videos()
    print(f"Removed {deleted_files} old video files.")