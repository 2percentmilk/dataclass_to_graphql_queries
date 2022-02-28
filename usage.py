from dataclass import *
from query_builder import SimpleBuilder, AttrVal, MOD
from enums import RequestType


# AttrVal.attr need to be unique
S = SimpleBuilder(data_returns=
[
    MosaicsQueryResult,
    FilesQueryResult,
    ImagesQueryResult,
    FeatureSetsQueryResult
])
S.add_cls_value(Survey, AttrVal('sentera_id', 'senteraId'))
S.add_attr_value(Survey, AttrVal(val='sentera_id', attr='mosaicSenteraId', col='mosaics'))
S.add_attr_value(Survey, AttrVal(val='pagination', attr=S.define_pagination(1, 10), col='mosaics'))

query = S.r_fields(
    dc=Survey,
    mod=MOD(
        type=RequestType.QUERY,
        name='Surveys',
        variables=S.state,
        exclude_type=[User, Pagination],
        exclude_name=['pagination', 'page', 'page_size'],
    )
)
S.print_query()
S.print_query_readable()
