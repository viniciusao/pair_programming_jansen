import json
import os
import uuid

from chalice import Chalice

from chalicelib import cursor, db


app = Chalice(app_name='pair_programming_jansen')


@app.route('/encurtar', methods=['POST'])
def encurtar():
    b = app.current_request.raw_body.decode()
    body = json.loads(b)
    uuid_ = str(uuid.uuid4()).split('-').pop()
    shorten_link = os.environ['LINK_SHORTENER'].format(uuid_)
    cursor.execute(
        f'''INSERT INTO {os.environ['TABLE_LINKS_SHORTENED']} (original, shortened) 
        VALUES ("{body['original']}", "{shorten_link}")'''
    )
    db.commit()
    return {**body, 'shortenado': True}


@app.route('/links')
def get_links():
    query_strings = app.current_request.query_params
    if not query_strings:
        links = cursor.execute(
            f'''SELECT * FROM {os.environ['TABLE_LINKS_SHORTENED']}'''
        ).fetchall()
        links_shortened = [{'shortened': v[2]} for v in links]
        return links_shortened

    shortened = query_strings.get('shortened')
    link_original = cursor.execute(
        f'''SELECT original FROM {os.environ['TABLE_LINKS_SHORTENED']} 
        WHERE shortened = "{shortened}"'''
    ).fetchone()[0]
    return {'link_original': link_original}
