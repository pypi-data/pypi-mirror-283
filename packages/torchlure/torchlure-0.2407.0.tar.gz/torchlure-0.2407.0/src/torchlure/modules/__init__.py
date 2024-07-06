import einops as ein
import torch
from torch import Tensor, nn
from torchtyping import TensorType


class RMSNorm(nn.Module):
    """
    Implements Root Mean Square Normalization introduced in
    https://arxiv.org/pdf/1910.07467.pdf.

    Reference implementation (used for correctness verfication)
    can be found here:
    https://github.com/facebookresearch/llama/blob/main/llama/model.py

    Args:
        dim (int): embedding size
        eps (float): small value to avoid division by zero. Default: 1e-6
    """

    def __init__(self, dim: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.scale = nn.Parameter(torch.ones(dim))

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x (Tensor): input tensor to normalize

        Returns:
            Tensor: The output tensor after applying RMSNorm.
        """
        # computation is in fp32
        x_fp32 = x.float()
        x_normed = (
            x_fp32 * torch.rsqrt(x_fp32.pow(2).mean(-1, keepdim=True) + self.eps)
        ).type_as(x)
        return x_normed * self.scale


class ReLUKANLayer(nn.Module):
    def __init__(
        self, input_size: int, g: int, k: int, output_size: int, train_ab: bool = True
    ):
        super().__init__()
        self.g, self.k, self.r = g, k, 4 * g * g / ((k + 1) * (k + 1))
        self.input_size, self.output_size = input_size, output_size

        phase_low = torch.arange(-k, g, dtype=torch.float32) / g
        phase_height = phase_low + (k + 1) / g
        self.phase_low = nn.Parameter(
            phase_low.repeat(input_size, 1),
            requires_grad=train_ab,
        )
        self.phase_height = nn.Parameter(
            phase_height.repeat(input_size, 1),
            requires_grad=train_ab,
        )

        self.equal_size_conv = nn.Conv2d(1, output_size, (g + k, input_size))

    def forward(
        self, x: TensorType["B", "input_size"]
    ) -> TensorType["B", "output_size"]:
        x = x.unsqueeze(-1)
        x1 = F.relu(x - self.phase_low)
        x2 = F.relu(self.phase_height - x)
        x = x1 * x2 * self.r
        x = x * x
        x = ein.rearrange(x, "... in gk -> ... 1 gk in")
        x = self.equal_size_conv(x)
        x = ein.rearrange(x, "... out 1 1 -> ... out")
        return x
