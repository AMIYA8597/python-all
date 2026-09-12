import math

# Try to import torch to demonstrate the math of LoRA
try:
    import torch
    import torch.nn as nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("PyTorch is not installed. This script requires PyTorch to run the math simulation.")

if HAS_TORCH:
    class MockLinearWithLoRA(nn.Module):
        """
        A simulated Linear layer that implements the LoRA (Low-Rank Adaptation) mechanism.
        Formula: output = x * W_base + x * (A * B) * scaling
        """
        def __init__(self, in_features, out_features, rank=4, lora_alpha=8):
            super(MockLinearWithLoRA, self).__init__()
            
            # 1. The original base model weights (Frozen)
            self.base_layer = nn.Linear(in_features, out_features, bias=False)
            # Freeze base weights
            self.base_layer.weight.requires_grad = False
            
            # 2. LoRA Matrices A and B
            # A projects down to the low rank 'r'
            self.lora_A = nn.Parameter(torch.empty(in_features, rank))
            # B projects back up to 'out_features'
            self.lora_B = nn.Parameter(torch.empty(rank, out_features))
            
            # Scaling factor (standard practice in LoRA)
            self.scaling = lora_alpha / rank
            
            self.reset_parameters()

        def reset_parameters(self):
            # Normal initialization for A
            nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
            # Zero initialization for B (so initially, the adapter does nothing)
            nn.init.zeros_(self.lora_B)

        def forward(self, x):
            # Standard forward pass with frozen weights
            base_output = self.base_layer(x)
            
            # LoRA forward pass: x -> A -> B
            lora_output = (x @ self.lora_A) @ self.lora_B
            
            # Add them together with scaling
            return base_output + (lora_output * self.scaling)

    def main():
        print("--- LoRA (Low-Rank Adaptation) Concept Demonstration ---")
        
        in_features = 1024
        out_features = 1024
        rank = 8 # Low rank (r)
        
        # 1. Standard Linear Layer (Full Fine-tuning scenario)
        standard_layer = nn.Linear(in_features, out_features, bias=False)
        total_params_standard = sum(p.numel() for p in standard_layer.parameters())
        print(f"\nStandard Layer Total Parameters (Requires Update): {total_params_standard:,}")
        
        # 2. LoRA Layer
        lora_layer = MockLinearWithLoRA(in_features, out_features, rank=rank)
        
        # Count trainable parameters in LoRA
        trainable_params_lora = sum(p.numel() for p in lora_layer.parameters() if p.requires_grad)
        total_params_lora = sum(p.numel() for p in lora_layer.parameters())
        
        print(f"\nLoRA Layer Total Parameters: {total_params_lora:,}")
        print(f"LoRA Trainable Parameters (Matrix A & B): {trainable_params_lora:,}")
        
        # Calculate reduction
        reduction = (trainable_params_lora / total_params_standard) * 100
        print(f"Percentage of trainable parameters compared to full tuning: {reduction:.2f}%")
        
        # 3. Simulate Forward Pass
        dummy_input = torch.randn(1, in_features)
        output = lora_layer(dummy_input)
        print(f"\nForward Pass Successful. Output shape: {output.shape}")
        
        print("\nSummary:")
        print("In full fine-tuning, the optimizer tracks 1,048,576 parameters.")
        print("With LoRA (rank=8), the original 1M parameters are frozen, and the optimizer only updates 16,384 parameters.")
        print("This leads to massive GPU memory savings!")

if __name__ == "__main__":
    if HAS_TORCH:
        main()
