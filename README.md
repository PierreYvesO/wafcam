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

## UNUSED/OPTIONNAL
<details><summary>GPU Config</summary>
<p>
(Not used at the moment but it could be possible to use GPU to detect objects)
Tensorflow config : 
- Update Nvidia drivers tested with 460.x versions
- Download CUDA 11.2 [here](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exelocal)
- Download cuDNN 8.1.1 [here](https://developer.nvidia.com/rdp/cudnn-download) unzip and add <DIR>/cuda/bin to you path
- test with 
    ```
  python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
    ```
</p>
</details>

