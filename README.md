# mininet-json-topology

Python utility code for generating mininet topology based on json files.

## File format

The provided json file should have three main objects:
1. hosts
2. switches
3. links

each object is an array and each element in the array represents options of the related object.

#### host:
The mandatory field for this object is `name`.
Every other option in the host object such as `cpu` will be interpreted as additional options of the host and would add to `hostConfig`.

#### switch:
The mandatory fields for this object are `name` and `protocols`.
Like a host, every other option in the switch object will be interpreted as additonal options of the switch and would add to `switchConfig`.

#### link:
The mandatory fields for this object are `e1` and `e2`.
Like previous objects, every other option like `delay` or `bw` will be interpreted as additional options of the link and would add to `linkConfig`.

### sample file:
```json
{
    "hosts":[
       {
          "name":"h1",
          "cpu":0.5
       }
    ],
    "switches":[
       {
          "name":"s1",
          "protocols":"OpenFlow10",
          "dpid":"1"
       },
       {
         "name":"s2",
         "protocols":"OpenFlow10",
         "dpid":"2"
      }
    ],
    "links":[
       {
          "e1":"h1",
          "e2":"s1",
          "bw":10,
          "delay":"100ms"
       }
    ]
 }
```

## Tests
To run unit tests please follow the below instructions:

1. `git clone https://github.com/ali-a-a/mininet-json-topology.git`
2. `cd mininet-json-topology`
3. `python3 test_topo.py`

Note that you should install the `mininet` package first.

## Usage
To add this utility class to your project, you should import the `FVTopo` class first.

```python
from topo import FVTopo
```
then you can initialize `FVTopo` with your json file path.

```python
topo = FVTopo('your-json-file-path')
```

And use this object in your `Mininet` construction.

```python
net = Mininet(
        topo=topo,
        # other fields
      )
```