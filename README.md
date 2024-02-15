# **LINK TODO LIST**    
This is a TODO LIST that allows users to link their browser history to each item on the list
    
## **Prerequest**:    
### Data    
Assign the path for places.sqlite to .env    
```    
$ echo "PLACES_SQLITE=<path for places.sqlite>" > .env    
```    
    
### Enviroment (optional)    
create virtual enviroment <br>    
```    
$ python -m virtualvenv venv    
$ source venv/bin/activate    
```    
    
### Install pakages    
```    
$ pip install -r requirements.txt    
```    
    
## **Usage**:    
### Read Todo List
```    
$ python main.py r
```

### Create Item
```    
$ python main.py i --item_name
```

### Create Url
```    
$ python main.py u --item_id --content
```

### Remove Item from list
```
$ python main.py d --item_id --status
```
