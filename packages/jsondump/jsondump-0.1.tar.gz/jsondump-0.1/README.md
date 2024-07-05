# jsondump

Serialize a object including it's function into a JSON.


## Install

```
pip install jsondump
```

## Usage

```python
import jsondump
```

Serialize an object including it's function:


```python
obj = {
  'name': 'Bob',
  'say': ['Hello', 'World']
}

objS = jsondump.dumps(obj)
type(objS) is str
jsondump.loads(objS).name == 'Bob'
```

Serialize an object with a sub object:

```python
var objWithSubObj = {
  'obj': {
    'name': 'Jeff',
    'say': ['Hello', 'World']
  }
}

objWithSubObjS = jsondump.dumps(objWithSubObj);
type(objWithSubObjS) is str
jsondump.loads(objWithSubObjS).obj.name == 'Jeff'
```
