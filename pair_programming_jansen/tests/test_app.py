import json

from chalice.test import Client

from app import app
from chalicelib import cursor


def test_encurtar():
    with Client(app, stage_name='dev') as client:
        response = client.http.post(
            '/encurtar',
            body=json.dumps({'original': 'www.mock.com'})
        )
        link = cursor.execute('''SELECT * FROM links_shortened WHERE original = "www.mock.com"''').fetchone()
        assert link and response.json_body['shortenado']


def test_get_links():
    with Client(app, stage_name='dev') as client:
        response = client.http.get('/links')
        assert response.json_body


def test_get_link():
    with Client(app, stage_name='dev') as client:
        response = client.http.get('/links?shortened=https://www.sasi.com/890e729de217')
        assert response.json_body['link_original'] == 'www.mock.com'
