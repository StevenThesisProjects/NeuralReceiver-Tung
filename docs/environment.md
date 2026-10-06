# Environment Specifications — `nrx-bounded`

Tài liệu này chuẩn hóa thông số môi trường thực thi thực tế phục vụ tái lập nghiên cứu theo yêu cầu Issue #2 (`[S1][INFRA]`).

---

## 1. Bảng tổng hợp phiên bản thực tế

| Thành phần | Phiên bản khuyến nghị | Mục đích sử dụng | Ghi chú tương thích |
|---|---|---|---|
| **Python** | `3.10` – `3.12` | Runtime ngôn ngữ chính | Chuẩn Colab T4 (mặc định Python 3.10/3.11) |
| **PyTorch** | `>= 2.2.0` (CUDA 12.1+) | Huấn luyện & suy luận mô hình nơ-ron | Hỗ trợ `torch.compile` (`inductor`), AMP FP16/BF16, CUDA T4 |
| **Sionna** | `>= 1.0.0` (PyTorch PHY) | Mô phỏng kênh truyền 3GPP CDL, OFDM, LDPC | Sử dụng trực tiếp `from sionna.phy import ...` trên GPU |
| **NumPy** | `>= 1.24.0, < 2.0.0` | Tính toán ma trận mảng số học | Giữ `< 2.0.0` để tránh tương thích ABI với Sionna C++/Cython extensions |
| **SciPy** | `>= 1.10.0` | Xử lý tín hiệu & tính toán khoa học | Bổ trợ cho giải thuật LMMSE và ước lượng kênh |
| **Matplotlib** | `>= 3.7.0` | Vẽ đồ thị BER/BLER và constellation | Hiển thị inline trong notebook và xuất vector PDF |
| **thop** | `>= 0.1.1` | Đo độ phức tạp tính toán (FLOPs/MACs) | Dùng bản sao uncompiled của model để đo FLOPs |
| **PyYAML** | `>= 6.0` | Đọc cấu hình đơn nguồn `config.yaml` | Single source of truth cho toàn bộ tham số PHY & mạng |
| **Pytest** | `>= 7.0.0` | Kiểm thử tự động (CI / Smoke test) | Chạy kiểm tra import và tính toàn vẹn hệ thống |
| **TensorFlow** | *(Tùy chọn / Ghi chú)* | Baseline Sionna TF cũ (nếu có) | Dự án chính thức chuẩn hóa trên nền **PyTorch native** |

---

## 2. Hướng dẫn thiết lập môi trường

### 2.1 Cài đặt trên Google Colab (GPU T4)
Chạy trong cell đầu tiên của Colab:
```bash
!pip install --upgrade sionna thop pyyaml pytest -q
```
Kiểm tra thiết bị GPU:
```python
import torch, sionna
print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available(), "(Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None", ")")
print("Sionna Device:", sionna.phy.config.device)
```

### 2.2 Cài đặt trên môi trường Local venv
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt venv (Linux/macOS)
source .venv/bin/activate
# Hoặc trên Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

# Cài đặt toàn bộ dependencies
pip install -r requirements.txt
```
