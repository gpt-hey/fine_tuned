## server setup
```
$ pip install -r requirements.txt
$ supervisord -c supervisord.conf
```

## docker
```
$docker build -t gpt_python_server .
$docker run -p 8081:8081 gpt_python_server
$docker docker exec -it <container-id> /bin/bash
```



## prompt examples

// 1. ask server to set up reminder
"@remindme to take notes! in 5 mins"

// 2. ask server questions using llama2 7B gguf model
"@gguf tell me about yourself"


## setup
```
// Mac (only), need to update transformer to use 4.30.0
// Note: setup for MAC
// 1. create env
$python3 -m venv venv

// 2. activate venv
$ source venv/bin/activate

// 3. install package (one-time)
$ pip install -r requirements.txt

// 4. deactivate
$ deactivate
```


# setup for linux (aarch64)
```
// oracle linux (aarch64), need to update transformer to use 4.18.0
$ conda create --name myenv python=3.8
$ source activate myenv
$ conda install --file requirements.txt
$ conda install pillow numpy

$ conda install langchain
$ conda install sentence-transformers
$ conda install faiss-cpu
$ conda install ctransformers
```

## llama_cpp
```
$ pip install -r requirements.txt
$ python llama_cpp.py
```