# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup
from json import dumps
from lektor.build_programs import BuildProgram
from lektor.context import get_ctx
from lektor.db import F
from lektor.pluginsystem import Plugin
from lektor.sourceobj import VirtualSourceObject
from lektor.utils import build_url


PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
else:
    text_type = str


def split_to_list(value):
    return [item.strip() for item in value.split(',') if item.strip()]


def json_url(alt):
    return '/static/js/tipuesearch_content_{}.json'.format(alt)


class TipueSource(VirtualSourceObject):

    def __init__(self, parent, plugin):
        VirtualSourceObject.__init__(self, parent)
        self.plugin = plugin

    @property
    def path(self):
        return build_url([self.parent.path, '@tipue', 'tipuesearch'])

    def __getattr__(self, item):
        try:
            return self.plugin.config_value('tipuesearch', item)
        except KeyError:
            raise AttributeError(item)


class TipueBuilderProgram(BuildProgram):

    def produce_artifacts(self):
        sources = []
        for page in self.get_all_children():
            sources.extend(page.iter_source_filenames())
        self.declare_artifact(
            json_url(self.source.alt),
            sources=sources
        )

    def get_children(self, page):
        results = []
        for model in split_to_list(self.source.models):
            children = page.children
            children.include_undiscoverable(True)
            children = children.filter(F._model == model)
            results.extend(children.all())
        return list(set(results))

    def get_all_children(self):
        pages = [self.source.parent]
        before = 0
        while before != len(pages):
            before = len(pages)
            pages_ = []
            for page in pages:
                pages_.append(page)
                pages_.extend(self.get_children(page))
            pages = set(pages_)

        return pages

    def join_fields(self, page, fields):
        result = text_type()

        for field in split_to_list(fields):
            try:
                value = page[field]
                if type(value) == text_type:
                    result += ' ' + value
                elif hasattr(value, 'html'):
                    soup = BeautifulSoup(value.html, "html.parser")
                    result += ' ' + soup.text
                elif hasattr(value, 'source'):
                    result += ' ' + text_type(value.source)
            except KeyError:
                pass

        return ' '.join(result.split())

    def build_artifact(self, artifact):

        data = {'pages': []}
        for page in self.get_all_children():
            data['pages'].append({
                'title': self.join_fields(page, self.source.title),
                'text': self.join_fields(page, self.source.text),
                'tags': self.join_fields(page, self.source.tags),
                'url': page.url_path
            })

        get_ctx().record_dependency(artifact.artifact_name)

        with artifact.open('wb') as f:
            f.write(dumps(data).encode('utf-8'))


class TipuePlugin(Plugin):
    name = u'lektor-tipue'

    defaults = {
        'models': 'page',
        'title': 'title',
        'text': 'body',
    }

    def config_value(self, section, key):
        default_value = self.defaults.get(key, '')
        return self.get_config().get('%s.%s' % (section, key), default_value)

    def on_setup_env(self, **extra):

        def get_search_content():
            return json_url(get_ctx().source.alt)

        self.env.jinja_env.globals['tipue_search_content'] = get_search_content

        self.env.add_build_program(TipueSource, TipueBuilderProgram)

        @self.env.generator
        def generate_results(source):
            if source.path == '/':
                yield TipueSource(source, self)
