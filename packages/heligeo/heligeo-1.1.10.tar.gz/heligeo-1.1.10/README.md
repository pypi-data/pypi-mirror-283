# Project Description

## Quickstart

### About HELIWARE

Heliware is a Web-GL Powered Geo-Spatial Analytics Platform for developer ,analytics & data Scientist that provides GIS, Web Mapping, and spatial data science tools which help companies to get InSite in just few click using AI, Data Science & Advance Geo-Processing

### Contact

For any query please contact [rajan@heliware.co.in](rajan@heliware.co.in)

### Access Free Api-Key

Get `free` `Api-key` by sign-up on Heliware [Visit Website](https://heliware.co.in/)

## Description About heligeo module

heligeo module provides you high level `Geoprocessing`,`Routing`,`Isochrone` and `Visualization` services.

___
## Routing and Isochrone
* `routes`
* `isochrone`
___
## Geoprocessing
* `polygon_union`
* `polygon_intersection`
* `alias_multistring`
* `point_buffer`
* `line_buffer`
* `point_within_polygon`
* `crop_geometry_data`
* `Polygon_Grid_Creation`
* `Find_Polygon_Center_Point`
* `Find_Polygon_linestring_inside_a_polygon_or_not`
* `crop_polygon_from_linestring`
* `distance_between_point`
* `boundingbox_geojson_geometry`
* `area_of_multipolygon`
* `linear_nearest_neighour`
* `point_within_polygon_based_on_polygon_properties`
* `line_arc_from_point`
* `nearest_point_along_line`
___
## File conversion
* `shp_to_geojson`
* `kml_to_geojson`
* `geojson_to_kml`
* `obj_to_geojson`
* `geo_to_dxf`
___
## Visualization without filteration
* `hex_map_from_geojson`
* `hex_map_from_csv`
* `scatter_map_from_geojson`
* `scatter_map_from_csv`
* `line_map_from_geojson`
* `fill_geo_map_from_geojson`
* `density_map_from_geojson`
* `density_map_from_csv`

## Visualization with filteration
* `visualization_from_geojson`
* `visualization_from_csv`
___
### Requirements
`heligeo-py` is tested over `Python>=3.0`
### Installation

To install from PyPI, simply use pip:  `pip install heligeo`

### How to use
Most of the cases heligeo module accept `Polygon`,`Point`,`Lisestring` data that format must be geojson.

### Usage
#### Basic Example Of Routing Service
By default heligeo support four type of transport mode
* `drive`
* `walk`
* `bike`
* `cycling`

### Output format
Output always `Geojson response`

### Isochrone Service
![image](https://pbs.twimg.com/media/DC5VxnxUMAAyZ-_.jpg)

```

from heligeo import heliRouteService
apikey = ''
longtitude = [88.3639]
latitude = [22.5726]
transport_mode = "drive" 
isochrone_data = heliRouteService.isochrone(apikey,latitude,longtitude,transport_mode)

```


### Routing Service
![image](https://www.propertyxpo.com/blog/wp-content/uploads/2019/09/Golf-Course-Extension-Road.jpg)

```
apikey = ''
transport_mode = "drive" 
direction_coordinates = [[88.3639,22.5726],[72.8777,19.0760]] ### user can use multiple points
route_data = heliRouteService.route(apikey,direction_coordinates,transport_mode)

```
### Basic Example Of Geoprocessing Service

* `heliGeoprocessingService.Union()`,`heliGeoprocessingService.Intersection()` function accept multiple polygon data inside a list.
* In this example we shown only 2 polygon data
### Polygon Union Example
```
from heligeo import heliGeoprocessingService
apikey = ''
polygon1 = {"type": "FeatureCollection","features":[{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0][77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [74029103817493, 28.36918941103731, 0.0]]]
  }}]}
polygon2 = {"type": "FeatureCollection","features":[{
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0], [77.40218550684746, 28.    3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [740486731638147, 28.36831967535351, 0.0]]]
      }}]}
polygon_list = [polygon1,polygon2]
union_data = heliGeoprocessingService.Union(apikey,polygon_list)


```
### Polygon Intersection Example

```
from heligeo import heliGeoprocessingService
apikey = ''
polygon1 = {"type": "FeatureCollection","features":[{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.4029103817493, 28.36918941103731, 0.0], [77.40184896262588, 28.3722403721131, 0.0][77.39922678901301, 28.37081966588294, 0.0], [77.40030856003351, 28.36816909494472, 0.0], [74029103817493, 28.36918941103731, 0.0]]]
  }}]}
polygon2 = {"type": "FeatureCollection","features":[{
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[77.40486731638147, 28.36831967535351, 0.0], [77.40416140548453, 28.37080235923333, 0], [77.40218550684746, 28.    3699755298779, 0.0], [77.40187364471585, 28.36769815943599, 0.0], [740486731638147, 28.36831967535351, 0.0]]]
      }}]}
polygon_list = [polygon1,polygon2]
intersection_data = heliGeoprocessingService.Intersection(apikey,polygon_list)

```

### PointBuffer Example
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/point-buffer.png?raw=true)
* point_list accept multiple points data
```
apikey = ''
point_list = [[88.3639,22.5726]] ### user can user multiple Point inside a list 
area = 100  ### how area user want to conver from this point by default its meter
point_buffer_polygon=heliGeoprocessingService.PointBuffer(apikey,point_list,area)


```

### CropPolygonusingLineString Example

* pp accept one polygon geojson data.
* ls accept only single LineString geojson data.
```
apikey = ''
pp = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[73.1191291041643,25.952161948461686],[73.1200261730937,25.95228141045213],[73.11998606278118,25.95249650900002],[73.1205147037379,25.952710699675958],[73.12058570338387,25.952860896463314],[73.12191931762833,25.953218219496392],[73.12201576873873,25.95292092059184],[73.12389940677676,25.953301946008786],[73.12434583885353,25.952337442082705],[73.12331303549425,25.952100144258512],[73.12258837500113,25.952099041426823],[73.12231284277169,25.952120347130396],[73.12199795253532,25.952887517224518],[73.12231350066179,25.95207889035184],[73.12043239077273,25.951540309982462],[73.11918985318253,25.951225622673974],[73.1191291041643,25.952161948461686]]]},"properties":{"prop0":"value0","prop1":{"this":"that"}}}]
 
ls = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"LineString","coordinates":[[73.1200261730937,25.95228141045213],[73.12043239077273,25.951540309982462],[73.12043239077273,25.951540309982462]]},"properties":{"prop0":"value0","prop1":{"this":"that"}}}]}
linestring_buffer_polygon=heliGeoprocessingService.crop_polygon_using_linestring(apikey,pp,ls)

```

### LineBuffer Example
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/line-buffer.png?raw=true)
* linestring_point_list accept multiple linestring.
```
apikey = ''
linestring_point_list = [[[88.3639,22.5726],[88.4143,22.5797]],[[88.2636,22.5958],[88.4789,22.7248]]] ### usecan  user multiple Point inside a list 
area = 100  ### how area user want to conver from this point by default its meter
linestring_buffer_polygon=heliGeoprocessingService.LineBuffer(apikey,linestring_point_list,area)

```
### PointWithinPoly Example

```
apikey = ''
point_geojson_object = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":                {"type":"Point","coordinates":[76.95513342,28.46301607]}}]}
polygon_list = [polygon1,polygon2]
point_inside_poly = heliGeoprocessingService.PointWithinPoly(apikey,point_geojson_object,polygon_list)


```

### Polygon and Linestring WithinPoly Example

```
apikey = ''
pp = {} #polygon geojson data
cp = [{},{},{}] # list of multiple geometry data(Polygon,LineString)
res=heliGeoprocessingService.check_polygon_ls_within_poly(apikey,pp,cp)


```

### LineBuffer Example
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/line-buffer.png?raw=true)
* linestring_point_list accept multiple linestring.
```
apikey = ''
linestring_point_list = [[[88.3639,22.5726],[88.4143,22.5797]],[[88.2636,22.5958],[88.4789,22.7248]]] ### usecan  user multiple Point inside a list 
area = 100  ### how area user want to conver from this point by default its meter
linestring_buffer_polygon=heliGeoprocessingService.LineBuffer(apikey,linestring_point_list,area)

```
### AliasLinestring Example
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/alias.png?raw=true)
```
apikey = ''
linestring_geojson_object = {"type": "FeatureCollection","features":[{"type": "Feature","geometry{"type":"LineString",
    "coordinates": [
      [88.3639,22.5726],[88.4143,22.5797]
    ]}}]}
gap = 100 #gap between multiple linestring(meter)
quantity = 100 ## how many line string u need 
alias_linestring_data = heliGeoprocessingService.AliasLinestring(apikey,linestring_geojson_object,gap,quantity)

```
### CropGeometryData
* `CropGeo` fuction accept a `Polygon GeoJson` data and `crop` other geometry data based on the `Polygon Size`.
* `CropGeo` accept `bb={}` contain `Polygon Geojson` data in which size u want to crop other geometry and `gd={[]}` contain all the getometry data which u want to `crop` `gd` `list` contain `Polygon`,`Linestring` and `point` data. Data must be `GeoJson format`.
* `CropGeo` supported only `Polygon`,`Linestring` and `point` data in `Geojson` format

```
apikey = ''
bb = {"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[76.76781345955712,30.524042786522788],[76.76658493660516,30.521411933136562],[76.76638374787312,30.520437335225605],[76.76812128413364,30.519991051100444],[76.76935817172217,30.5235212331106],[76.76781345955712,30.524042786522788]]]},"properties":{"PERIMETER":"1.166km","ENCLOSED_AREA":"0.0727sqkm"}}]}

gd = [{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"LineString","coordinates":[[76.76605941690902,30.521077391710715],[76.76854013805993,30.52031431912859],[76.76854013805993,30.52031431912859]]},"properties":{"LENGTH":"252.68m","BEARING":"1093333.9"}},{"type":"Feature","geometry":{"type":"LineString","coordinates":[[76.76629027392768,30.521865657532633],[76.76849050129871,30.521044858531493],[76.768764809871,30.520962819202154],[76.768764809871,30.520962819202154]]},"properties":{"LENGTH":"257.8m","BEARING":"112514.9"}},{"type":"Feature","geometry":{"type":"LineString","coordinates":[[76.76897591153649,30.52205540468611],[76.76691180534269,30.522839498623096],[76.76691197785424,30.522849031168167]]},"properties":{"LENGTH":"217.4m","BEARING":"2935656.9"}},{"type":"Feature","geometry":{"type":"LineString","coordinates":[[76.76727709618594,30.523549659635112],[76.76936689485044,30.52278710560935],[76.76936689485044,30.52278710560935]]},"properties":{"LENGTH":"217.66m","BEARING":"1125115.1"}}]}]

crop_data = heliGeoprocessingService.CropGeo(apikey,bb,gd)

```

### Polygon Grid Creation Example
* `PolyGrid` function accept `three` parameter `apikey`, `polygon_geo_json_data` and  `grid-size`.
* Based on the grid size `PolyGrid` function break down the `parent poly` into `small grids`.
* `PolyGrid` accept only `polygon` geojson data.

```
apikey = ''

polygon_geo_json_data = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[76.9720448,28.4914468],[76.9734664,28.490094],[76.9745038,28.4891069],[76.9777595,28.4865896],[76.9832406,28.4847617],[76.9877826,28.4817885],[76.9994099,28.4931639],[76.9958932,28.49571],[76.9958867,28.4995722],[76.993081,28.5026631],[76.9897562,28.5047863],[76.9854207,28.5071706],[76.979788,28.501845],[76.9762078,28.4984432],[76.9720448,28.4914468]]]}}]}

gridsize = 3 # in meter user change value as per user choice
poly_grid_data = heliGeoprocessingService.PolyGrid(apikey,polygon_geo_json_data,gridsize)
```
### Find Polygon Center Point Example
* `PolyCenter` accept `two` `parameter` `apikey` and `list_of_polygon_data=[polygeojson1,polygeojson1...n]`.

* `PolyCenter` function accept only `multiple polygon data` in `geojson` format.

* `list_of_polygon_data` its a list of multiple polygon data that must be geojson format
```
apikey = ''

list_of_polygon_data = [{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[76.9720448,28.4914468],[76.9734664,28.490094],[76.9745038,28.4891069],[76.9777595,28.4865896],[76.9832406,28.4847617],[76.9877826,28.4817885],[76.9994099,28.4931639],[76.9958932,28.49571],[76.9958867,28.4995722],[76.993081,28.5026631],[76.9897562,28.5047863],[76.9854207,28.5071706],[76.979788,28.501845],[76.9762078,28.4984432],[76.9720448,28.4914468]]]}}]},{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[76.9720448,28.4914468],[76.9734664,28.490094],[76.9745038,28.4891069],[76.9777595,28.4865896],[76.9832406,28.4847617],[76.9877826,28.4817885],[76.9994099,28.4931639],[76.9958932,28.49571],[76.9958867,28.4995722],[76.993081,28.5026631],[76.9897562,28.5047863],[76.9854207,28.5071706],[76.979788,28.501845],[76.9762078,28.4984432],[76.9720448,28.4914468]]]}}]},{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[76.9720448,28.4914468],[76.9734664,28.490094],[76.9745038,28.4891069],[76.9777595,28.4865896],[76.9832406,28.4847617],[76.9877826,28.4817885],[76.9994099,28.4931639],[76.9958932,28.49571],[76.9958867,28.4995722],[76.993081,28.5026631],[76.9897562,28.5047863],[76.9854207,28.5071706],[76.979788,28.501845],[76.9762078,28.4984432],[76.9720448,28.4914468]]]}}]}]

poly_center_point = heliGeoprocessingService.PolyCenter(apikey,list_of_polygon_data)

```
### Find distance between two Point Example
* `distance_between_point` accept two parameters `apikey` and `list of two point`
* `distance_between_point` support only `point` geometry
```
apikey = ''
point1 = [23,45]
point2 = [24,46]
points = [point1,point2]
distance_btw = heliGeoprocessingService.distance_between_point(apikey,points)
```

### Find bounding box geojson geometry Example
* `boundingbox_geojson` accept two parameters `apikey` and `geojson_data_of_geometry`
* `boundingbox_geojson` support all type of geometry Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon.
* Output will be bounding box `Polygon` data of geojson format
```
apikey = ''
geo_data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
          [[[77.03171253204346, 28.45861799583438], [77.0447587966919, 28.458316159251893], [77.05158233642578, 28.451109554935286], [77.04231262207031, 28.444883558900028], [77.02840805053711, 28.450505838034935], [77.03171253204346, 28.45861799583438]]],[[[77.03707695007324, 28.455335476723302], [77.03630447387695, 28.452166051216853], [77.04136848449707, 28.45163780439558], [77.04145431518555, 28.455033630768483], [77.03707695007324, 28.455335476723302]]]
        ]
      },
      "properties": {
        "service_provider": "HELIWARE",
        "timestamp": "20",
        "color": "black",
        "stroke": "red",
        "stroke-opacity": 0.4,
        "stroke-width": 5,
        "rev":200000,
        "pop":20
      }
    }
  ]}
bounding_box_data = heliGeoprocessingService.boundingbox_geojson(apikey,geo_data)
```

### Find area of multipolygons geometry Example
* `area_multipolygon` accept two parameters `apikey` and `geojson_data_of_geometry`
* `area_multipolygon` supported geometry Polygon, MultiPolygon.
* output will be dictionary contain total area and unit of area, example: {"Area": poly_area,"Unit":"Meter Square(Sq m)"}
```
apikey = ''
geo_data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
          [[[77.03171253204346, 28.45861799583438], [77.0447587966919, 28.458316159251893], [77.05158233642578, 28.451109554935286], [77.04231262207031, 28.444883558900028], [77.02840805053711, 28.450505838034935], [77.03171253204346, 28.45861799583438]]],[[[77.03707695007324, 28.455335476723302], [77.03630447387695, 28.452166051216853], [77.04136848449707, 28.45163780439558], [77.04145431518555, 28.455033630768483], [77.03707695007324, 28.455335476723302]]]
        ]
      },
      "properties": {
        "service_provider": "HELIWARE",
        "timestamp": "20",
        "color": "black",
        "stroke": "red",
        "stroke-opacity": 0.4,
        "stroke-width": 5,
        "rev":200000,
        "pop":20
      }
    }
  ]}
geo_area = heliGeoprocessingService.area_multipolygon(apikey,geo_data)
```

### Find linear nearest neighour point from given point Example
* `linear_nearest_neighour` accept three parameters `apikey`, `point_data` and `mark_point`
* `mark_point` is a point from which to find nearest point linearly from `point_data` 
* `point_data` in `linear_nearest_neighour` only support `point` geometry.
* output will be geojson format data of nearest `point` geometry with distance property
```
apikey = ''
point_data = {"type": "FeatureCollection",
  "features": [{"type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
            40.8193359375,
            25.64152637306577]},
     "properties": {
        "name": 10
      }},
    {"type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
            41.17968749994,
            23.644524198573688]},
     "properties": {
        "name": 20
      }},
    {"type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Point",
        "coordinates": [
            44.4130859375,
            25.760319754713887]},
     "properties": {
        "name": 30
      }}]}
mark_point = [42.6160,24.7518]

nearest_point = heliGeoprocessingService.linear_nearest_neighour(apikey,point_data,mark_point)
```

### Find points withen Polygon based on Polygon properties Example
* `point_within_polygon` accept three parameters `apikey`, `polygon_data` and `scale`
* Input is geojson data of polygon or multipolygon and property `scale` to render points based on properties
* `scale` is ['{property name}':{scale_value}], same property name should also in polygon property, where `scale_value` in `scale` and `polygon_data` must be integer.
* output will be in geojson format data of all point geometry within a polygon/multipolygon with properties
* `polygon_data` only support `Polygon` and `MultiPolygon` geometry.
```
apikey = ''
polygon_data = {"type": "FeatureCollection",
  "features": [{"type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [[77.03968405723572,
              28.448081502646776],
            [77.03970551490784,
              28.44760040224489],
            [77.04024195671082,
              28.447562668787487],
            [77.04019904136658,
              28.448090935966118],
            [77.03968405723572,
              28.448081502646776]
          ]]},
	  "properties": {
        "service_provider": "HELIWARE",
        "timestamp": "5",
        "color": "black",
        "stroke": "red",
        "stroke-opacity": 0.4,
        "stroke-width": 5,
        "rev":800000,
        "area":12
      }}]}
scale = {"area":5}
points_poly = heliGeoprocessingService.point_within_polygon(apikey,polygon_data,scale)
```
* output has 2 point in polygon, polygon has area 12 and scale provide area 5, points define numbers of parts in polygon with area 5 

### Create line arc from point Example
* `line_arc_from_point` accept three parameters `apikey`, `point_data` and `measure`
* `line_arc_from_point` return geometry data to Creates a circular arc of the given radius and center point between angle1 and angle2, angle work in positive clockwise.
* Input is geojson data of point and measurements of radius, angle1, angle2 in one list
* example of measurements will be measure=[{raduis},{angle1},{angle2}]
* output will be in geojson format of all linestring geometry data for creating line arc
* `point_data` only support `Point` geometry.
```
apikey = ''
point_data = {"type": "FeatureCollection",
  "features": [{"type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [[77.03968405723572,
              28.448081502646776],
            [77.03970551490784,
              28.44760040224489],
            [77.04024195671082,
              28.447562668787487],
            [77.04019904136658,
              28.448090935966118],
            [77.03968405723572,
              28.448081502646776]
          ]]},
	  "properties": {
        "service_provider": "HELIWARE",
        "timestamp": "5",
        "color": "black",
        "stroke": "red",
        "stroke-opacity": 0.4,
        "stroke-width": 5,
        "rev":800000,
        "area":12
      }}]}
measure = [0.1,10,20]
line_arc = heliGeoprocessingService.line_arc_from_point(apikey,point_data,measure)
```

### Find nearest point along line Example
* `nearest_point_along_line` accept three parameters `apikey`, `line_data` and `url`
* `nearest_point_along_line` return point geometry data of points which is nearest to line and also along to line, where line belongs to `line_data`
* `line_data` is geojson of `LineString` and url contain `Point` geometry data
* output will be in geojson format of all `point` geometry data which is nearest and along to `LineString`
```
apikey = ''
line_data = {"type": "FeatureCollection",
  "features": [{"type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
        [78.0029296875,
            25.799891182088334],
          [77.51953125,
            19.269665296502332]]
      }}]}
url = "https://raw.githubusercontent.com/mukulsharma97/Heliware_Visualization/main/assets/point_along.geojson"
n_point = heliGeoprocessingService.nearest_point_along_line(apikey,line_data,url)
```


## Basic Example of File conversion Service

### shp_to_geojson Example
* `shp_file` input shpe file name with complete path
* `geojson_file` output geojson file name with complete path
```
from heligeo import heliconverter
shp_file = ".../heligeo_converter/lines.shp"
geojson_file = ".../heligeo_converter/shptogeo.geojson"
heliconverter.shp_to_geojson(shp_file,geojson_file)
```

### kml_to_geojson Example
* `kmlf` input kml file name with complete path
* `geof` output geojson file path
```
kmlf = ".../heligeo_converter/kml.kml"
geof = ".../heligeo_converter/kmltogeo"
heliconverter.kml_to_geojson(kmlf,geof)
```

### geojson_to_kml Example
* `geof` input geojson file name with complete path
* `kmlf` output kml file name with complete path
```
kmlf = ".../heligeo_converter/geotokml.kml"
geof = ".../heligeo_converter/isochrone.geojson"
heliconverter.geojson_to_kml(geof,kmlf)
```

### obj_to_geojson Example
* `obj` input object file name with complete path
* `geof` output geojson file name with complete path
```
obj = ".../heligeo_converter/mesh.obj"
geof = ".../heligeo_converter/objtogeo.geojson"
heliconverter.obj_to_geojson(obj,geof)
```

### geo_to_dxf Example
* `geof` input geojson file name with complete path
* `dwgf` output dxf file name without extension and with complete path
```
geof = ".../heligeo_converter/multilinestring.geojson"
dwgf = ".../heligeo_converter/poly_line_point"
heliconverter.geo_to_dxf(geof,dwgf)
```

## Basic Example Of Visualization Service


### Hexagon Map
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/hexagon.png?raw=true)
* User Can Select Different type of `BaseMap` Like `basic`, `streets`,`outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* User can Create `hex_map` from `.geojon` and `.csv` file
* File Must be contain `geometry` data
* `hex_map_from_geojson` funtion accepty `.geojson` file with other parameter and `hex_map_from_csv` accept `.csv` file with other parameter.
* `hex_map_from_geojson` accept `apikey`,`file_path`,`hover_properties`,`basemap_style`,`hexagon_quantity`,`zoom_level`
* `hex_map_from_csv` accept `apikey`,`file_path`,`column name from csv file that contain latitude value`,`column name from csv file that contain longtitude value`,`hover_properties`,`basemap_style`,`hexagon_quantity`,`zoom_level`
* As of Now `heligeo` module able to visualize only `one propertie ` with their corrosponding `Lat`,`Long` value
* `Base_map=''`
* Use `res.show()` to visualize the data into web. 
* for `hex_map_from_geojson` user dont need to pass this two parameter  `column name that contain latitude value`,`column name that contain longtitude value` we create these two value as our own.
#### Example 
```
from heligeo import heliVisualizationService
apikey=''
file_path = '' 
latitude_value_col_name = ''
longtitude_value_col_name = ''
hover_properties = ''
base_map = ''
hexagan_quantity = 20  
zoom_level = 16
h = heliVisualizationService.hex_map_from_csv(apikey,file_path,latitude_value_col_name,longtitude_value_col_name,hover_properties,base_map,hexagan_quantity,zoom_level)
h.show()

h = heliVisualizationService.hex_map_from_geojson(apikey,file_path,hover_properties,base_map,hexagan_quantity,zoom_level)
h.show()

```


### Scatter Map
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/scatter.png?raw=true)
* User Can Select Different type of `BaseMap` Like `basic`, `streets`, `outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* User can Create `scatter_map` from `.geojson` and `.csv` file
* File Must be contain `geometry` data
* `scatter_map_from_geojson` funtion accept `.geojson` file with other parameter and `scatter_map_from_csv` accept `.csv` file with other parameter.
* `scatter_map_from_geojson` accept `apikey`,`file_path`,`hover_properties`,`basemap_style`,`zoom_level`
* `scatter_map_from_csv` accept `apikey`,`file_path`,`column name from csv file that contain latitude value`,`column name from csv file that contain longtitude value`,`hover_properties`,`basemap_style`,`zoom_level`
* As of Now `heligeo` `Visualization` module able to visualize only `one propertie ` with their corrosponding `Lat`,`Long` value

* Use `res.show()` to visualize the data into web. 
* for `scatter_map_from_geojson` user dont need to pass this two parameter  `column name that contain latitude value`,`column name that contain longtitude value` we create these two value as our own.

#### Example 
```
from heligeo import heliVisualizationService
apikey=''
file_path = '' 
latitude_value_col_name = ''
longtitude_value_col_name = ''
hover_properties = ''
base_map = ''  
zoom_level = 16
h = heliVisualizationService.scatter_map_from_csv(apikey,file_path,latitude_value_col_name,longtitude_value_col_name,hover_properties,base_map,zoom_level)
h.show()

h = heliVisualizationService.scatter_map_from_geojson(apikey,file_path,hover_properties,base_map,zoom_level)
h.show()


```





### Density Map
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/density.png?raw=true)
* User Can Select Different type of `BaseMap` Like `basic`, `streets`, `outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* User can Create `density_map` from `.geojson` and `.csv` file
* File Must be contain `geometry` data
* `density_map_from_geojson` funtion accept `.geojson` file with other parameter and `density_map_from_csv` accept `.csv` file with other parameter.
* `density_map_from_geojson` accept `apikey`,`file_path`,`hover_properties`,`basemap_style`,`zoom_level`
* density_map_from_csv` accept `apikey`,`file_path`,`column name from csv file that contain latitude value`,`column name from csv file that contain longtitude value`,`hover_properties`,`basemap_style`,`zoom_level`
* As of Now `heligeo` `Visualization` module able to visualize only `one propertie ` with their corrosponding `Lat`,`Long` value

* Use `res.show()` to visualize the data into web. 
* for `density_map_from_geojson` user dont need to pass this two parameter  `column name that contain latitude value`,`column name that contain longtitude value` we create these two value as our own.

#### Example 
```
from heligeo import heliVisualizationService
apikey=''
file_path = '' 
latitude_value_col_name = ''
longtitude_value_col_name = ''
hover_properties = ''
base_map = ''  
zoom_level = 16
h = heliVisualizationService.density_map_from_csv(apikey,file_path,latitude_value_col_name,longtitude_value_col_name,hover_properties,base_map,zoom_level)
h.show()

h = heliVisualizationService.density_map_from_geojson(apikey,file_path,hover_properties,base_map,zoom_level)
h.show()

```


### Line Map
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/linemap.png?raw=true)
* User Can Select Different type of `BaseMap` Like `basic`, `streets`, `outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* User can Create `line_map` from `.geojson`.
* `line_map_from_geojson` funtion accept `.geojson` file with other parameter.
* `density_map_from_geojson` accept `apikey`,`file_path`,`hover_properties`,`basemap_style`,`zoom_level`
* As of Now `heligeo` `Visualization` module able to visualize only `one propertie ` with their corrosponding `Lat`,`Long` value
* Use `res.show()` to visualize the data into web. 

#### Example 
```
from heligeo import heliVisualizationService
apikey=''
file_path = '' 
hover_properties = ''
base_map = ''  
zoom_level = 15
h = heliVisualizationService.line_map_from_geojson(apikey,file_path,hover_properties,base_map,zoom_level)
h.show()

```

### Fill Geometry With Color
![image](https://github.com/NandanPattanayak/heligeo/blob/main/images/color.png?raw=true)
* User Can Select Different type of `BaseMap` Like `open-street-map`, `carto-positron`, `carto-darkmatter`, `stamen-terrain`, `stamen-toner` or `stamen-watercolor`
* User can fill a `Geometry` with different color and `Visualize` on map.
* `fill_geo_map_from_geojson` funtion accept `.geojson` file with other parameter.
* `fill_geo_map_from_geojson` accept `apikey`,`file_path`,`color`,`basemap_style`,`zoom_level`
* As of Now `heligeo` `Visualization` module able to visualize only `one propertie ` with their corrosponding `Lat`,`Long` value
* Use `res.show()` to visualize the data into web. 

#### Example 
```
from heligeo import heliVisualizationService
apikey=''
file_path = '' 
color = ''
base_map = ''  
zoom_level = 15
h = heliVisualizationService.fill_geo_map_from_geojson(apikey,file_path,color,base_map,zoom_level)
h.show()

```
## Visualization with filteration
![image](https://github.com/mukulsharma97/Heliware_Visualization/blob/main/assets/front%20page.png?raw=true)
* As of now our module accept `10 features`,`filteration` functionality
* once you call the module its automatically create 
localserver localhost:8085
* Paste the local host address on browser
* Select a Map type

### visualization from  geojson
* User Can Select Different type of `BaseMap` Like `basic`, `streets`, `outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* User can filter the data in real time
* `visualization_from_geojson` function accept `file_path`,`hover_properties`,`BaseMap(optional)`

#### Example 
```
from heligeo import heliVisualizationWithFilteration
file_path = '' ## local csv file path
hover_properties = '' ## based on this property our module will create map
heliVisualizationWithFilteration.visualization_from_geojson(file_path,hover_properties)

```

### visualization from csv
* User Can Select Different type of `BaseMap` Like `basic`, `streets`, `outdoors`, `light`, `dark`, `satellite`, or `satellite-streets`
* once you call the module its automatically create 
localserver localhost:8085
* User can filter the data in real time
* `visualization_from_geojson` function accept `file_path`,`lat_column_name`,`long_column_name`,`hover_properties`,`BaseMap(optional)`

#### Example 
```
from heligeo import heliVisualizationWithFilteration
file_path = '' ## local csv file path
lat_column_name = ''
long_column_name = ''
hover_properties = '' ## based on this property map will create

heliVisualizationWithFilteration.visualization_from_csv(file_path,lat_column_name,long_column_name,hover_properties)

```




## License
Â© 2021 HELIWARE

This repository is licensed under the MIT license. See LICENSE for details.