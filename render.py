#-*-coding:utf-8-*-

import logging
import envoy
import pystache as mustache

logger = logging.getLogger(__name__)

templates = {
    'head': u'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <style type="text/css">
                    body {
                    }
                    p {
                        text-indent: 2em;
                        line-height: 1.3em;
                    }
                    .p_indent {
                        text-indent: 2em;
                    }
                    .t_indent {
                        text-indent: 2em;
                    }
                    .p_align_left {
                        text-align: left;
                    }
                    .p_align_center,
                    .p_center {
                        text-align: center;
                    }
                    .p_align_right {
                        text-align: right;
                    }
                    .p_bold {
                        font-weight: bold;
                    }
                    .p_quote {
                        
                    }
                </style>
            </head>
            <body>
    ''',

    'footer': u'''
            </body>
        </html>
    ''',

    'title': u'''
        <a href="#{{toc_anchor}}"></a>
        <h2 id="{{toc_anchor}}">{{title}}</h2>
        <h4>
            {{author}}
            {{#translator}} | {{translator}} 译{{/translator}}
        </h4>
        <br>
    ''',

    'headline': u'''
        <a href="#{{toc_anchor}}"></a>
        <h3 id="{{toc_anchor}}" class="{{classes}}">{{text}}</h3>
    ''',

    'paragraph': u'''
        <p class="{{classes}}">{{text}}</p>
    ''',

    'illus': u'''
        <p class="p_align_center">
            <img class="{{classes}}" src="{{image}}" />
        </p>
    ''',

    'breaker': u'''
        <mbp:pagebreak/>
    ''',

    'toc.ncx': u'''
        <?xml version="1.0" encoding="UTF-8"?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">
            <head>
                <meta name="dtb:depth" content="4" />
                <meta name="dtb:totalPageCount" content="0" />
                <meta name="dtb:maxPageNumber" content="0" />
            </head>
            <docTitle><text>{{ title }}</text></docTitle>
            <docAuthor><text></text></docAuthor>
            <navMap>
                <navPoint class="book">
                    <navLabel><text>{{ title }}</text></navLabel>
                    <content src="content.html" />
                    {{#contents}}
                        <navPoint class="chapter" id="{{ anchor }}" playOrder="{{ anchor }}">
                            <navLabel><text>{{ title }}</text></navLabel>
                            <content src="content.html#{{ anchor }}" />
                        </navPoint>
                    {{/contents}}
                </navPoint>
            </navMap>
        </ncx>
    ''',

    'opf': u'''
        <?xml version="1.0" encoding="utf-8"?>
        <package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uid">
            <metadata>
                <dc-metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
                    <dc:title>{{ title }}</dc:title>
                    <dc:language>zh-CN</dc:language>
                    <dc:creator>wong2</dc:creator>
                    <dc:publisher>wong2</dc:publisher>
                    <dc:subject>{{ title }}</dc:subject>
                    <dc:date>2013-04-05T06:07:08</dc:date>
                    <dc:description></dc:description>
                </dc-metadata>
            </metadata>
            <manifest>
                <item id="content" media-type="application/xhtml+xml" href="content.html"></item>
                <item id="toc" media-type="application/x-dtbncx+xml" href="toc.ncx"></item>
            </manifest>
            <spine toc="toc">
                <itemref idref="content"/>
            </spine>
        </package>
    '''
}


def render(template_name, data):
    return mustache.render(templates[template_name], data)


table_of_contents = []
book_index = 0

def add_to_table_of_contens(title):
    if len(table_of_contents) <= book_index:
        table_of_contents.append([])
    anchor = 'toc_%s_%s' % (len(table_of_contents), len(table_of_contents[-1])+1)
    table_of_contents[-1].append({
        'title': title,
        'anchor': anchor
    })
    return anchor


# ------------

def generate_book(book_id, book_title, content_json_data):
    logger.info('going to render content.html')
    content_html = render_html(content_json_data)
    logger.info('content.html rendered')
    with open('data/%s/content.html' % book_id, 'w') as fp:
        fp.write(content_html.encode('utf-8'))
    toc_xml = render_toc(book_title)
    with open('data/%s/toc.ncx' % book_id, 'w') as fp:
        fp.write(toc_xml.encode('utf-8'))
    opf_xml = render_opf(book_title)
    with open('data/%s/book.opf' % book_id, 'w') as fp:
        fp.write(opf_xml.encode('utf-8'))
    logger.info('book files prepared for %s', book_id)

    # kindlegen
    logger.info('before run kindlegen for %s', book_id)
    r = envoy.run('kindlegen -o %s.mobi data/%s/book.opf' % (book_id, book_id))
    if r.status_code != 1:
        logging.error('generate book error: %s', r.std_out, exc_info=True)
        raise RuntimeError(r)
    logger.info('mobi file generated to data/%s/%s.mobi', book_id, book_id)
    return 'data/%s/%s.mobi' % (book_id, book_id)


def render_opf(book_title):
    return render('opf', {'title': book_title})


def render_toc(book_title):
    if len(table_of_contents) > 1:
        toc_s = [tocs[0] for tocs in table_of_contents]
    else:
        toc_s = table_of_contents[0]
    return render('toc.ncx', {
        'title': book_title,
        'contents': toc_s
    })


# generate html from json data
def render_html(data):
    body = '<mbp:pagebreak/>'.join(map(render_post, data['posts']))
    return templates['head'] + body + templates['footer']


# a post is an article
def render_post(post):
    html = ''
    html += render_title(post)
    html += ''.join(map(render_content, post['contents']))
    return html


def render_title(post):
    toc_anchor = add_to_table_of_contens(post['title'])
    global book_index
    book_index += 1
    return render('title', {
        'title': post['title'],
        'author': post['orig_author'],
        'translator': post['translator'],
        'toc_anchor': toc_anchor
    })


# 一个段落等
def render_content(content):
    classes = []
    content_type, data = content['type'], content['data']

    text_format = data.get('format')

    if text_format:
        for class_name in ['p_indent', 'p_center', 'p_quote', 'p_bold']:
            if text_format.get(class_name):
                classes.append(class_name)

        text_align = text_format.get('p_align')
        if text_align in ['left', 'right', 'center']:
            classes.append('p_align_' + text_align)

    text = data.get('text')

    render_data = {
        'text': text,
        'classes': ' '.join(classes)
    }

    # image
    if content_type == 'illus':
        render_data['image'] = data['size']['medium']['src']

    if content_type == 'headline':
        render_data['toc_anchor'] = add_to_table_of_contens(text)

    return render(content_type, render_data)


if __name__ == '__main__':
    with open('data/data.json') as fp:
        json_str = fp.read()
        import json
        data = json.loads(json_str)
        print render_html(data).encode('utf-8')
