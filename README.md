To run mypy :

```
poetry run mypy .
```

create image : 
```shell
docker build -t todolist_back .
```

run the image
```shell
docker run -p 8000:80 -e PORT=8000 -e HOST=0.0.0.0  todolist_back
```

run the app
```shell
fastapi.exe run .\src\todolist_back\start.py
```
