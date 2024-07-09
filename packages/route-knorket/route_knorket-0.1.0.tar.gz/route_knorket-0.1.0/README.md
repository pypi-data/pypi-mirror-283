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
pip3 install ziti-router
```

### Example command to register a router

```sh
ziti-router --jwt enroll.txt --controller=ec2-13-60-60-200.eu-north-1.compute.amazonaws.com --controllerFabricPort=6262 --force
```