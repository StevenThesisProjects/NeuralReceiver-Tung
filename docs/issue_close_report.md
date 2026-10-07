# BÁO CÁO THIẾT KẾ HẠ TẦNG VÀ CHUẨN HÓA CẤU HÌNH ĐƠN NGUỒN (SYSTEM INFRASTRUCTURE & ARCHITECTURE REPORT) — nrx-bounded

**Tác giả:** Vương Thanh Tùng  
**Đề tài:** Nghiên Cứu và Triển Khai Bộ Thu Neural Receiver Cho Hệ Thống Vô Tuyến Thế Hệ Mới (6G)  
**Trạng thái:** Hoàn tất thiết kế hạ tầng kỹ thuật & nghiệm thu toàn diện (Technical Infrastructure Verification Passed)  
**Ngày hoàn thành:** 2026-10-06  

---

## 1. Tổng Quan Thiết Kế & Lịch Sử Triển Khai Hệ Thống

Để đảm bảo tính tái lập (reproducibility), khả năng mở rộng và độ tin cậy khoa học của toàn bộ luận văn, repository `nrx-bounded` được xây dựng với cấu trúc module hóa chuẩn công nghiệp và cơ chế cấu hình đơn nguồn (Single Source of Truth - writing-as-code). 

Toàn bộ quá trình triển khai mã nguồn và tài liệu kỹ thuật được quản lý phiên bản qua Git tại `Working/nrx-bounded` theo chuẩn Conventional Commits:

| STT | Mã Commit | Thông điệp Commit | Mục tiêu kỹ thuật |
|:---:|:---:|:---|:---|
| 1 | `5286795` | `feat(infra): initialize git repository and add .gitignore` | Khởi tạo repo & thiết lập `.gitignore` loại trừ file tạm |
| 2 | `e692503` | `feat(infra): import original colab notebooks into notebooks/ directory` | Phân loại và cấu trúc các notebook thực nghiệm |
| 3 | `e85033f` | `fix(infra): remove duplicated root notebook and cleanup checkpoints` | Dọn dẹp thư mục gốc và chuẩn hóa vị trí checkpoints |
| 4 | `27dfc59` | `fix(infra): remove all residual non-repo files from Working directory` | Chuẩn hóa môi trường làm việc sạch |
| 5 | `4cbd635` | `feat(infra): setup modular directory structure per Roadmap §24` | Thiết lập cây thư mục module hóa hoàn chỉnh |
| 6 | `357e6a7` | `docs(infra): add task 2 summary report` | Ghi nhận cấu trúc phân cấp module |
| 7 | `c47881f` | `feat(infra): record verified environment versions in requirements.txt and environment.md` | Khóa phiên bản môi trường & phụ thuộc kỹ thuật |
| 8 | `af12c9b` | `docs(infra): add task 3 summary report` | Ghi nhận thông số môi trường thực tế |
| 9 | `07840ea` | `docs(infra): resolve config conflicts D6-D9, D13 in docs/config_resolution.md` | Chuẩn hóa toàn bộ tham số kỹ thuật D6–D9, D13 |
| 10 | `7555419` | `docs(infra): add task 4 summary report` | Báo cáo đối soát kiến trúc kỹ thuật |
| 11 | `87d4708` | `feat(infra): add single-source config/config.yaml and src/config.py loader` | Xây dựng cấu hình đơn nguồn `config.yaml` và loader |
| 12 | `d9ca326` | `docs(infra): add task 5 summary report` | Ghi nhận tích hợp loader cấu hình tự động |
| 13 | `a6794e4` | `feat(infra): implement set_all_seeds for NumPy, PyTorch, and TensorFlow` | Cài đặt hàm `set_all_seeds()` đảm bảo tính tất định |
| 14 | `4197801` | `docs(infra): add task 6 summary report` | Kiểm chứng tính tất định hạt giống ngẫu nhiên |
| 15 | `7818f7a` | `feat(infra): add pytest configuration and automated smoke tests` | Xây dựng khung kiểm thử tự động với `pytest` |
| 16 | `96c6984` | `docs(infra): add task 7 summary report` | Nghiệm thu độ phủ kiểm thử tự động |
| 17 | `d7f1e40` | `refactor(notebook): wire single-source config into main notebook` | Loại bỏ hoàn toàn hard-code trong notebook thực nghiệm |

---

## 2. Danh Mục Kết Quả Kỹ Thuật (Deliverables)

1. **Trọng số huấn luyện đối soát thực tế**:
   - Checkpoint gốc: `Storage/weight_proposed_model_64_QAM` (114 tensor keys, kiểm chứng trực tiếp hình dạng trọng số và kiến trúc mạng).
2. **Cấu hình đơn nguồn duy nhất (Single Source of Truth)**:
   - File cấu hình trung tâm: [`config/config.yaml`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/config/config.yaml)
   - Module nạp cấu hình: [`src/config.py`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/src/config.py) (tự động nhận diện thư mục gốc dự án, hỗ trợ fallback an toàn).
3. **Báo cáo chuẩn hóa tham số kỹ thuật**:
   - Tài liệu: [`docs/config_resolution.md`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/docs/config_resolution.md) đối soát chi tiết giữa bản thảo lý thuyết, mã nguồn thực tế và checkpoint thực nghiệm.
4. **Bộ kiểm thử tự động (Automated Smoke Test Suite)**:
   - Cấu hình: [`pytest.ini`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/pytest.ini)
   - Bộ test: [`tests/test_smoke.py`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/tests/test_smoke.py) xác thực việc nhập các thư viện nền tảng, tính toàn vẹn của config, và tính tất định của seed ngẫu nhiên.
5. **Notebooks thực nghiệm chuẩn hóa**:
   - Main Notebook: [`notebooks/Single/Neural_Receiver_real6G_64QAM_0_9_10ms_C_128_(collab-lretrainlatest).ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/notebooks/Single/Neural_Receiver_real6G_64QAM_0_9_10ms_C_128_(collab-lretrainlatest).ipynb)
   - Demo Pipeline: [`demo/nrx_main_pipeline.ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/demo/nrx_main_pipeline.ipynb)
   - Compare Notebook: [`notebooks/Compare/Neural_Receiver_compare_debugged(collab).ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/notebooks/Compare/Neural_Receiver_compare_debugged(collab).ipynb)
   - Toàn bộ tham số được nạp tự động thông qua `cfg = load_config()`, xử lý sạch sẽ đường dẫn import, loại bỏ hoàn toàn các hằng số phân tán.

---

## 3. Tài Nguyên Tính Toán & Đo Đạc Thực Nghiệm

- **Thời gian triển khai & chuẩn hóa hạ tầng**: 1.5 ngày công kỹ thuật.
- **Tài nguyên phần cứng sử dụng**:
  - Máy trạm cục bộ: Phân tích checkpoint trọng số, tái cấu trúc mã nguồn `src/`, xây dựng pipeline kiểm thử tự động với `pytest`.
  - Môi trường GPU Colab T4: Kiểm chứng tính ổn định của `set_all_seeds()` trên CUDA/cuDNN, đo đạc độ trễ suy luận và FLOPs của các mô hình neural receiver qua thư viện `thop`.

---

## 4. Các Quyết Định Thiết Kế & Chuẩn Hóa Kiến Trúc Kỹ Thuật

Qua quá trình đối soát chặt chẽ giữa mã nguồn mô phỏng, checkpoint đã huấn luyện và lý thuyết hệ thống, các tham số và cấu trúc kiến trúc đã được chuẩn hóa dứt khoát như sau:

### D6: Cấu trúc mô hình Proposed Axial Attention & CNN-ResNet
- **Mô hình đề xuất (Proposed Axial Attention)**:
  - Chiều biểu diễn đặc trưng: $d_{model} = 128$.
  - Số lớp chú ý trục tuần tự: $N = 6$ khối đối với điều chế **64-QAM**, và $N = 3$ khối đối với điều chế **QPSK (4-QAM)**.
  - Mỗi khối chú ý trục bao gồm 2 cơ chế Multi-Head Attention độc lập (chiều thời gian và chiều tần số) với `nhead = 4`, cùng mạng FFN có chiều ẩn trung gian $d_{ff} = 256$ ($2 \times d_{model}$).
- **Mô hình đối chuẩn (Baseline CNN-ResNet)**:
  - Số khối ResNet: $N = 11$ khối đối với điều chế **64-QAM**, và $N = 4$ khối đối với điều chế **QPSK (4-QAM)**.

### D7: Lưới Thời Gian - Tần Số và Kích Thước FFT
- Chuẩn hóa kích thước FFT: $F = 128$ sóng mang con (loại bỏ hoàn toàn các giá trị không phù hợp trong các bản thảo cũ như 72 subcarriers).
- Số ký tự OFDM trên một khung truyền: $T = 14$ ký tự OFDM.
- Tổng số subcarrier hữu ích sau khi loại bỏ 11 subcarrier bảo vệ (`[5, 6]`) và 1 DC subcarrier là **116 subcarriers**.

### D8: Số Kênh Đầu Vào và Định Dạng Đặc Trưng
- **Proposed Axial Attention**: Nhận đúng **12 kênh đặc trưng đầu vào** (`input_proj.weight` shape `[128, 12]`):
  - Kênh 0–1: Tín hiệu thu phần thực trên 2 anten trạm gốc (`y_real[0, 1]`)
  - Kênh 2–3: Tín hiệu thu phần ảo trên 2 anten trạm gốc (`y_imag[0, 1]`)
  - Kênh 4–5: Ước lượng kênh truyền LS phần thực (`h_ls_real[0, 1]`)
  - Kênh 6–7: Ước lượng kênh truyền LS phần ảo (`h_ls_imag[0, 1]`)
  - Kênh 8–9: Tín hiệu san bằng sơ bộ LMMSE phần thực & ảo (`x_lmmse_real`, `x_lmmse_imag`)
  - Kênh 10: Logarit mật độ phổ công suất nhiễu $\log_{10}(N_0)$ mở rộng 2D
  - Kênh 11: Mặt nạ Pilot (Pilot mask, giá trị 1.0 tại các vị trí ký tự pilot 2 và 11)
- **CNN-ResNet**: Nhận **5 kênh đặc trưng đầu vào** tương ứng với các thành phần biểu diễn cơ sở.

### D9: Độ Trải Trễ Mô Hình Kênh CDL (Delay Spread)
- Xác lập giá trị vô hướng cố định: `delay_spread = 1.0e-07` ($100\text{ ns}$), đồng nhất tuyệt đối giữa mô hình kênh CDL Sionna và các kịch bản mô phỏng kiểm thử. Loại bỏ các định dạng từ điển dư thừa.

### D13: Siêu Tham Số Huấn Luyện & Dải Tín Hiệu
- Tối ưu hóa: AdamW với tốc độ học $lr = 10^{-3}$, weight decay $= 10^{-4}$.
- Kích thước batch hiệu dụng: 128 (batch size 16 kết hợp gradient accumulation 8 bước).
- Dải $E_b/N_0$ kiểm thử và đánh giá: $0.0\text{ dB} \rightarrow 20.0\text{ dB}$.

---

## 5. Kết Luận & Kiểm Thử Nghiệm Thu Hệ Thống

Hạ tầng kỹ thuật của đề tài đã đạt độ hoàn thiện cao, sẵn sàng phục vụ cho các bước huấn luyện chuyên sâu và thực nghiệm so sánh:

- ✅ **Kiểm thử tự động hoàn toàn**: Bộ test suite chạy bằng `pytest` đạt 100% tỷ lệ pass trên cả máy trạm cục bộ và Google Colab.
- ✅ **Cấu hình đơn nguồn minh bạch**: File `config/config.yaml` làm chủ toàn bộ thông số mô phỏng và kiến trúc mô hình, loại bỏ nguy cơ lệch cấu hình giữa các notebook.
- ✅ **Mã nguồn module hóa sạch sẽ**: Các gói `src/sim`, `src/models`, `src/train`, `src/eval`, `src/utils` được tổ chức khoa học, tách bạch giữa giao diện thực nghiệm và logic toán học.
