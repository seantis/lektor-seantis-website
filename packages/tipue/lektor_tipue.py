# -*- coding: utf-8 -*-
import sys
import posixpath

from json import dumps
from lektor.build_programs import BuildProgram
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


class TipueSource(VirtualSourceObject):

    def __init__(self, parent, section, plugin):
        VirtualSourceObject.__init__(self, parent)
        self.section = section
        self.plugin = plugin

    @property
    def path(self):
        return build_url([self.parent.path, '@tipue', self.section])

    @property
    def url_path(self):
        return self.plugin.config_value(self.section, 'target_path')

    def __getattr__(self, item):
        try:
            return self.plugin.config_value(self.section, item)
        except KeyError:
            raise AttributeError(item)


class TipueBuilderProgram(BuildProgram):

    def produce_artifacts(self):
        self.declare_artifact(
            posixpath.join(
                self.source.url_path, '{}.json'.format(self.source.section)
            ),
            sources=list(self.source.iter_source_filenames())
        )

    def get_children(self, page):
        results = []
        for model in split_to_list(self.source.models):
            children = page.children
            children.include_undiscoverable(True)
            children = children.filter(F._model == model)
            results.extend(children.all())
        return list(set(results))

    def join_fields(self, page, fields):
        result = text_type()

        for field in split_to_list(fields):
            try:
                value = page[field]
                if type(value) == text_type:
                    result += ' ' + value
                elif hasattr(value, 'source'):
                    result += ' ' + text_type(value.source)
            except KeyError:
                pass

        return result

    def build_artifact(self, artifact):
        pages = [self.source.parent]
        before = 0
        while before != len(pages):
            before = len(pages)
            pages_ = []
            for page in pages:
                pages_.append(page)
                pages_.extend(self.get_children(page))
            pages = set(pages_)

        data = {'pages': []}
        for page in pages:
            data['pages'].append({
                'title': self.join_fields(page, self.source.title),
                'text': self.join_fields(page, self.source.text),
                'tags': self.join_fields(page, self.source.tags),
                'url': page.url_path
            })

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
        self.env.add_build_program(TipueSource, TipueBuilderProgram)

        @self.env.generator
        def generate_results(source):
            for section in self.get_config().sections():
                if source.path == self.config_value(section, 'source_path'):
                    yield TipueSource(source, section, self)
