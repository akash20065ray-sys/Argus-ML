# 🧬 ArgusML: DSA Engineering & Algorithmic Specification

> **Deep-Dive Data Structure Analysis, Complexity Proofs, and Pseudocode**  
> *Location:* `docs/DSA_SPECIFICATION.md`

---

## 1. Circular FIFO EventQueue (`core/dsa/queue.py`)

### 1.1 Mathematical Model & Invariants
* Bounded array `buffer` of length $C$ (Capacity, default $C=5000$).
* Pointers: `head` (next dequeue slot) and `tail` (next enqueue slot).
* Counter: `count` (current elements in queue, $0 \le \text{count} \le C$).
* Modular index arithmetic:
  $$\text{tail}_{\text{next}} = (\text{tail} + 1) \pmod C$$
  $$\text{head}_{\text{next}} = (\text{head} + 1) \pmod C$$

### 1.2 Overflow Policy
When $\text{count} == C$, rather than blocking or throwing exceptions, ArgusML drops the oldest element:
$$\text{head} = (\text{head} + 1) \pmod C, \quad \text{dropped\_events} = \text{dropped\_events} + 1$$
**Complexity:** Enqueue $O(1)$, Dequeue $O(1)$, Space $O(C)$.

---

## 2. MetricSlidingWindow Deque (`core/dsa/deque.py`)

### 2.1 The $O(1)$ Amortized Rolling Telemetry Proof
Let $W$ be the sliding window size. Traditional recalculation of accuracy across all $W$ elements takes $O(W)$ time per incoming event.

**ArgusML Optimization:** We maintain running integer state variables:
* $TP$ (True Positives), $FP$ (False Positives), $TN$ (True Negatives), $FN$ (False Negatives)
* $N_{\text{labeled}} = TP + FP + TN + FN$

Upon arrival of event $E_{\text{new}}$ when $|\text{window}| == W$:
1. Evict oldest: $E_{\text{old}} = \text{window}[0]$.
2. If $E_{\text{old}}.\text{gt} == 1 \land E_{\text{old}}.\text{pred} == 1 \implies TP \gets TP - 1$.
3. If $E_{\text{new}}.\text{gt} == 1 \land E_{\text{new}}.\text{pred} == 1 \implies TP \gets TP + 1$.
4. Calculate accuracy:
   $$\text{Accuracy} = \frac{TP + TN}{N_{\text{labeled}}} \quad \implies O(1) \text{ time}$$

---

## 3. AlertMaxHeap (`core/dsa/heap.py`)

### 3.1 Binary Max-Heap Array Representation
A complete binary tree stored sequentially in array `heap`:
* For node at index $i$:
  * $\text{Parent}(i) = \lfloor \frac{i - 1}{2} \rfloor$
  * $\text{LeftChild}(i) = 2i + 1$
  * $\text{RightChild}(i) = 2i + 2$

### 3.2 Max-Heap Invariant
$$\forall i > 0, \quad \text{heap}[\text{Parent}(i)].\text{priority} \ge \text{heap}[i].\text{priority}$$

### 3.3 Pseudocode for `_sift_up` and `_sift_down`
```python
def _sift_up(self, i):
    parent = (i - 1) // 2
    while i > 0 and self.heap[i].priority > self.heap[parent].priority:
        self._swap(i, parent)
        i = parent
        parent = (i - 1) // 2

def _sift_down(self, i):
    n = len(self.heap)
    max_idx = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and self.heap[left].priority > self.heap[max_idx].priority:
        max_idx = left
    if right < n and self.heap[right].priority > self.heap[max_idx].priority:
        max_idx = right
    if max_idx != i:
        self._swap(i, max_idx)
        self._sift_down(max_idx)
```
**Complexity:** Push $O(\log N)$, Pop Max $O(\log N)$, Peek $O(1)$, Space $O(N)$.

---

## 4. DependencyGraph DAG (`core/dsa/graph.py`)

### 4.1 Adjacency List Structure
* $V = \text{Pipelines} \cup \text{Features} \cup \text{Models} \cup \text{Services}$
* $E = \text{Directed dependencies}$
* Forward adjacency: `forward_adj[u]` contains edges $(u \to v)$
* Reverse adjacency: `reverse_adj[v]` contains edges $(u \to v)$ (stored at $v$)

### 4.2 Reverse-BFS Algorithm for Root Cause Analysis
```python
def get_upstream_nodes(self, model_id):
    visited = set()
    queue = deque([model_id])
    upstream_features = []
    
    while queue:
        curr = queue.popleft()
        if curr != model_id and curr not in visited:
            visited.add(curr)
            upstream_features.append(self.nodes[curr])
            
        for edge in self.reverse_adj.get(curr, []):
            parent_id = edge.source_id
            if parent_id not in visited:
                queue.append(parent_id)
                
    return upstream_features
```
**Complexity:** $O(V + E)$ time, $O(V)$ space.
