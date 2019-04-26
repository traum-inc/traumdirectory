import re
import os
import logging
log = logging.getLogger('template')

re_var = re.compile('\{(\w+)\}')
re_indent = re.compile('\t*')

def format_kwargs(kwargs):
    return ' '.join(
        f'{k}={v}' for k,v in kwargs.items())

class Template(object):

    def __init__(self, name):
        self.name = name
        self.dirpaths = []
        self.varnames = []

    def load(self, filepath):
        with open(filepath) as fp:
            text = fp.readlines()
        text = [l.rstrip() for l in text if l.strip()]

        last_indent = -1
        path_comps = []
        varnames = {}

        indent_type = None

        for line_idx, line in enumerate(text):
            # get indent & dirname
            line = line.rstrip()
            name = line.lstrip()

            indent = len(line) - len(name)
            indent_text = line[:indent]
            #print(f'INDENT: "{indent_text}"')
            assert re_indent.match(indent_text), f'Bad indent at line {1+line_idx}'
            # FIXME check just tabs

            change = indent - last_indent
            assert change <= 1

            if change <= 0:
                for i in range(1 - change):
                    path_comps.pop()

            path_comps.append(name)
            last_indent = indent

            dirpath = os.path.join(*path_comps)
            self.dirpaths.append(dirpath)

            for v in re_var.findall(name):
                varnames[v] = True

        self.varnames = list(varnames.keys())

    def exec(self, outdir, **kwargs):
        log.info(f'exec outdir={outdir} args={format_kwargs(kwargs)}')

        for v in self.varnames:
            if v not in kwargs:
                raise Exception(f'Missing argument: {v}')

        for dirpath in self.dirpaths:
            dirpath = dirpath.format(**kwargs)
            dirpath = os.path.join(outdir, dirpath)

            try:
                os.makedirs(dirpath, exist_ok=True)
                log.info(f'mkdir: {dirpath}')
            except Exception as e:
                log.error(e)


class TemplateManager(object):

    def __init__(self, template_dir):
        self.templates = {}
        self._load_templates(template_dir)

    def _load_templates(self, template_dir):
        for filename in os.listdir(template_dir):
            name, ext = os.path.splitext(filename)
            if ext == '.dir':
                tpl = Template(name)
                tpl.load(os.path.join(template_dir, filename))
                log.info(f'loaded template {name}')
                self.templates[name] = tpl
