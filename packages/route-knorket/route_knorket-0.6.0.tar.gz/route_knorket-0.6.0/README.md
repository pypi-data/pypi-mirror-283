## To make changes 

### change version in setup.py 

```sh
pip3 install -e . 
```

```sh
python3 -m build 
```

```sh
python3 -m twine upload dist/* 
```

### To use this package 

```sh
pip3 install route-knorket
```

### Example command to register a router

```sh
route-knorket --jwt enroll.txt 
```