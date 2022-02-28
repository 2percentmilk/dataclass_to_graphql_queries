import inspect
from dataclasses import dataclass, fields, field
from typing import Optional, Type, List, Any, Union
from enums import RequestType


type_map = {
    'str': 'String',
    'bool': 'Boolean',
    'Id': "ID",
    'datetime': 'ISO8601DateTime',
    'int': 'Int'
}


@dataclass
class AttrVal:
    val: Optional[str]
    attr: str
    col: Optional[Any] = None


@dataclass
class QueryVars:
    query: str
    var: dict


@dataclass
class MOD:
    type: RequestType
    name: str
    variables: Optional[dict] = None
    exclude_type: Optional[List[Type]] = None
    exclude_name: Optional[List[str]] = None
    modifiers: Optional[dict] = None


@dataclass
class SimpleBuilder:
    """
    Builds Query(Query) for a GraphQl Api
    """
    data_returns: list
    state: dict = field(default_factory=dict)
    vars: list = field(default_factory=list)
    query: list = field(default_factory=list)


    def add_cls_value(self, cls, q: Union[List[AttrVal], AttrVal]):

        self.add_variable(cls, q)

        if not self.state.get(cls.__name__):
            self.state[cls.__name__] = {'cls': {}, 'attr': {}}
        self.state[cls.__name__]['cls'] = {q.val: q.attr}

    def add_attr_value(self, cls, q: Union[List[AttrVal], AttrVal]):
        self.add_variable(cls, q)
        if not self.state.get(cls.__name__):
            self.state[cls.__name__] = {'cls': {}, 'attr': {}}

        if not self.state[cls.__name__]['attr'].get(q.col):
            self.state[cls.__name__]['attr'][q.col] = {}
        self.state[cls.__name__]['attr'][q.col][q.val] = q.attr

    def print_vars(self):
        return f"({', '.join(self.vars)})"

    def add_variable(self, cls, q: Union[List[AttrVal], AttrVal]):

        for attr, t in inspect.get_annotations(cls).items():
            if attr == q.val:
                self.vars.append(f'{q.attr}: {type_map.get(t.__name__)}')

    def define_pagination(self, page: int, page_size: int) -> str:
        return f'page: {page} page_size: {page_size}'

    def variables_on_cls(self, vars, dc_name):
        if dc_name not in vars:
            pass
        else:
            var_string = []
            if cls_vars := vars.get(dc_name, {}).get('cls'):
                for k, v in cls_vars.items():
                    var_string.append(f'{k}: ${v}')

                return f"{dc_name.lower()}({', '.join(var_string)})"

    def variables_on_cls_val(self, vars, dc_name, field, level):
        if dc_name not in vars:
            pass
        else:
            var_string = []
            if cls_vars := vars.get(dc_name)['attr']:
                for k, v in cls_vars.items():
                    if k == field.name:
                        for i, j in v.items():
                            if i not in ['pagination', 'order_by', 'order_by_direction']:
                                var_string.append(f'{i}: ${j}')
                            elif i == 'pagination':
                                var_string.append(f'{i}: {{{j}}}')
                            elif i in ['order_by', 'order_by']:
                                var_string.append(f'{i}: {j}')
                        return f'''{" " * level}{field.name.lower()}({', '.join(var_string)})'''

    def pprint(self, field: field, level: int, overwrite: str):
        if overwrite:
            return overwrite
        else:
            return f'{" " * level}{field.name.lower()}'

    def exclude(self, mods: MOD, dc: dataclass, field, level: int):
        _type = field.type
        if isinstance(field.type, list):
            _type = field.type[0]
        overwrite_value = self.variables_on_cls_val(mods.variables, dc.__name__, field, level)
        if not mods.exclude_type and not mods.exclude_type:
            self.query.append(self.pprint(field, level, overwrite_value))
            return True
        elif any([_type == _t for _t in mods.exclude_type]):
            return False
        elif field.name in mods.exclude_name:
            return False
        else:
            self.query.append(self.pprint(field, level, overwrite_value))
            return True

    def r_fields(self, dc: dataclass, level: Optional[int] = 2, mod: Optional[MOD] = None, count: int = 0):

        if count == 0:
            self.query.append(f'{mod.type:s} {mod.name:s}')
            self.query.append(f'{" " * (level - 2)}{{')

        self.query.append(self.variables_on_cls(mod.variables, dc.__name__))

        self.query.append(f'{" " * (level - 2)}{{')
        for field in fields(dc):
            if isinstance(field.type, list):
                if self.exclude(mod, dc, field, level):
                    self.r_fields(field.type[0], level=level + 2, mod=mod, count=count + 1)
            elif any([field.type == _t for _t in self.data_returns]):
                if self.exclude(mod, dc, field, level):
                    self.r_fields(field.type, level=level + 2, mod=mod, count=count + 1)
            elif isinstance(field.type, dict):
                pass  # Unable to convert dict to graphql schema
            else:
                self.exclude(mod, dc, field, level)
        self.query.append(f'{" " * (level - 2)}}}')

    def print_query(self):
        print(' '.join([l for l in self.query if l]))

    def print_query_readable(self):
        for l in self.query:
            if l:
                print(l)
