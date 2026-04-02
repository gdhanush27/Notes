# TurboQuant — Structured Walkthrough

## 1. Big-picture: What is TurboQuant?

**Short definition**

TurboQuant is a **vector quantization algorithm** from Google Research (ICLR 2026) that:

- Compresses high-dimensional vectors (especially KV caches in LLMs and embeddings for vector search).
- Uses **random rotation + scalar quantization + a 1-bit residual correction (QJL)**.
- Achieves **near-optimal distortion** (MSE and inner product) with **very low memory overhead**.
- Requires **no training or fine-tuning**.

Primary use-cases:

- **KV cache compression** for long-context LLM inference
- **Embedding compression** for vector databases (ANN search)

[Quick Presentation](https://htmldrop.pythonanywhere.com/d/0f73e3b02c)

---

## 2. Why TurboQuant exists: the problem it solves

### 2.1 The KV cache memory problem

In transformers, during autoregressive decoding:

- Keys and values are generated per token
- Stored in a **KV cache**
- Reused for all future tokens

Problem:

KV cache grows **linearly with sequence length**

Example:

- LLaMA 2 7B (FP16)
- ~0.5 MB per token
- 4096 tokens ≈ 2 GB KV cache

At long context (128k tokens), KV cache can exceed model weight size.

---

### 2.2 Traditional vector quantization limitations

Typical vector quantization:

1. Split vectors into blocks
2. Store quantization metadata
   - scale
   - zero point
   - min/max
3. Quantize values

Problem:

Metadata overhead reduces effective compression at low bit-width.

---

### 2.3 TurboQuant’s objective

TurboQuant aims to:

- Minimize quantization metadata
- Achieve near-optimal distortion
- Preserve inner products
- Work online without training

---

## 3. High-level pipeline

```mermaid
flowchart LR
  A[Input vector x] --> B[Random rotation R]
  B --> C[MSE scalar quantizer Q]
  C --> D[Residual r]
  D --> E[QJL 1-bit transform]
  E --> F[Compressed representation]
  F --> G[Approximate reconstruction]
````

Pipeline:

1. Rotate vector
2. Quantize coordinates
3. Compute residual
4. Encode residual using QJL
5. Store compressed representation

---

## 4. Core ideas in plain language

### 4.1 Random rotation

Rotate vector:

$$
y = R x
$$

Why:

After random rotation:

* coordinates behave similarly
* distribution becomes predictable
* same scalar quantizer can be applied to all coordinates

---

### 4.2 PolarQuant concept

Convert Cartesian vector:

$$
(x_1, x_2, ..., x_d)
$$

into:

* radius ( r )
* direction angles ( \theta )

Benefits:

* avoids storing dynamic normalization parameters
* reduces quantization metadata
* enables consistent quantization grid

Analogy:

Cartesian:

> 3 blocks east, 4 blocks north

Polar:

> 5 blocks at 37°

---

### 4.3 QJL residual correction

QJL = Quantized Johnson–Lindenstrauss transform

Steps:

1. project residual into lower dimension
2. keep only sign bits

$$
s = sign(J r)
$$

Properties:

* preserves inner products
* reduces bias from scalar quantization
* extremely compact (1 bit per dimension)

Important because:

Attention uses dot products:

$$
Attention(Q,K) = QK^T
$$

---

## 5. Detailed algorithm

### 5.1 Input

Vector:

$$
x \in \mathbb{R}^d
$$

Goal:

Minimize distortion:

MSE:

$$
E[||x-\hat{x}||^2]
$$

Inner product error:

$$
E[(x^T y - \hat{x}^T \hat{y})^2]
$$

---

### 5.2 Two-stage quantizer

#### Stage 1 — MSE scalar quantization

Rotate:

$$
y = R x
$$

Quantize each coordinate:

$$
\tilde{y_i} = Q(y_i)
$$

Residual:

$$
r = y - \tilde{y}
$$

---

#### Stage 2 — QJL encoding

Project residual:

$$
z = J r
$$

Store sign:

$$
s_i = sign(z_i)
$$

Final compressed representation:

* scalar quantization indices
* sign bits from QJL

---

### 5.3 Near-optimal distortion guarantee

TurboQuant achieves distortion close to theoretical lower bound:

constant factor ≈ 2.7

Valid across:

* all bit-widths
* all dimensions

---

## 6. Toy example

Assume:

dimension:

```
d = 8
```

bit budget:

```
3 bits per element
```

---

### Step 1 — rotation

$$
y = R x
$$

---

### Step 2 — scalar quantization

each coordinate mapped to 4 levels (2 bits)

example:

```
y = [0.2, -1.1, 0.7, ...]
```

quantized:

```
ŷ = [0.25, -1.0, 0.75, ...]
```

---

### Step 3 — residual

$$
r = y - \tilde{y}
$$

small correction vector

---

### Step 4 — QJL projection

dimension reduced:

```
8 → 4
```

store signs:

```
[+1, -1, +1, +1]
```

---

### Step 5 — reconstruction

approximate inverse rotation:

$$
\hat{x} = R^T \tilde{y}
$$

QJL bits improve dot product estimation.

---

## 7. Use cases

### 7.1 KV cache compression

Benefits:

* reduce GPU memory usage
* enable longer context
* improve batching capacity

Typical performance:

| bits    | quality            |
| ------- | ------------------ |
| 4 bit   | near FP16          |
| 3.5 bit | lossless quality   |
| 2.5 bit | slight degradation |

---

### 7.2 vector search

TurboQuant can compress embeddings used in:

* RAG pipelines
* semantic search
* recommendation systems

Benefits:

* smaller index size
* faster retrieval
* high recall

---

## 8. Practical implementation notes

### 8.1 open-source implementations

Examples:

* turboquant-pytorch
* vLLM integrations
* llama.cpp forks

---

### 8.2 empirical observations

4-bit sweet spot:

* negligible quality drop
* strong compression

3-bit:

* works best for large models (>8B parameters)

values more sensitive than keys.

recent tokens often kept in FP16:

```
residual window ≈ 128–256 tokens
```

---

## 9. Example integration workflow

1. choose model

example:

```
Llama 3 8B
context = 32k
```

2. choose bit width

recommended starting point:

```
4-bit KV cache
```

3. integrate quantizer

quantization applied to:

* key vectors
* value vectors

4. combine optimizations

* weight quantization (GPTQ / AWQ)
* paged attention
* FP16 residual window

---

## 10. Summary

TurboQuant combines:

random rotation
scalar quantization
QJL residual encoding

Advantages:

* near-optimal distortion
* minimal metadata overhead
* no training required
* strong KV cache compression

Main impact areas:

* long-context LLM inference
* vector database compression

---
