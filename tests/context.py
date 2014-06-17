from spec import Spec, skip, eq_
from mock import patch

from invoke.context import Context


class Context_(Spec):
    class init:
        "__init__"
        def takes_optional_run_and_config_args(self):
            # Meh-tastic doesn't-barf tests. MEH.
            Context()
            Context(run={'foo': 'bar'})
            Context(config={'foo': 'bar'})

    class run_:
        def _honors(self, kwarg, value):
            with patch('invoke.context.run') as run:
                Context(run={kwarg: value}).run('x')
                run.assert_called_with('x', **{kwarg: value, 'expand':{}})

        def warn(self):
            self._honors('warn', True)

        def hide(self):
            self._honors('hide', 'both')

        def pty(self):
            self._honors('pty', True)

        def echo(self):
            self._honors('echo', True)

        def ctx_expansion(self):
            ctx = Context(config={"foo":"bar"})
            res = ctx.run("echo {foo}")
            eq_(res.stdout.strip(), "bar")

        def ctx_expansion_and_vars(self):
            ctx = Context(config={"foo":"bar"})
            res = ctx.run("echo {foo} {something}", expand={"something":"baz"})
            eq_(res.stdout.strip(), "bar baz")

        def ctx_expansion_override(self):
            ctx = Context(config={"foo":"bar"})
            res = ctx.run("echo {foo}", expand={"foo":"baz"})
            eq_(res.stdout.strip(), "baz")

    class clone:
        def returns_copy_of_self(self):
            skip()

        def contents_of_dicts_are_distinct(self):
            skip()

    class configuration:
        "Dict-like for config"
        def setup(self):
            self.c = Context(config={'foo': 'bar'})

        def getitem(self):
            "___getitem__"
            eq_(self.c['foo'], 'bar')

        def get(self):
            eq_(self.c.get('foo'), 'bar')
            eq_(self.c.get('biz', 'baz'), 'baz')

        def keys(self):
            skip()

        def update(self):
            self.c.update({'newkey': 'newval'})
            eq_(self.c['newkey'], 'newval')
