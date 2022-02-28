# dataclass_to_graphql_queries
Takes a Hierarchy of Dataclasses and creates the proper graphql query

Creating the Class
data_returns = special return type that isn't used on create
Example Usage:
```python
# AttrVal.attr need to be unique
S = SimpleBuilder(data_returns=
[
    MosaicsQueryResult,
    FilesQueryResult,
    ImagesQueryResult,
    FeatureSetsQueryResult
])
```

Adding Graphql Variables:
You can add two types of variables, variables on the class name it self or on one of its attributes
```python
class ExampleDataclass:
  example_str: str
  example_int: int
```
creating a variable against the dataclass itself:
```python
# use the SimpleBuilder.add_cls_value method
S.add_cls_value(ExampleDataClass, AttrVal('id', 'Id'))
```
will end up creating
```text
query ExampleDataclass { ExampleDataClass(id: $Id) { ...
```

creating a variable against a dataclass attribute:
```python
# use the SimpleBuilder.add_attr_value method
S.add_attr_value(example_str, AttrVal('string', 'String'))
```
will end up creating
```text
# Appends on to the previous variable
query ExampleDataclass { ExampleDataClass(id: $Id, string: $String) { ...
```


Adding to the real class
```python
S.add_cls_value(Survey, AttrVal('sentera_id', 'senteraId'))
S.add_attr_value(Survey, AttrVal(val='sentera_id', attr='mosaicSenteraId', col='mosaics'))
S.add_attr_value(Survey, AttrVal(val='pagination', attr=S.define_pagination(1, 10), col='mosaics'))
```
query = S.r_fields(
    dc=Survey,
    mod=MOD(
        type=RequestType.QUERY, # Query or Mutation (currently only Query is available)
        name='Surveys', # Highest Level Class that query is derived from
        variables=S.state,
        exclude_type=[User, Pagination], # Lower level classes may want to be excluded, exclude here, This value will not be added to the query
        exclude_name=['pagination', 'page', 'page_size'],  # Individual attributes of classes may not want to be returned
    )
)
```python
S.print_query()
>>> query Surveys { survey(sentera_id: $senteraId) {   sentera_id   start_time   end_time   images   {     total_count     results     {       altitude       calculated_index       camera_make       camera_model       captured_at       color_applied       content_hash       created_at       download_filename       filename       gps_carrier_phase_status       gps_horizontal_accuracy       gps_vertical_accuracy       latitude       longitude       orientation       path       pitch       roll       sensor_type       sentera_id       size       updated_at       url       yaw     }   }   mosaics(sentera_id: $mosaicSenteraId, pagination: {page: 1 page_size: 10})   {     total_count     results     {       sentera_id       mosaic_type       quality       s3_uri       name       image_status       is_from_sentera_sensor       message       files       {         total_count         results         {           download_filename           file_type           filename           path           s3_uri           sentera_id           size           updated_at           url         }       }       captured_at       acres     }   }   feature_sets   {     total_count     results     {       type       sentera_id       name       error       files       {         total_count         results         {           download_filename           file_type           filename           path           s3_uri           sentera_id           size           updated_at           url         }       }       status       created_at     }   }   files   {     total_count     results     {       download_filename       file_type       filename       path       s3_uri       sentera_id       size       updated_at       url     }   } }
```

```python
S.print_query_readable()
>>>query Surveys
{
survey(sentera_id: $senteraId)
{
  sentera_id
  start_time
  end_time
  images
  {
    total_count
    results
    {
      altitude
      calculated_index
      camera_make
      camera_model
      captured_at
      color_applied
      content_hash
      created_at
      download_filename
      filename
      gps_carrier_phase_status
      gps_horizontal_accuracy
      gps_vertical_accuracy
      latitude
      longitude
      orientation
      path
      pitch
      roll
      sensor_type
      sentera_id
      size
      updated_at
      url
      yaw
    }
  }
  mosaics(sentera_id: $mosaicSenteraId, pagination: {page: 1 page_size: 10})
  {
    total_count
    results
    {
      sentera_id
      mosaic_type
      quality
      s3_uri
      name
      image_status
      is_from_sentera_sensor
      message
      files
      {
        total_count
        results
        {
          download_filename
          file_type
          filename
          path
          s3_uri
          sentera_id
          size
          updated_at
          url
        }
      }
      captured_at
      acres
    }
  }
  feature_sets
  {
    total_count
    results
    {
      type
      sentera_id
      name
      error
      files
      {
        total_count
        results
        {
          download_filename
          file_type
          filename
          path
          s3_uri
          sentera_id
          size
          updated_at
          url
        }
      }
      status
      created_at
    }
  }
  files
  {
    total_count
    results
    {
      download_filename
      file_type
      filename
      path
      s3_uri
      sentera_id
      size
      updated_at
      url
    }
  }
}
```
