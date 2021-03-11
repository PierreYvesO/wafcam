# wafcam
## Environement
using python 3.8
Setup python environnement (https://docs.python.org/3/library/venv.html)
```
pip install -r requirements.txt
```
In case you want to add a new module to the project make sure to update the requirements
```
pip freeze < requirements.txt
```

## Setup WAMP (on Windows 10)
Version : 3.2.3

Installation guide
- Choose your language
- Choose the folder destination for WAMP
- Install the default configuration
    - PHP 7.3.21
    - MySQL 5.7.31
    - PhpMyAdmin 5.0.2
- Choose your default IDE and browser

## React app
Install node (https://nodejs.org/en/download/)

node version : 14.16.0

npm version : 6.14.11

Add those libraries
```
npm i -s react-dom react-router-dom node-sass@4.14.1
```

Now you can start the application and see the URL where your app is running (http://localhost:3000 for example)
```
npm start
```

## Unused/Optional Setup
<details><summary>GPU Config</summary>

(Not used at the moment but it could be possible to use GPU to detect objects)
Tensorflow config : 
- Update Nvidia drivers tested with 460.x versions
- Download CUDA 11.2 [here](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)
- Download cuDNN 8.1.1 [here](https://developer.nvidia.com/rdp/cudnn-download) unzip and add <DIR>/cuda/bin to you path
- test with 
    ```
  python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
    ```

</details>
