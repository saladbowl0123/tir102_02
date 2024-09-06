'''
-*- coding: utf-8 -*-

Reference: https://github.com/line/line-bot-sdk-python/tree/master

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
Google Cloud Run functions usage
Runtime: Python >= 3.8, usually 3.12
Entry point: callback
'''

import functions_framework
from flask import Flask, request, abort
import check_date
import extend_url
import select_from_bigquery
import os
import json
import random

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

app = Flask(__name__)

with open(os.path.join(os.path.dirname(__file__), 'line_channel_details.json')) as f:
    line_channel_details = json.load(f)

    channel_access_token = line_channel_details['channel_access_token']
    channel_secret = line_channel_details['channel_secret']

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

@functions_framework.http
@app.route("/callback", methods=['POST'])
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    BUTTONS_USAGE = '點選按鈕了解更多資訊 Tap a button to learn more\n向右滑動以查看更多按鈕 Scroll right for more buttons'

    INVALID_DATE = '日期無效 Invalid date'
    DATE_USAGE = '日期用法 Date usage: `yyyy-mm-dd`'
    DATE_OUT_OF_RANGE = '以前無資料 No data before'
    NO_DATA_TODAY = '尚未獲得今日資料 Data not yet available for today'
    NO_DATA_AT_DATE = '無資料 No data at'

    APOD_COLUMN_NAMES_OUTPUT_ORDER = [
        'date',
        'title',
        'explanation',
        'copyright',
    ]

    user_input = event.message.text
    user_input = user_input.strip()
    user_input = user_input.lower()

    messages = []

    text_list = []

    labels = None

    if user_input.lower().islower():
        # contains an English letter, so search for English tag
        if user_input in ['planet', 'planets']:
            text_list.append(BUTTONS_USAGE)
            planet_names = select_from_bigquery.query_planet_names()
            labels = [planet.title() for planet in planet_names]
        elif user_input in ['constellation', 'constellations']:
            text_list.append(BUTTONS_USAGE)
            constellation_names = select_from_bigquery.query_constellation_names()
            labels = [constellation.title() for constellation in constellation_names]
        elif user_input in ['satellite', 'satellites']:
            # TODO
            pass
        elif user_input in ['comet', 'comets']:
            comets = select_from_bigquery.query_comets()
            comets_describe = comets.describe()
            df_text = reformat_describe_df(comets_describe)
            text_list.append(df_text)
        elif user_input in ['shower', 'showers']:
            showers = select_from_bigquery.query_showers()
            showers_describe = showers.describe()
            df_text = reformat_describe_df(showers_describe)
            text_list.append(df_text)
        else:
            # get random image or video corresponding to tag if possible
            dates = select_from_bigquery.query_english_tag(user_input)

            if dates:
                date = random.choice(dates)
                apod = select_from_bigquery.query_apod(date)

                for column in APOD_COLUMN_NAMES_OUTPUT_ORDER:
                    if column != 'explanation':
                        reformatted_column_name = reformat_column_name(column)
                        value = apod.loc[0][column] # TODO
                        new_line = f'{reformatted_column_name}: {value}'
                        text_list.append(new_line)

                match apod.loc[0]['media_type']:
                    case 'image':
                        image_message = date_to_image_message(date)
                        messages.append(image_message)
                    case 'video':
                        # videos cannot normally be directly downloaded from YouTube
                        # but LINE automatically embeds YouTube videos by URL in text messages
                        video_url = apod.loc[0]['URL']
                        text_list.append(video_url)

            if user_input in [planet_name.lower() for planet_name in select_from_bigquery.query_planet_names()]:
                planet = select_from_bigquery.query_planet(user_input)
                df_text = df_to_text(planet)
                text_list.append(df_text)
            elif user_input in [constellation_name.lower() for constellation_name in select_from_bigquery.query_constellation_names()]:
                constellation = select_from_bigquery.query_constellation(user_input)
                df_text = df_to_text(constellation)
                text_list.append(df_text)
            # TODO: satellites
            # elif user_input in [satellite_name.lower() for satellite_name in select_from_bigquery.query_satellite_names()]:
            #     satellite = select_from_bigquery.query_satellite(user_input)
            #     df_text = df_to_text(satellite)
            #     text_list.append(df_text)
            elif user_input in [comet_name.lower() for comet_name in select_from_bigquery.query_comet_names()]:
                comet = select_from_bigquery.query_comet(user_input)
                df_text = df_to_text(comet)
                text_list.append(df_text)
            elif user_input in [shower_name.lower() for shower_name in select_from_bigquery.query_shower_names()]:
                shower = select_from_bigquery.query_shower(user_input)
                df_text = df_to_text(shower)
                text_list.append(df_text)
            elif user_input == 'sun':
                sun = select_from_bigquery.query_sun()
                df_text = df_to_text(sun)
                text_list.append(df_text)
    else:
        date = check_date.check_date(user_input)

        if not date:
            text_list.append(INVALID_DATE)
            text_list.append(DATE_USAGE)
        elif not check_date.is_in_range(date):
            text_list.append(f'{check_date.OLDEST} {DATE_OUT_OF_RANGE} {check_date.OLDEST}')
        else:
            # date is valid and in range
            apod = select_from_bigquery.query_apod(date)

            if apod.empty:
                if date == check_date.today():
                    text_list.append(NO_DATA_TODAY)
                else:
                    # some dates have no data
                    text_list.append(f'{date} {NO_DATA_AT_DATE} {date}')
            else:
                # data found
                for column in APOD_COLUMN_NAMES_OUTPUT_ORDER:
                    reformatted_column_name = reformat_column_name(column)
                    value = apod.loc[0][column]
                    new_line = f'{reformatted_column_name}: {value}'
                    text_list.append(new_line)

                match apod.loc[0]['media_type']:
                    case 'image':
                        image_message = date_to_image_message(date)
                        messages.append(image_message)
                    case 'video':
                        # videos cannot normally be directly downloaded from YouTube
                        # but LINE automatically embeds YouTube videos by URL in text messages
                        video_url = apod.loc[0]['URL']
                        text_list.append(video_url)

    text = '\n'.join(text_list)
    text_message = text_to_text_message(text, labels)
    messages.append(text_message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages,
            )
        )

def text_to_text_message(text, labels=None):
    if labels:
        text_message = TextMessage(
            text=text,
            # construct buttons
            quick_reply=QuickReply(
                items=[
                    QuickReplyItem(
                        action=MessageAction(
                            label=label,
                            text=label,
                        )
                    )
                    for label in labels
                ]
            )
        )
    else:
        text_message = TextMessage(text=text)

    return text_message

def reformat_column_name(column):
    return (' '.join(column.split('_'))
        .lower()
        .capitalize()
    )

def df_to_text(df, output_order=None):
    text_list = []

    if not output_order:
        output_order = df.columns

    for column in output_order:
        reformatted_column_name = reformat_column_name(column)
        value = df.loc[0][column]
        if column in ['Start_date', 'End_date']:
            # show only `mm-dd` from constellation date period
            value = value.strftime('%m-%d')
        new_line = f'{reformatted_column_name}: {value}'
        text_list.append(new_line)

    text = '\n'.join(text_list)

    return text

def reformat_describe_df(df):
    index = df.index
    columns = df.columns

    index = dict(zip(index, [reformat_column_name(i) for i in index]))
    columns = dict(zip(columns, [reformat_column_name(c) for c in columns]))

    df = df.rename(
        index=index,
        columns=columns,
    )

    df_text = df.to_string()

    return df_text

def date_to_image_message(date):
    # images from GCS database are named by `yyyy-mm-dd` date format
    bucket_name = 'tir102_apod'
    blob_name = f'{date}.jpg'
    credentials = extend_url.credentials

    image_url = extend_url.generate_signed_url(
        bucket_name,
        blob_name,
        credentials,
    )

    image_message = ImageMessage(
        original_content_url=image_url,
        preview_image_url=image_url,
    )

    return image_message

if __name__ == "__main__":
    app.run()
