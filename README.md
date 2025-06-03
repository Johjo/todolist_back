To run mypy :

```
poetry run mypy .
```

create image : 
```shell
docker build -t todolist_back .
```

run the app
```shell
docker run -p 8000:8000 -e PORT=8000 -e HOST=0.0.0.0  mon-app-python
```
