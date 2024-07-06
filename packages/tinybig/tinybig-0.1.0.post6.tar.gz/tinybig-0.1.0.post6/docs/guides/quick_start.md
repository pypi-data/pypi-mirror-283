# Quickstart

In this quickstart tutorial, we will walk you through the APIs for common tasks in deep function learning.
We assume you have correctly installed the latest tinybig and its dependency packages already.
If you haven't installed them yet please refer to the [installation page](installation.md) for more detailed guidance.

## Loading Datasets

### Base Dataloaders and Dataset

{{toolkit}} offers two base primitives to work with data: `tinybig.data.base_data.dataloader` and `tinybig.data.base_data.dataset`.
`dataset` stores the data instances (including features, labels, and optional encoders for feature embedding), and
`dataloader` wraps an iterable around the `dataset`.

Based on `dataloader` and `dataset`, several dataloaders for specific data modalities have been created:

```python
>>> import tinybig as tb
>>> from tinybig.data import dataloader, dataset
>>> from tinybig.data import function_dataloader, vision_dataloader, text_dataloader, tabular_dataloader
```

Built based on torchvision and torchtext, {{toolkit}} can load many real-world vision data, like MNIST and CIFAR10, and
text data, like IMDB, SST2 and AGNews, for model training and evaluation. In addition, {{toolkit}} also offers a variety
of other well-known datasets by itself, including continuous function datasets, like Elementary, Composite and Feynman functions,
and classic tabular datasets, like Iris, Diabetes and Banknote.

### MNIST Dataloader

In this quickstart tutorial, we will take the MNIST dataset as an example to illustrate how {{toolkit}} loads data:
```python
>>> from tinybig.data import mnist
>>> 
>>> mnist_data = mnist(name='mnist', train_batch_size=64, test_batch_size=64)
>>> mnist_loaders = mnist_data.load(cache_dir='./data/')
>>> train_loader = mnist_loaders['train_loader']
>>> test_loader = mnist_loaders['test_loader']
```
The above code will download mnist from torchvision to a local directory `'./data/'`.
??? quote "Data downloading outputs"
    ```
    Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 403: Forbidden
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-images-idx3-ubyte.gz to ./data/MNIST/raw/train-images-idx3-ubyte.gz
    100%|██████████| 9912422/9912422 [00:00<00:00, 12146011.18it/s]
    Extracting ./data/MNIST/raw/train-images-idx3-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 403: Forbidden
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/train-labels-idx1-ubyte.gz to ./data/MNIST/raw/train-labels-idx1-ubyte.gz
    100%|██████████| 28881/28881 [00:00<00:00, 278204.89it/s]
    Extracting ./data/MNIST/raw/train-labels-idx1-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
    Failed to download (trying next):
    HTTP Error 403: Forbidden
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw/t10k-images-idx3-ubyte.gz
    100%|██████████| 1648877/1648877 [00:04<00:00, 390733.03it/s]
    Extracting ./data/MNIST/raw/t10k-images-idx3-ubyte.gz to ./data/MNIST/raw
    
    Downloading http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
    Failed to download (trying next):
    HTTP Error 403: Forbidden
    
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz
    Downloading https://ossci-datasets.s3.amazonaws.com/mnist/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz
    100%|██████████| 4542/4542 [00:00<00:00, 2221117.96it/s]
    Extracting ./data/MNIST/raw/t10k-labels-idx1-ubyte.gz to ./data/MNIST/raw
    ```

With the `train_loader` and `test_loader`, we can access the MNIST image and label data mini-batches as follows:

```python
>>> for X, y in train_loader:
...     print('X shape:', X.shape, 'y.shape', y.shape)
...     print('X', X)
...     print('y', y)
...     break
```

??? quote "Data batch printing outputs"
    ```
    X shape: torch.Size([64, 784]) y.shape torch.Size([64])
    X tensor([[-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242],
            [-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242],
            [-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242],
            ...,
            [-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242],
            [-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242],
            [-0.4242, -0.4242, -0.4242,  ..., -0.4242, -0.4242, -0.4242]])
    y tensor([3, 7, 8, 5, 6, 1, 0, 3, 1, 7, 4, 1, 3, 4, 4, 8, 4, 8, 2, 4, 3, 5, 5, 7,
            5, 9, 4, 2, 2, 3, 3, 4, 1, 2, 7, 2, 9, 0, 2, 4, 9, 4, 9, 2, 1, 3, 6, 5,
            9, 4, 4, 8, 0, 3, 2, 8, 0, 7, 3, 4, 9, 4, 0, 5])
    ```

Note that images loaded via the `tinybig.data.mnist` will flat and normalize the MNIST images of size $28 \times 28$ into
vectors of length $784$ via the following `torchvision.transforms` code:
```python
transform = torchvision.transforms.Compose([
    transforms.ToTensor(),
    Normalize((0.1307,), (0.3081,)),
    torch.flatten
])
```

## Creating RPN Models

To model the underlying data distribution mapping $f: R^m \to R^n$, the {{our}} model disentangle the input data from 
model parameters into three component functions:

* **Data Expansion Function**: $\kappa: R^m \to R^D$,
* **Parameter Reconciliatoin Function**: $\psi: R^l \to R^{n \times D}$,
* **Remainder Function** $\pi: R^m \to R^n$,

where $m$ and $n$ denote the input and output space dimensions, respectively. Notation $D$ denotes the target expansion 
space dimension (determined by the expansion function and input dimension $m$) and $l$ is the number of learnable parameters 
in the model (determined by the reconciliation function and dimensions $n$ and $D$).

So, the underlying mapping $f$ can be approximated by {{our}} as the inner product of the expansion function with
the reconciliation function, subsequentlly summed with the remainder function:
$$
g(\mathbf{x} | \mathbf{w}) = \left \langle \kappa(\mathbf{x}), \psi(\mathbf{w}) \right \rangle + \pi(\mathbf{x}),
$$
where for any input data instance $\mathbf{x} \in R^m$.

### Data Expansion Function

Various data expansion functions have been implemented in {{toolkit}} already. In this tutorial, we will use the 
Taylor's expansion function as an example to illustrate how data expansion works.
```python
>>> from tinybig.expansion import taylor_expansion
>>> 
>>> exp_func = taylor_expansion(name='taylor_expansion', d=2)
>>> x = X[0:1,:]
>>> x = X[0:1,:]
>>> D = exp_func.calculate_D(m=x.size(1))
>>> print('D:', D)
>>> 
>>> kappa_x = exp_func(x=x)
>>> print('x.shape', x.shape, 'kappa_x.shape', kappa_x.shape)
```
??? quote "Data expansion printing outputs"
    ```
    Expansion space dimension: 615440
    x.shape torch.Size([1, 784]) kappa_x.shape torch.Size([1, 615440])
    ```

In the above code, we define a Taylor's expansion function of order $2$, and apply the expansion function to a data batch
with one single data instance. (Note: the expansion function will accept batch inputs as 2D tensors, e.g., `X[0:1,:]` or `X`.
If we feed list, array or 1D tensor, e.g., `X[0,:]`, it will report errors).

All the expansion functions in {{toolkit}} has a method `taylor_expansion(m:int)`, which can automatically calculates the
target expansion space dimension $D$ based on the input space dimension, i.e., the parameter $m$. The calculated $D$ will
be used later in the reconciliation functions.

### Parameter Reconciliation Function

In {{toolkit}}, we have implemented different categories of parameter reconciliation functions. Below, we will use the
low-rank reconciliation (lorr) to illustrate how parameter reconciliation works

Assuming we need to build a {{our}} layer with the output dimension $n=64$ here:
```python
>>> from tinybig.reconciliation import lorr_reconciliation
>>> 
>>> rec_func = lorr_reconciliation(name='lorr_reconciliation', r=1)
>>> l = rec_func.calculate_l(n=64, D=D)
>>> print('Required learnable parameter number:', l)
```
??? quote "Lorr parameter reconciliation printing outputs"
    ```
    Required learnable parameter number: 615504
    ```

We will not create parameters here, which can be automatically created in the {{our}} head to be introduced later.

### Remainder Function

By default, we will use the zero remainder in this tutorial, which will not create any learnable parameters:
```python
>>> from tinybig.remainder import zero_remainder

>>> rem_func = zero_remainder(name='zero_remainder', require_parameters=False, enable_bias=False)
```

### RPN Head

Based on the above component functions, we can combine them together to define the {{our}} mode. Below, we will first
define the {{our}} head first, which will be used to compose the layers of {{our}}.
```python
>>> from tinybig.module import rpn_head
>>> 
>>> head = rpn_head(m=784, n=64, channel_num=1, data_transformation=exp_func, parameter_fabrication=rec_func, remainder=rem_func)
```
Here, we build a rpn head with one channel of parameters. The parameter `data_transformation` is a general name of 
`data_expansion`, and `parameter_fabrication` can be viewed as equivalent to `parameter_reconciliation`.
We use the names `data_transformation` and `parameter_fabrication` here, just to provide {{toolkit}} with more possibility
to handle other different learning problems.

### RPN Layer

The above head can be used to build the first {{our}} layer of {{our}}: 
```python
>>> from tinybig.module import rpn_layer
>>> 
>>> layer_1 = rpn_layer(m=784, n=64, heads=[head])
```

Via a similar process, we can also define two more {{our}} layers:
```python

```

### Deep RPN Model with Multi-Layers


## Training Models

### Training Setups

### Training

### Testing

## Saving and Loading Models

## Evaluating and Saving Results

## Using Configs for Learning Pipeline Creation

