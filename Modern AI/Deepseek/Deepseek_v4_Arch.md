# DeepSeek-V4 Focus Notes

This document explains only three parts of the DeepSeek-V4 paper:

1. Attention mechanism
2. Manifold-Constrained Hyper-Connections, or mHC
3. Routed Mixture-of-Experts, or Routed MoEs

No images are included.

---

## 1. Attention Mechanism

### What is an attention mechanism?

An attention mechanism is the part of a Transformer model that helps each token decide which earlier tokens are important.

For example, in a sentence or document, a word may need information from another word that appeared much earlier. Attention allows the model to compare the current token with previous tokens and pull useful information from them.

In simple words:

> Attention is how the model chooses what to look at.

<img width="2317" height="353" alt="image" src="https://github.com/user-attachments/assets/d49dcc45-797a-42af-9681-4c93adb2178d" />


### Why normal attention becomes expensive

Standard Transformer attention compares many tokens with many other tokens. As the context becomes longer, the cost grows very quickly.

For short text, this is manageable. For a one-million-token context, it becomes extremely expensive in:

- computation, measured as FLOPs;
- memory, especially the KV cache;
- inference latency, meaning how long the model takes to respond.

### How DeepSeek-V4 implements attention

DeepSeek-V4 uses a hybrid attention design. Instead of relying only on normal dense attention, it combines:

- CSA: Compressed Sparse Attention
- HCA: Heavily Compressed Attention
- SWA: Sliding Window Attention branch

These are used together to make one-million-token context practical.

### CSA: Compressed Sparse Attention

CSA works in two main steps.

#### Step 1: Compress old KV entries

The model stores previous token information as Key-Value entries, usually called the KV cache.

CSA groups several KV entries together and compresses them into fewer entries. In the paper, CSA compresses every `m` tokens into one compressed entry.

This means the model does not need to keep every old token in full detail for long-range attention.

#### Step 2: Select only useful compressed entries

After compression, CSA does not attend to all compressed entries. It uses a small indexer called the Lightning Indexer.

The indexer scores compressed blocks and selects the top-k most useful ones for the current query token.

So CSA can be understood as:

> First summarize the past, then look only at the most relevant summaries.

### HCA: Heavily Compressed Attention

HCA compresses the KV cache even more aggressively than CSA.

In the paper, HCA uses a much larger compression ratio, written as `m'`, where `m'` is much greater than `m`.

Unlike CSA, HCA does not perform sparse top-k selection. Instead, it attends densely over a much smaller set of heavily compressed KV entries.

So HCA can be understood as:

> Keep a very compact memory of the long past, then attend over that compact memory.

### Sliding Window Attention branch

Compression is useful for old context, but recent tokens often need fine detail.

To handle this, DeepSeek-V4 also keeps a small sliding window of recent uncompressed KV entries.

This helps the model preserve local dependencies, such as grammar, nearby references, and short-range meaning.

### Why the hybrid design is useful

Each attention part has a different role:

| Component | Main role |
|---|---|
| CSA | Find important information from far back in the context |
| HCA | Maintain cheap global memory over very long context |
| Sliding Window Attention | Preserve recent local detail |

Together, they reduce both compute and memory while still allowing the model to use very long context.

---

## 2. Manifold-Constrained Hyper-Connections, or mHC

<img width="1486" height="874" alt="image" src="https://github.com/user-attachments/assets/e668fde6-7db4-40c7-8e05-6af1611979b1" />


### What are residual connections?

Residual connections are shortcuts between neural network layers.

Instead of forcing each layer to completely rewrite the information it receives, a residual connection lets information pass forward directly while the layer adds changes on top.

In simple words:

> A residual connection lets the model carry old information forward safely.

Residual connections are important because they help deep models train more stably.

### What are Hyper-Connections?

Hyper-Connections extend normal residual connections by widening the residual stream.

Instead of keeping only one residual path, Hyper-Connections maintain multiple residual paths. These paths can be mixed before and after each layer.

This gives the model more flexibility, because information can flow through several routes instead of only one.

### Why standard Hyper-Connections can be unstable

The paper says standard Hyper-Connections can improve performance, but they may cause numerical instability when many layers are stacked.

The reason is that the residual mixing matrix can expand signals too much. If this happens repeatedly through many layers, values may grow too large during forward or backward passes.

### What is mHC?

mHC stands for Manifold-Constrained Hyper-Connections.

It keeps the main benefit of Hyper-Connections, which is richer residual routing, but adds mathematical constraints to make the residual mapping stable.

In simple words:

> mHC gives the model more residual paths, but controls how strongly those paths can amplify signals.

### How DeepSeek-V4 implements mHC

DeepSeek-V4 uses mHC around Transformer blocks. It applies three kinds of mixing:

- pre-block mixing;
- residual mixing;
- post-block mixing.

These mix the widened residual stream before and after attention or MoE layers.

### The key stability constraint

The main idea is to constrain the residual mapping matrix so it becomes a doubly stochastic matrix.

A doubly stochastic matrix has two properties:

- every row sums to 1;
- every column sums to 1;
- all values are non-negative.

This keeps the transformation non-expansive, meaning it should not amplify the signal uncontrollably.

### How the constraint is applied

DeepSeek-V4 first generates raw mixing parameters dynamically from the input.

Then it constrains them:

- input and output mappings are passed through sigmoid functions so they stay bounded;
- the residual mapping is projected into the doubly stochastic matrix space using the Sinkhorn-Knopp algorithm.

The Sinkhorn-Knopp algorithm repeatedly normalizes rows and columns until the matrix satisfies the desired constraints.

### Why mHC matters

mHC improves the model by giving it a richer way to pass information through layers while reducing the risk of unstable signal growth.

Its role in DeepSeek-V4 is not mainly about long-context efficiency. Its role is more about model quality and training stability.

---

## 3. Routed Mixture-of-Experts, or Routed MoEs

### What is a Mixture-of-Experts model?

A Mixture-of-Experts model contains many expert networks inside one model.

Instead of using all experts for every token, the model chooses only a small number of experts for each token.

In simple words:

> MoE makes the model very large in total size, but only uses a small part of it for each token.

This allows the model to increase knowledge capacity without increasing computation by the same amount.

<img width="785" height="874" alt="image" src="https://github.com/user-attachments/assets/e8a8d62b-c1c4-4466-94cf-eadf9ac78563" />


### What is routing?

Routing is the process of deciding which experts should handle each token.

A router looks at the token representation and assigns the token to selected experts.

In simple words:

> Routing is expert selection.

### What are routed experts and shared experts?

DeepSeek-style MoE uses two kinds of experts:

- routed experts;
- shared experts.

Routed experts are selected differently for different tokens. A token may activate only a few routed experts out of many available experts.

Shared experts are used more generally and are available across tokens.

### How DeepSeek-V4 implements Routed MoEs

DeepSeek-V4 keeps the DeepSeekMoE design from earlier DeepSeek models, with some changes.

The paper says DeepSeek-V4 uses MoE layers for feed-forward networks inside Transformer blocks.

For each token, only a small number of routed experts are activated.

### Expert counts in DeepSeek-V4

The paper gives these model setups:

| Model | Routed experts per MoE layer | Shared experts | Routed experts activated per token |
|---|---:|---:|---:|
| DeepSeek-V4-Flash | 256 | 1 | 6 |
| DeepSeek-V4-Pro | 384 | 1 | 6 |

This means that although each layer contains many experts, each token only uses 6 routed experts, plus the shared expert.

### Hash routing in early layers

DeepSeek-V4 uses Hash routing in the first few MoE layers.

Hash routing chooses experts using a predefined hash function based on the input token ID.

This is simpler than fully learned routing and is used in the initial MoE layers.

### Load balancing

A common problem in MoE models is expert imbalance.

If the router sends too many tokens to the same experts, some experts become overloaded while others are underused.

DeepSeek-V4 uses an auxiliary-loss-free load balancing strategy, plus a small sequence-wise balance loss, to avoid extreme imbalance inside individual sequences.

### Why Routed MoEs matter

Routed MoEs let DeepSeek-V4 have very large total parameter counts while keeping per-token computation much smaller.

For example:

- DeepSeek-V4-Pro has 1.6T total parameters, but only 49B are activated per token.
- DeepSeek-V4-Flash has 284B total parameters, but only 13B are activated per token.

This is one of the main reasons the model can scale capacity while remaining computationally practical.

---
## 4. Infrastructure

### Why infrastructure matters

DeepSeek-V4 is too large to fit on a single GPU, so the model must be split across multiple GPUs or even multiple racks.

In practice this means:

- The model is too big to load on a single GPU, so it has to live on multiple GPUs or racks.
- Each GPU holds only some layers of the model.
- There is some latency in each stage, and GPUs end up waiting for one another to finish.

For an MoE model, each token also has to be **dispatched** to the GPUs that hold the chosen experts, and the expert outputs have to be **combined** back. These dispatch and combine steps involve cross-GPU communication, which can dominate runtime if not overlapped with computation.

A single MoE step can be broken down into four parts:

- DISPATCH: send tokens to the GPUs that own the selected experts.
- LAYER 1 / LAYER 2: the expert feed-forward computation, with an activation (ACT) in between.
- COMBINE: gather expert outputs back to the source GPU.

The paper compares three ways of scheduling these parts.

### Normal approach

In the normal approach, everything happens sequentially on the critical path:

<img width="784" height="280" alt="image" src="https://github.com/user-attachments/assets/f37ac724-9ee2-46a2-8f59-9ee2e1786f10" />


While DISPATCH runs, the compute units are idle. While LAYER 1 and LAYER 2 run, the network is idle. While COMBINE runs, compute is idle again.

In simple words:

> Communication and computation take turns, so the GPU is never fully busy.

### Comet approach

The Comet approach overlaps communication with computation. DISPATCH and COMBINE are run as separate streams that can happen in parallel with the LAYER 1 / ACT / LAYER 2 compute path.

Layout:

<img width="518" height="280" alt="image" src="https://github.com/user-attachments/assets/27f70736-3fde-4d76-a5ac-175829280832" />


This hides part of the communication cost behind compute, but the overlap is coarse: one full DISPATCH overlaps with one full LAYER block, and one full COMBINE overlaps with the next.

### DeepSeek-V4 approach

DeepSeek-V4 takes the overlap idea further by **chunking** the work and interleaving DISPATCH, compute, ACT, and COMBINE at a finer granularity.

Layout:

<img width="1306" height="339" alt="image" src="https://github.com/user-attachments/assets/f229ed6c-ecbb-49d0-95f9-8a17774ed835" />


Key ideas:

- A single DISPATCH feeds **several** LAYER 1 / LAYER 2 micro-blocks.
- ACT and COMBINE are interleaved with the next compute micro-block.
- While one chunk is computing, the previous chunk’s COMBINE and the next chunk’s ACT can run in parallel.

The effect is that GPUs spend much less time waiting. Communication for one chunk is hidden behind computation of another chunk, and the pipeline stays full.

### Why the hybrid schedule is useful

| Approach | Communication and compute overlap | GPU utilization |
|---|---|---|
| Normal | None, fully sequential | Low |
| Comet | Coarse, one DISPATCH / COMBINE overlapped with one LAYER block | Medium |
| DeepSeek-V4 | Fine-grained, chunked DISPATCH / ACT / COMBINE interleaved with compute | High |

In simple words:

> DeepSeek-V4 breaks the MoE step into smaller pieces and pipelines them, so dispatch, compute, and combine are happening at the same time on different chunks.

This is what makes very large MoE models with hundreds of experts and trillions of total parameters practical to run at scale.

---

## Short Summary

| Topic | Brief meaning | DeepSeek-V4 implementation |
|---|---|---|
| Attention mechanism | Chooses what previous tokens to look at | Hybrid CSA + HCA + sliding window attention |
| mHC | Stable enhanced residual connections | Widened residual stream with constrained doubly stochastic mixing |
| Routed MoEs | Selects a few experts per token | DeepSeekMoE with many routed experts, one shared expert, and 6 routed experts active per token |
| Infrastructure | Schedules dispatch/compute/combine across GPUs | Chunked, fine-grained interleaving of DISPATCH, LAYER 1/2, ACT, and COMBINE |

DeepSeek-V4’s main design pattern is efficient scaling: compress what is too large, route only to what is needed, constrain what may become unstable, and pipeline what would otherwise wait.
