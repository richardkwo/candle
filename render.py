#-*-coding:utf-8-*-

import pystache as mustache

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
        <h2>{{title}}</h2>
        <h4>
            {{author}}
            {{#translator}} | {{translator}} 译{{/translator}}
        </h4>
        <br>
    ''',

    'headline': u'''
        <h3 class="{{classes}}">{{text}}</h3>
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
    '''
}


def render(template_name, data):
    return mustache.render(templates[template_name], data)


# generate html from json data
def render_html(data):
    # has_formula = data['hasFormula']
    posts = data['posts']
    body = '<mbp:pagebreak/>'.join(map(render_post, posts))
    return templates['head'] + body + templates['footer']


def render_title(post):
    return render('title', {
        'title': post['title'],
        'author': post['orig_author'],
        'translator': post['translator']
    })


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

    # image
    if content_type == 'illus':
        image = data['size']['medium']['src']
    else:
        image = ''

    return render(content_type, {
        'text': text,
        'image': image,
        'classes': ' '.join(classes)
    })


# a post is an article
def render_post(post):
    html = ''
    html += render_title(post)
    for content in post['contents']:
        html += render_content(content)
    return html


if __name__ == '__main__':
    with open('data/data.json') as fp:
        json_str = fp.read()
        import json
        data = json.loads(json_str)
        print render_html(data).encode('utf-8')
