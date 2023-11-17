## setup
```
// Mac (only), need to update transformer to use 4.30.0

// oracle linux (only), need to update transformer to use 4.18.0
$ pip install --upgrade pip
$ pip install torch==1.10.0 torchvision==0.11.1 torchaudio==0.10.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html
// install swig manually since yum install a very old version
$ scp ~/Downloads/swig-4.1.1.tar.gz opc@129.213.151.7:/home/opc
swig-4.1.1.tar.gz
$ tar -xzf swig-4.1.1.tar.gz
$ cd swig-4.1.1/
$ ./configure
$ make
$ sudo make install
$ swig -version
// install pytorch
$ conda install -c pytorch faiss-cpu=1.7.4 mkl=2021 blas=1.0=mkl
$ conda install --file requirements.txt
// install other libs that are not on conda channel
$ pip install accelerate bitsandbytes langchain sentence-transformers unstructured xformers "unstructured[pdf]"
// install openGL
$ sudo yum install mesa-libGL
$ pip install accelerate
$ pip install -i https://test.pypi.org/simple/ bitsandbytes

//
$ pip uninstall torchvision
$ pip install --upgrade git+https://github.com/pytorch/vision.git
$ conda install pillow numpy

$python3 -m venv env
// install package
$ pip install -r requirements.txt

// activate
$ source venv/bin/activate

// deactivate
$ deactivate
```
