"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""



from typing import Any, Callable, Dict, Optional, Tuple, Union, TYPE_CHECKING
from dataclasses import dataclass, fields

from mkdocs.config import config_options as C


from ...messages import Lang
from ..maestro_tools import CopyableConfig

if TYPE_CHECKING:
    from pyodide_mkdocs_theme.pyodide_macros.plugin.pyodide_macros_plugin import PyodideMacrosPlugin


VAR_ARGS = -1



@dataclass
class ArgConfigDumpable:
    """
    Define a macro argument, that can be dumped as mkdocs C.OptionItem for a plugin Config.
    """

    name: str
    """ Argument name """

    py_type: Any
    """ Type of the actual value, used at runtime in python (see BaseMaestro extractors). """

    # --- kwargs only:

    in_config: bool = True
    """
    If False, this argument will not be added to the Config class/objects.
    (useful for thing that are implemented or were, but shouldn't be visible on user's side)
    """

    conf_type: Optional[Any] = None
    """
    ConfigOption related type. Created automatically from py_type if None, unless default
    is not None.
    """

    default: Optional[Any] = None
    """ Default value for the conf_type. Ignored if None (use is_optional for this). """

    is_optional: bool = False
    """ If True, add a C.Optional wrapper around the conf_type """

    index: Optional[int] = None
    """
    Index of the argument in the *args tuple, if it's positional.
    If index is -1, means the argument itself is a varargs.
    """

    extractor_prop: str = ''
    """ MaestroBase property name (ConfigExtractor) """


    @property
    def is_positional(self):
        return self.index is not None


    def __post_init__(self):

        if self.in_config:

            if self.conf_type is None:
                # Reminder: "default=None" is equivalent to "no default at all"
                self.conf_type = C.Type(self.py_type, default=self.default)

            if self.is_optional and self.default is None:
                self.conf_type = C.Optional(self.conf_type)


    def copy_with(self, **kw):
        args = {
            field.name: getattr(self, field.name) for field in fields( type(self) )
        }
        args.update(kw)
        return self.__class__(**args)


    def to_config(self):
        return self.conf_type



    def get_value(self, env:'PyodideMacrosPlugin'):
        return getattr(env, self.extractor_prop)


    def as_config_extractor_code(self, path:Tuple[str]):
        prop     = self.extractor_prop
        py_type  = self.py_type.__name__
        location = '.'.join(path[:-1])
        return f"\n    { prop }: { py_type } = ConfigExtractor('{ location }', prop='{self.name}')"








@dataclass
class ArgDeprecationAutoTransfert(ArgConfigDumpable):
    """
    Some macros args could replace a previously global setting in the mkdocs configuration.
    If registered as such, any value registered in the deprecated config field can be
    automatically extracted and transferred "here".
    """

    deprecated_source: Optional[Union[Tuple[str], str]] = None
    """
    Path attributes chaining of a deprecated config option: if this option is not None at
    runtime, the current option should be overridden with the one from the old option.

    NOTE: given as string at declaration time, then converted automatically to tuple.
    """

    transfer_processor: Optional[Callable[[Any],Any]] = None
    """
    Potential conversion function, used when automatically transferring the value from a
    deprecated option to it's new location (note: unused so far...)
    """

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.deprecated_source,str):
            self.deprecated_source = tuple(self.deprecated_source.split('.'))

    def process_value_from_old_location(self, value):
        return value if not self.transfer_processor else self.transfer_processor(value)









@dataclass
class ArgToDocs(ArgConfigDumpable):
    """
    Represent an argument of a macro and it's associated behaviors/config.
    """

    docs: str = ""
    """ Text to use when building the "summary" args tables in the docs """

    docs_default_as_type: bool = True
    """ If True, use the default value instead of the type in the as_docs_table output. """

    in_docs: bool = True
    """
    If False, this argument will not be present in the docs (tables of arguments, signatures).
    """

    docs_type: str = ""
    """ String replacement for the types in the docs """

    ide_link: bool=True
    """
    If True, when generating `as_table_row`, an md link will be added at the end, pointing
    toward the equivalent argument in the IDE-details page.
    """

    @property
    def doc_name_type_min_length(self):
        return 1 + len(self.name) + len(self.get_docs_type())



    def get_type_str(self):
        if self.docs_default_as_type and self.default is not None:
            return repr(self.default)
        return self.py_type.__name__

    def get_docs_type(self):
        return self.docs_type or self.py_type.__name__


    def signature(self, size:int=None):
        length   = self.doc_name_type_min_length
        n_spaces = length if size is None else size - length + 1
        return f"\n    { self.name}:{ ' '*n_spaces }{ self.get_docs_type() } = {self.default!r},"


    def as_table_row(self, for_resume=False):
        """
        Generate a md table row for this specific argument.
        @for_resume conditions what is used for arg name, type and value:

            for_resume | False   | True
            col1       | type    | nom argument
            col2       | default | type (or default, depending on docs_default_as_type)
            col3       | docs    | docs + ide_link if needed
        """

        if for_resume:
            a,b,doc = self.name, self.get_type_str(), self.docs
            if self.ide_link:
                doc += f"<br>_([plus d'informations](--IDE-{ self.name }))_"
        else:
            a,b,doc = f"#!py { self.get_docs_type() }", repr(self.default), self.docs

        return f"| `{ a }` | `#!py { b }` | { doc } |"






@dataclass
class ArgConfig(
    ArgToDocs,
    ArgDeprecationAutoTransfert,
    ArgConfigDumpable,
):
    pass












class MacroConfigDumpable:
    """
    Class making the link between:
        - The actual python implementation
        - The docs content (avoiding out of synch docs)
        - The Config used for the .meta.pmt.yml features. Note that optional stuff "there" is
          different from an optionality (or it's absence) in the running macro/python layer.

    Those instances represent the config "starting point", so all defaults are applied here,
    for the Config implementation.
    When extracting meta files or meta headers, the CopyableConfig instances will receive dicts
    from the yaml content, and those will be merged in the current config. This means the dict
    itself can contain only partial configs, it's not a problem.
    The corollary of this, is that _only_ values that could be None at runtime as an actual/useful
    value should be declared as `C.Optional`.
    """

    def __init__(self, name, *args:ArgConfig, in_config=True,  in_docs=True):

        self.in_config: bool = in_config
        self.in_docs:   bool = in_docs
        self.name:      str = name
        self.args:      Dict[str,ArgConfig] = {arg.name: arg for arg in args}

        if len(self.args) != len(args):
            raise ValueError(name+": duplicate arguments names.\n"+str(args))

        positionals = tuple(arg for arg in args if isinstance(arg,ArgConfigDumpable) and arg.is_positional)
        if args[:len(positionals)] != positionals:
            names = ', '.join(arg.name for arg in positionals)
            raise ValueError(
                f"{self.name}: the positional arguments should come first ({names})"
            )
        self.i_kwarg = len(positionals) and not positionals[-1].name.startswith('*')


    def __getattr__(self, prop):
        if prop not in self.args:
            raise AttributeError(prop)
        return self.args[prop]


    def get_sub_config_if_exist(self, name) -> Union[None, 'MacroConfig']:
        if name=='IDEv':
            name = 'IDE'
        return getattr(self, name, None)


    def args_with_tree_path_as_gen(self):
        """
        Build all the ArgConfig instances with their path attribute in the plugin config.
        """

        def dfs(obj: Union[MacroConfig,ArgConfigDumpable] ):
            path.append(obj.name)
            if isinstance(obj, ArgConfigDumpable):
                yield obj, tuple(path)
            else:
                for child in obj.args.values():
                    yield from dfs(child)
            path.pop()

        path = []
        return dfs(self)


    @classmethod
    def build_config_and_accessors(cls, *args):
        config = cls(*args)
        for arg,path in config.args_with_tree_path_as_gen():
            if arg.index == VAR_ARGS:
                continue
            arg.extractor_prop = '_'.join(path)
        return config


    def to_config(self):
        """
        Convert recursively to the equivalent CopyableConfig object.
        """
        class_name = ''.join(map(str.title, self.name.split('_'))) + 'Config'
        extends = (CopyableConfig,)
        body = {
            name: arg.to_config()
                for name,arg in self.args.items()
                if arg.in_config
        }
        kls = type(class_name, extends, body)
        return C.SubConfig(kls)







class MacroConfigToDocs(MacroConfigDumpable):

    def as_docs_table(self):
        """
        Converts all arguments to a 3 columns table (data rows only!):  name + type + help.
        No indentation logic is added here.
        """
        return '\n'.join(
            arg.as_table_row(True) for arg in self.args.values() if arg.in_docs
        )

    def signature_for_docs(self):
        """
        Converts the MacroConfig to a python signature for the docs, ignoring arguments that
        are not "in_docs".
        """
        args = [arg for arg in self.args.values() if arg.in_docs]
        size = max( arg.doc_name_type_min_length for arg in args )
        lst  = [ arg.signature(size) for arg in args ]
        if self.i_kwarg:
            lst.insert(self.i_kwarg, "\n    *,")

        return f"""
```python
{ '{{' } { self.name }({ ''.join(lst) }
) { '}}' }
```
"""






class MacroConfig(
    MacroConfigToDocs,
    MacroConfigDumpable,
): pass
