#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import shutil
import mako.template
import mako.lookup

class Navi(list):
    def __init__(self, name, href=None, icon=None, children=[]):
        super(Navi, self).__init__(children)
        self.name = name
        self.href = href
        self.icon = icon

main_navigations = [
    Navi('TOP', href='/index.html', icon='icon-dashboard'),
    Navi(u'議員情報', href='/reports.html', icon='icon-list-alt'),
    Navi(u'ランク', href='/guidely.html', icon='icon-facetime-video'),
    Navi(u'ニュース', href='/guidely.html', icon='icon-facetime-video'),
    # Navi('Charts', href='/charts.html', icon='icon-bar-chart'),
    # Navi('Shortcodes', href='/shortcodes.html', icon='icon-code'),
    # Navi('Drops', icon='icon-long-arrow-down', children=[
    #     Navi('Icons', href="/icons.html"),
    #     Navi('FAQ', href='/faq.html'),
    #     Navi('Pricing Plans', href='/pricing.html'),
    #     Navi('Login', href='/login.html'),
    #     Navi('Signup', href='/signup.html'),
    #     Navi('Error', href='/error.html'),
    #     ]),
    ]


def mkdir_p(path):
    try:
        os.makedirs(path)
    except:
        pass

def main():
    regxes = list(map(
        lambda pattern: re.compile(pattern),
        ['.*\.html$',
         '.*\.htm$',
         '.*\.css$',
         ]))

    ignores = list(map(
        lambda pattern: re.compile(pattern),
        ['.*~$',
         ]))

    template_dir = os.path.abspath('templates')
    output_dir = os.path.abspath('_build')
    lookupper = mako.lookup.TemplateLookup(
        directories=[template_dir],
        input_encoding='utf-8',
        output_encoding='utf-8',
        encoding_errors='replace',
        )
    for root, dirs, files in os.walk(template_dir):
        for filename in files:
            template_file = os.path.abspath(os.path.join(root, filename))
            template_name = os.path.relpath(template_file, template_dir)
            output_file = os.path.join(output_dir, template_name)
            mkdir_p(os.path.dirname(output_file))
            if any(regx.search(filename) for regx in regxes):
                if not filename.startswith('_') and not any(regx.search(filename) for regx in ignores):
                    tmpl = lookupper.get_template(template_name)
                    with open(output_file, 'w+b') as fp:
                        contexts = {
                            'export_file': template_file,
                            'title': 'Baast - Backend As A Service for Tornado',
                            'search_placeholder': 'search',
                            'main_navigations': main_navigations,
                            'base_color': '#00ba8b',
                            }
                        buf = tmpl.render(**contexts)
                        fp.write(buf)
            else:
                shutil.copy(template_file, output_file)


if __name__ == '__main__':
    main()
