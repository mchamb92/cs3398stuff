import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .create_speech_form import Create_speechForm
from pathlib import Path
from flask import url_for

create_speech_blueprint = Blueprint('create_speech', __name__)

@create_speech_blueprint.route('/create_speech', methods=['GET', 'POST'])
@app.route('/create_speech', methods = ['GET', 'POST'])
def create_speech():
    form = Create_speechForm(request.form)

    if request.method == 'POST':
        if form.validate():
            try:
                audio_filename = "output.mp3"
                static_folder = app.static_folder
                audio_file_path = os.path.join(static_folder, audio_filename)

                client = OpenAI()

                response = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=form.prompt.data
                )

                with open(audio_file_path, 'wb') as audio_file:
                    audio_file.write(response.content)

                audio_file_url = url_for('static', filename='output.mp3')
                return render_template('create_speech.html', form=form, create_speechprompt=form.prompt.data, create_speechresponse=audio_file_url, success=True)
            except Exception as e:
                # Handle OpenAI API or any other exceptions
                return render_template('create_speech.html', form=form, error=str(e))
        else:
            return render_template('create_speech.html', form=form)

    elif request.method == 'GET':
        return render_template('create_speech.html', form=form)
