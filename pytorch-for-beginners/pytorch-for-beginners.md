

```python
import torch
```


```python
print("torch version:{}".format(torch.__version__))
```

    torch version:1.2.0



```python
a = torch.ones(5)
print(a)
b = torch.zeros(5)
print(b)
```

    tensor([1., 1., 1., 1., 1.])
    tensor([0., 0., 0., 0., 0.])



```python
c = torch.tensor([1.0,2.0,3.0,4.0,5.0])
```


```python
print(c)
```

    tensor([1., 2., 3., 4., 5.])



```python

d = torch.zeros(3,2)
print(d)

e = torch.ones(3,2)
print(e)

f = torch.tensor([[1.0, 2.0],[3.0, 4.0]])
print(f)

# 3D Tensor
g = torch.tensor([[[1., 2.], [3., 4.]], [[5., 6.], [7., 8.]]])
print(g)
```

    tensor([[0., 0.],
            [0., 0.],
            [0., 0.]])
    tensor([[1., 1.],
            [1., 1.],
            [1., 1.]])
    tensor([[1., 2.],
            [3., 4.]])
    tensor([[[1., 2.],
             [3., 4.]],
    
            [[5., 6.],
             [7., 8.]]])



```python
print(f.shape)
 
print(e.shape)
 
print(g.shape)
```

    torch.Size([2, 2])
    torch.Size([3, 2])
    torch.Size([2, 2, 2])



```python
print(c[2])
```

    tensor(3.)



```python
print(f[:])
```

    tensor([[1., 2.],
            [3., 4.]])



```python
print(c[1:3])
```

    tensor([2., 3.])



```python
print(c[:4])
```

    tensor([1., 2., 3., 4.])



```python
print(f[0,:])
```

    tensor([1., 2.])



```python
int_tensor = torch.tensor([[1,2,3],[4,5,6]])
print(int_tensor.dtype)
 
# What if we changed any one element to floating point number?
int_tensor = torch.tensor([[1,2,3],[4.,5,6]])
print(int_tensor.dtype)
print(int_tensor)
 
# This can be overridden as follows
int_tensor = torch.tensor([[1,2,3],[4.,5,6]], dtype=torch.int32)
print(int_tensor.dtype)
print(int_tensor)
```

    torch.int64
    torch.float32
    tensor([[1., 2., 3.],
            [4., 5., 6.]])
    torch.int32
    tensor([[1, 2, 3],
            [4, 5, 6]], dtype=torch.int32)



```python
import numpy as np
```


```python
f_numpy = f.numpy()
print(f_numpy)
```

    [[1. 2.]
     [3. 4.]]



```python
h = np.array([[8,7,6,5],[4,3,2,1]])
h_tensor = torch.from_numpy(h)
print(h_tensor)
```

    tensor([[8, 7, 6, 5],
            [4, 3, 2, 1]])



```python
# Create tensor
tensor1 = torch.tensor([[1,2,3],[4,5,6]])
tensor2 = torch.tensor([[-1,2,-3],[4,-5,6]])
 
# Addition
print(tensor1+tensor2)
# We can also use
print(torch.add(tensor1,tensor2))
 
# Subtraction
print(tensor1-tensor2)
# We can also use
print(torch.sub(tensor1,tensor2))
 
# Multiplication
# Tensor with Scalar
print(tensor1 * 2)
 
# Tensor with another tensor
# Elementwise Multiplication
print(tensor1 * tensor2)
```

    tensor([[ 0,  4,  0],
            [ 8,  0, 12]])
    tensor([[ 0,  4,  0],
            [ 8,  0, 12]])
    tensor([[ 2,  0,  6],
            [ 0, 10,  0]])
    tensor([[ 2,  0,  6],
            [ 0, 10,  0]])
    tensor([[ 2,  4,  6],
            [ 8, 10, 12]])
    tensor([[ -1,   4,  -9],
            [ 16, -25,  36]])



```python
# Matrix multiplication
tensor3 = torch.tensor([[1,2],[3,4],[5,6]])
print(torch.mm(tensor1,tensor3))
 
# Division
# Tensor with scalar
print(tensor1/2)
 
# Tensor with another tensor
# Elementwise division
print(tensor1/tensor2)
```

    tensor([[22, 28],
            [49, 64]])
    tensor([[0, 1, 1],
            [2, 2, 3]])
    tensor([[-1,  1, -1],
            [ 1, -1,  1]])



```python
# Create a tensor for CPU
# This will occupy CPU RAM
tensor_cpu = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], device='cpu')
```


```python

```
