"""
# ==============================================================================
# LABORATORY: DEEP LEARNING (PYTORCH DATALOADERS & TRAINING LOOPS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to train a neural network on 1 Million high-resolution 
# images. They load all 1 Million images into a massive Python List in RAM at 
# the start of the script. The script requires 800 Gigabytes of RAM. The computer 
# instantly crashes with an OutOfMemory (OOM) error.
#
# A senior AI engineer understands the PyTorch `Dataset` and `DataLoader` architecture. 
# They write a Custom Dataset class where the `__getitem__` method loads exactly ONE 
# image from the hard drive at a time. They pass this to a `DataLoader` with 
# `batch_size=64` and `num_workers=8`. PyTorch uses 8 CPU threads to mathematically 
# pre-fetch chunks of 64 images directly into the GPU VRAM just-in-time, keeping 
# system RAM usage strictly at 2 Gigabytes while training on millions of images.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master PyTorch `Dataset` and `DataLoader` architecture.
# - Execute batching, shuffling, and multi-processing workers.
# - Architect a mathematically perfect Training Loop.
#
# ==============================================================================
"""

import math
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PYTORCH API (SIMULATED FOR EDUCATION)
# ==============================================================================
# We simulate the PyTorch architecture so it runs on any machine instantly.

class SimulatedDataset:
    """Simulates torch.utils.data.Dataset"""
    def __init__(self, total_samples: int):
        self.total_samples = total_samples
        print(f"  [INIT] Registered Dataset with {total_samples:,} simulated images on disk.")
        
    def __len__(self):
        """The DataLoader must know the mathematical total size."""
        return self.total_samples
        
    def __getitem__(self, idx: int):
        """
        The critical architectural secret! 
        This is called lazily. It loads exactly ONE item from disk to RAM.
        """
        # Simulating disk I/O latency
        time.sleep(0.001) 
        # Return a mock Tensor (Image Data, Label)
        return {"data": f"Tensor_Image_{idx}", "label": idx % 10}


class SimulatedDataLoader:
    """Simulates torch.utils.data.DataLoader"""
    def __init__(self, dataset: SimulatedDataset, batch_size: int, shuffle: bool = True):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        
        self.num_batches = math.ceil(len(dataset) / batch_size)
        print(f"  [INIT] Configured DataLoader: Batch Size = {batch_size} | Total Batches = {self.num_batches}")

    def __iter__(self):
        """Yields perfectly constructed Batches to the GPU."""
        # Simulated shuffling logic
        indices = list(range(len(self.dataset)))
        if self.shuffle:
            import random
            random.seed(42)
            random.shuffle(indices)
            
        # Group single items into Batches!
        for i in range(0, len(self.dataset), self.batch_size):
            batch_indices = indices[i:i+self.batch_size]
            
            batch_data = []
            batch_labels = []
            
            # The DataLoader calls Dataset.__getitem__ for every item in the batch
            for idx in batch_indices:
                item = self.dataset[idx]
                batch_data.append(item["data"])
                batch_labels.append(item["label"])
                
            # Yield the Batch to the Training Loop!
            yield {"batch_data": batch_data, "batch_labels": batch_labels}


# ==============================================================================
# 4. THE BUSINESS LOGIC (THE TRAINING LOOP)
# ==============================================================================
class TrainingSimulator:
    
    def execute_perfect_training_loop(self):
        print("\n  [ARCHITECTURE] Building the Data Pipeline...")
        # 1. Instantiate the Dataset (Pointers to the hard drive)
        dataset = SimulatedDataset(total_samples=1000)
        
        # 2. Instantiate the DataLoader (The Batching Engine)
        dataloader = SimulatedDataLoader(dataset, batch_size=256, shuffle=True)
        
        print("\n  [EXECUTION] Starting PyTorch Training Loop...")
        epochs = 2
        
        for epoch in range(epochs):
            print(f"\n  === EPOCH {epoch+1} ===")
            
            # The DataLoader physically executes here!
            for batch_idx, batch in enumerate(dataloader):
                
                # 1. Move Data to GPU (Simulated)
                # data = batch['batch_data'].to('cuda')
                current_batch_size = len(batch['batch_data'])
                
                # 2. Zero Gradients
                # optimizer.zero_grad()
                
                # 3. Forward Pass
                # predictions = model(data)
                
                # 4. Calculate Loss
                # loss = loss_function(predictions, labels)
                
                # 5. Backward Pass (Calculus)
                # loss.backward()
                
                # 6. Optimizer Step
                # optimizer.step()
                
                print(f"    -> Processed Batch {batch_idx+1}/{dataloader.num_batches} | Size: {current_batch_size} items | Gradients Updated.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_dataloaders():
    section_header("Deep Learning: DataLoaders & Training Loops")
    
    sim = TrainingSimulator()
    sim.execute_perfect_training_loop()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By architecting a `Dataset` and `DataLoader`, the Deep Learning ")
    print("  Engineer mathematically bypassed RAM limits. The DataLoader ")
    print("  dynamically stitched single images from the hard drive into ")
    print("  Batches of 256, streaming them directly into the Training Loop ")
    print("  with an O(1) memory footprint.")


def run_all_labs():
    demonstrate_dataloaders()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural purpose of the `__getitem__` method in a PyTorch Dataset class?"
   Senior Answer: "Lazy Evaluation / Just-In-Time Loading. If a dataset contains $500,000$ high-resolution images, you physically cannot load them into RAM in the `__init__` method. The `__getitem__(self, idx)` method acts as a mathematical pointer. It contains the logic to open the Hard Drive, read the exact image at `idx`, convert it to a Tensor, and return it. It is called lazily by the DataLoader *only* when that specific image is required for the current training batch, guaranteeing that RAM usage remains strictly capped at the Batch Size."

2. Interviewer: "Why do we mathematically enforce `shuffle=True` in the Training DataLoader, but `shuffle=False` in the Validation DataLoader?"
   Senior Answer: "Preventing Gradient Oscillation via I.I.D (Independent and Identically Distributed). If your dataset is sorted (e.g., all Cats first, then all Dogs), the GPU will receive $1,000$ Cats in a row. The Calculus Gradients will drastically update the weights to solely recognize Cats. Then it receives $1,000$ Dogs, and the Gradients violently swing the other way, destroying the Cat weights. This causes catastrophic oscillation. `shuffle=True` mathematically mixes the classes in every batch, smoothing the Calculus descent. For the Validation DataLoader, we do not calculate gradients (`torch.no_grad()`), we only calculate Accuracy. Accuracy is mathematically independent of order, so shuffling is a waste of CPU cycles."

3. Interviewer: "Explain exactly how `num_workers=4` in a PyTorch DataLoader interacts with the Python GIL (Global Interpreter Lock)."
   Senior Answer: "Multi-Processing Bypass. The Python GIL physically prevents multiple threads from executing Python bytecode simultaneously. If a DataLoader needs to load $64$ images, resize them, and apply data augmentations (rotations/crops), a single Python thread will bottleneck the massive GPU, starving it of data. By setting `num_workers=4`, PyTorch uses the `multiprocessing` library to physically spawn $4$ completely independent Python Processes (with their own RAM and their own GILs). These workers mathematically pre-fetch and augment the next batches on $4$ CPU cores simultaneously, queuing them up so the GPU experiences $0\\%$ idle time."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Deep Learning (PyTorch Basics) Completed.")
