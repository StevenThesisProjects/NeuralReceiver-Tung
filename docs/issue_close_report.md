# BÁO CÁO ĐÓNG ISSUE #2
**Tên Issue**: `[S1][INFRA] Thiết lập repo nrx-bounded và config.yaml đơn nguồn`  
**Mã Issue**: ISSUE-001 (#2)  
**Sprint**: S1 (05/10/2026 → 18/10/2026) — Milestone: Reproduce, Verify, Literature  
**Mức độ ưu tiên**: P0 — Critical Path  
**Người thực hiện**: Agent A (Vuong Thanh Tung)  
**Ngày hoàn thành**: 2026-10-06  

---

## 1. Link Commit / PR & Lịch sử triển khai

Toàn bộ quá trình thực thi từ Task 1 đến Task 8 được kiểm soát phiên bản qua Git tại repository `Working/nrx-bounded` (đồng bộ song song sang `Directory/nrx-bounded`). Lịch sử commit theo chuẩn Conventional Commits:

| STT | Mã Commit | Thông điệp Commit | Nhiệm vụ tương ứng |
|:---:|:---:|:---|:---|
| 1 | `5286795` | `feat(infra): initialize git repository and add .gitignore` | Task 1: Khởi tạo repo & .gitignore |
| 2 | `e692503` | `feat(infra): import original colab notebooks into notebooks/ directory` | Task 1: Nhập 5 Colab notebook |
| 3 | `e85033f` | `fix(infra): remove duplicated root notebook and cleanup checkpoints` | Task 1: Dọn dẹp root & checkpoints |
| 4 | `27dfc59` | `fix(infra): remove all residual non-repo files from Working directory` | Task 1: Vệ sinh môi trường Working |
| 5 | `4cbd635` | `feat(infra): setup modular directory structure per Roadmap §24` | Task 2: Dựng cây thư mục Roadmap §24 |
| 6 | `357e6a7` | `docs(infra): add task 2 summary report` | Task 2: Báo cáo Task 2 |
| 7 | `c47881f` | `feat(infra): record verified environment versions in requirements.txt and environment.md` | Task 3: Khóa môi trường & phụ thuộc |
| 8 | `af12c9b` | `docs(infra): add task 3 summary report` | Task 3: Báo cáo Task 3 |
| 9 | `07840ea` | `docs(infra): resolve config conflicts D6-D9, D13 in docs/config_resolution.md` | Task 4: Giải quyết mâu thuẫn D6–D9, D13 |
| 10 | `7555419` | `docs(infra): add task 4 summary report` | Task 4: Báo cáo Task 4 |
| 11 | `87d4708` | `feat(infra): add single-source config/config.yaml and src/config.py loader` | Task 5: Cấu hình đơn nguồn `config.yaml` |
| 12 | `d9ca326` | `docs(infra): add task 5 summary report` | Task 5: Báo cáo Task 5 |
| 13 | `a6794e4` | `feat(infra): implement set_all_seeds for NumPy, PyTorch, and TensorFlow` | Task 6: Hàm `set_all_seeds()` tái lập |
| 14 | `4197801` | `docs(infra): add task 6 summary report` | Task 6: Báo cáo Task 6 |
| 15 | `7818f7a` | `feat(infra): add pytest configuration and automated smoke tests` | Task 7: Khung kiểm thử `pytest` tự động |
| 16 | `96c6984` | `docs(infra): add task 7 summary report` | Task 7: Báo cáo Task 7 |
| 17 | `d7f1e40` | `refactor(notebook): wire single-source config into main notebook to satisfy DoD #3` | Task 8: Loại bỏ hard-code & lập báo cáo đóng issue |

---

## 2. Link Kết quả & Deliverables

1. **Checkpoint gốc đã đối soát hình dạng trọng số**:
   - Đường dẫn: `Storage/weight_proposed_model_64_QAM` (114 keys, kích thước tensor xác thực trực tiếp cấu trúc mạng).
2. **Cấu hình đơn nguồn duy nhất (Single Source of Truth - writing-as-code)**:
   - File cấu hình: [`config/config.yaml`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/config/config.yaml)
   - Module loader: [`src/config.py`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/src/config.py) (tự động phát hiện project root, fallback an toàn).
3. **Báo cáo giải quyết mâu thuẫn thông số**:
   - Tài liệu: [`docs/config_resolution.md`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/docs/config_resolution.md) với bảng so chiếu 3 cột: *Giá trị trong luận văn*, *Giá trị trong code*, và *Quyết định kỹ thuật*.
4. **Bộ kiểm thử tự động (Automated Smoke Test Suite)**:
   - Cấu hình: [`pytest.ini`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/pytest.ini)
   - Kiểm thử: [`tests/test_smoke.py`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/tests/test_smoke.py) xác thực imports, tính toàn vẹn của config, và tính tất định của seed. Kết quả: **3/3 passed (100%)**.
5. **Notebooks chính đã refactor**:
   - Main Notebook: [`notebooks/Single/Neural_Receiver_real6G_64QAM_0_9_10ms_C_128_(collab-lretrainlatest).ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/notebooks/Single/Neural_Receiver_real6G_64QAM_0_9_10ms_C_128_(collab-lretrainlatest).ipynb)
   - Demo Pipeline: [`demo/nrx_main_pipeline.ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/demo/nrx_main_pipeline.ipynb)
   - Compare Notebook: [`notebooks/Compare/Neural_Receiver_compare_debugged(collab).ipynb`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/notebooks/Compare/Neural_Receiver_compare_debugged(collab).ipynb)
   - Toàn bộ tham số được nạp tự động qua `cfg = load_config()`, xử lý `sys.path` tại cell đầu tiên, sạch sẽ hoàn toàn không còn hard-code.

---

## 3. Thời gian thực tế và GPU-giờ đã sử dụng

- **Ước lượng ban đầu (trong Issue #2)**: 1.5 ngày công.
- **Thời gian thực tế thực hiện**: **1.5 ngày công** (hoàn thành đúng hạn vào 06/10/2026, trước hạn chót 07/10/2026).
- **Tài nguyên tính toán / GPU-giờ**:
  - Máy cục bộ: CPU & RAM phục vụ phân tích checkpoint, xây dựng module `src/`, chạy smoke test với pytest.
  - GPU-giờ Colab T4: **0.2 GPU-giờ** (chạy forward pass kiểm tra khả năng tương thích của `set_all_seeds()` trên CUDA/cuDNN và đo đạc FLOPs/thời gian trễ qua module `thop`).

---

## 4. Điều bất ngờ & Quyết định kỹ thuật cần Cố vấn xem xét

Trong quá trình đối soát giữa bản thảo luận văn, mã nguồn trong các notebook và trọng số checkpoint thực tế (`weight_proposed_model_64_QAM`), đội ngũ kỹ thuật đã phát hiện và thống nhất giải quyết các mâu thuẫn trọng yếu sau:

### D6: Cấu trúc mô hình Proposed Axial Attention
- *Bất ngờ / Mâu thuẫn*: Bản thảo luận văn mô tả không đồng nhất giữa $d_{model} = 64$ và $d_{model} = 128$; số lớp biến thiên giữa 4 và 6 khối.
- *Quyết định giải quyết*: Đối soát checkpoint khẳng định chính xác:
  - `input_proj.weight`: shape `[128, 12]` $\rightarrow$ $d_{model} = 128$.
  - `axial_layers`: gồm 6 khối tuần tự (`axial_layers.0` đến `axial_layers.5`).
  - Mỗi khối chứa 2 bộ Multi-head Attention (tần số và thời gian) với `nhead = 4`, FFN intermediate dimension = 256 ($2 \times d_{model}$).

### D7: Lưới thời gian - tần số và kích thước FFT
- *Bất ngờ / Mâu thuẫn*: Một số đoạn ghi nhận lưới 72 sóng mang con.
- *Quyết định giải quyết*: Checkpoint khẳng định kích thước lưới là $T = 14$ ký tự OFDM và $F = 128$ sóng mang con (`pos_encoder_2d.time_embed` có shape `[1, 14, 1, 128]`, `freq_embed` có shape `[1, 1, 128, 128]`). Tổng số sóng mang con hữu ích sau khi trừ 11 subcarrier bảo vệ (`[5, 6]`) và 1 DC null là 116 sóng mang con.

### D8: Số kênh đầu vào và thứ tự ghép nối (12 kênh)
- *Bất ngờ / Mâu thuẫn*: Mô tả lý thuyết ghi nhận 5 hoặc 6 kênh đầu vào.
- *Quyết định giải quyết*: `input_proj.weight` có kích thước `[128, 12]` chứng minh mô hình thực tế nhận đúng **12 kênh đặc trưng**:
  - Kênh 0–1: Tín hiệu thu phần thực trên 2 anten BS (`y_real[0, 1]`)
  - Kênh 2–3: Tín hiệu thu phần ảo trên 2 anten BS (`y_imag[0, 1]`)
  - Kênh 4–5: Ước lượng kênh LS phần thực (`h_ls_real[0, 1]`)
  - Kênh 6–7: Ước lượng kênh LS phần ảo (`h_ls_imag[0, 1]`)
  - Kênh 8–9: Ký hiệu san bằng mềm LMMSE phần thực & ảo (`x_lmmse_real`, `x_lmmse_imag`)
  - Kênh 10: Logarit phương sai nhiễu $\log_{10}(N_0)$ mở rộng lên lưới 2D
  - Kênh 11: Mặt nạ phi công (Pilot mask, giá trị 1.0 tại ký tự 2 và 11)

### D9: Độ trễ trễ (Delay Spread) mô hình kênh CDL
- *Bất ngờ / Mâu thuẫn*: Code notebook gán cứng 100 ns cho mọi mô hình kênh.
- *Quyết định giải quyết*: Chuẩn hóa theo tiêu chuẩn 3GPP TR 38.901: CDL-A = 30 ns, CDL-B = 100 ns, CDL-C = 300 ns. Trong file cấu hình đơn nguồn đã cấu hình rõ cho từng mô hình với mô hình mặc định là CDL-C (300 ns).

### D13: Siêu tham số huấn luyện & Dải Eb/N0
- *Quyết định giải quyết*: Bộ tối ưu AdamW với $lr = 10^{-4}$, weight decay $= 10^{-4}$, kích thước batch thực tế bằng 128 (batch size 16 kết hợp 8 bước tích lũy gradient `gradient_accumulation_steps = 8`), dải $E_b/N_0$ huấn luyện từ $0.0\text{ dB}$ đến $20.0\text{ dB}$.

---

## 5. Kết luận nghiệm thu Definition of Done (DoD)

- [x] **DoD 1**: Repo chạy `pytest` không lỗi cả trên máy cục bộ và Colab T4 (3/3 smoke tests passed).
- [x] **DoD 2**: Bảng D6–D9, D13 trong `docs/config_resolution.md` đầy đủ 3 cột đối chiếu và quyết định.
- [x] **DoD 3**: Không còn tham số hard-code trong notebook chính; đã wire đơn nguồn từ `config/config.yaml`.
- [x] **DoD 4**: Cấu trúc thư mục khớp Roadmap §24; các module `src/config.py`, `src/utils.py` hoạt động chính xác.
- [x] **DoD 5**: Báo cáo đóng Issue #2 đầy đủ 4 mục theo quy định.
