# Config Resolution Report (D6–D9, D13) — `nrx-bounded`

Tài liệu này đối soát và chốt giá trị thực tế của các tham số then chốt giữa văn bản Luận văn, mã nguồn notebook Colab và trọng số checkpoint thực nghiệm (`weight_proposed_model_64_QAM`, `neural_receiver_weights`). Đây là **Single Source of Truth** làm cơ sở cấu hình cho `config/config.yaml`.

---

## 1. Bảng đối soát tổng hợp (Conflict Resolution Table)

| ID | Tham số | Giá trị trong Luận văn | Giá trị trong Code / Notebook | Trọng số Checkpoint thực tế | Quyết định chốt | Cơ sở kỹ thuật & Lý do |
|---|---|---|---|---|---|---|
| **D6** | **Kiến trúc mạng (Proposed)**<br>- `d_model`<br>- Số đầu chú ý (`nhead`)<br>- Số khối chú ý (`num_layers`)<br>- Feedforward dim (`d_ff`)<br>- Dropout | Luận văn ghi 64 hoặc 128;<br>N = 4 hoặc 6 khối | `d_model = 128`<br>`nhead = 4`<br>`num_layers = 6`<br>`dim_feedforward = 256`<br>`dropout = 0.1` | `input_proj`: `[128, 12]`<br>`axial_layers`: 6 khối (`0..5`)<br>`freq_attn/time_attn`: 128<br>`ffn`: `128 -> 256 -> 128` | **`d_model = 128`**<br>**`nhead = 4`**<br>**`num_layers = 6`**<br>**`d_ff = 256`**<br>**`dropout = 0.1`** | Khớp 100% cấu trúc checkpoint đã huấn luyện hội tụ 100,000 steps cho 64-QAM. Model 6 khối cho dung lượng biểu diễn tối ưu trên lưới OFDM. |
| **D6_CNN** | **Kiến trúc mạng Baseline (CNN)**<br>- Số kênh conv<br>- Số khối ResBlock | Luận văn ghi 4 khối | `num_conv_channels = 128`<br>`num_blocks = 11` (hoặc 4 ở bản rút gọn) | `_input_conv`: `[128, 5, 3, 3]`<br>`_res_block`: 11 khối trong checkpoint hoàn chỉnh | **`num_conv_channels = 128`**<br>**`num_blocks = 11`** (hỗ trợ eval)<br>**`num_blocks = 4`** (lightweight) | Giữ 11 khối tương thích checkpoint `weights_cnn` của notebook so sánh, đồng thời hỗ trợ tham số hóa qua config. |
| **D7** | **Lưới tài nguyên & FFT**<br>- Số ký hiệu OFDM ($T$)<br>- Kích thước FFT ($F = N_{FFT}$)<br>- Khoảng cách sóng mang (SCS)<br>- Guard subcarriers<br>- DC Null<br>- Số sóng mang khả dụng | $F = 72$ hoặc $128$;<br>$T = 14$ | `num_ofdm_symbols = 14`<br>`fft_size = 128`<br>`scs = 30e3` Hz<br>`guard = [5, 6]`<br>`dc_null = True` | `pos_encoder_2d.time_embed`: `[1, 14, 1, 128]`<br>`pos_encoder_2d.freq_embed`: `[1, 1, 128, 128]` | **$T = 14$**<br>**$F = 128$**<br>**SCS = 30 kHz**<br>**Guard = [5, 6]**<br>**DC Null = 1**<br>**Khả dụng = 116** | Khớp hoàn toàn tensor positional embedding 2D trong checkpoint. 116 subcarriers dữ liệu + pilot. |
| **D8** | **Kênh đầu vào & thứ tự**<br>- Số kênh vào ($C_{in}$)<br>- Danh sách các kênh | Luận văn ghi 6 hoặc 12 kênh | 12 kênh ghép nối (`torch.cat`) | `input_proj.weight`: `[128, 12]` | **12 kênh ghép nối** (Proposed)<br>**5 kênh ghép nối** (CNN) | Checkpoint yêu cầu chính xác 12 kênh đầu vào. Chi tiết thứ tự xem mục 2. |
| **D9** | **Trải trễ kênh (Delay Spread)**<br>- CDL-A<br>- CDL-B<br>- CDL-C | Luận văn ghi $10^{-7}$ s (100 ns) vs 30–300 ns | `delay_spread = 100e-9` (mặc định)<br>`selected_delay = 300e-9` (fallback) | Khớp cấu hình kênh 3GPP TR 38.901 | **CDL-A: 30 ns** (`30e-9` s)<br>**CDL-B: 100 ns** (`100e-9` s)<br>**CDL-C: 300 ns** (`300e-9` s) | Phản ánh đúng 3 mức độ chọn lọc tần số thực tế: CDL-A (trải trễ ngắn), CDL-B (trung bình), CDL-C (trải trễ dài 300 ns gây suy giảm chọn lọc tần số mạnh). |
| **D13** | **Huấn luyện & SNR**<br>- Optimizer<br>- Learning rate ($\eta$)<br>- Weight decay<br>- Dải $E_b/N_0$ train<br>- Batch size / Accumulation | Luận văn ghi $10^{-3}$ vs $10^{-4}$;<br>Dải SNR cố định vs động | `AdamW`<br>`lr = 1e-4`<br>`weight_decay = 1e-4`<br>`ebno_db_min ≈ 8.8 dB`<br>`ebno_db_max ≈ 22.0 dB`<br>`batch = 16`, `accum = 8` | Checkpoint train 100k iters với AdamW lr 1e-4 | **AdamW**<br>**$	ext{lr} = 10^{-4}$**<br>**$	ext{wd} = 10^{-4}$**<br>**Batch = 16 (Accum 8 -> 128)**<br>**Dải $E_b/N_0$: 0 dB đến 20 dB** (hoặc [8.8, 22.0] dB theo Shannon) | Tránh phân kỳ gradient khi train Transformer/Axial Attention. Dải Eb/N0 động bao phủ toàn bộ vùng thác lỗi (waterfall region) của 64-QAM rate 0.9. |

---

## 2. Đặc tả chi tiết 12 kênh đầu vào cho Proposed Neural Receiver (D8)

Thứ tự 12 kênh ghép nối trên chiều Channel ($C_{in} = 12$) của tensor lưới tài nguyên $(B, 12, T, F)$:

| Kênh Index | Ký hiệu trong Code | Định dạng | Miêu tả vật lý |
|---|---|---|---|
| **0** | `y_real[:, 0:1]` | Real (float32) | Phần thực tín hiệu sau DFT tại Anten thu Rx 0 |
| **1** | `y_real[:, 1:2]` | Real (float32) | Phần thực tín hiệu sau DFT tại Anten thu Rx 1 |
| **2** | `y_imag[:, 0:1]` | Real (float32) | Phần ảo tín hiệu sau DFT tại Anten thu Rx 0 |
| **3** | `y_imag[:, 1:2]` | Real (float32) | Phần ảo tín hiệu sau DFT tại Anten thu Rx 1 |
| **4** | `h_ls_real[:, 0:1]` | Real (float32) | Phần thực ước lượng kênh Least-Squares (LS) Anten Rx 0 |
| **5** | `h_ls_real[:, 1:2]` | Real (float32) | Phần thực ước lượng kênh Least-Squares (LS) Anten Rx 1 |
| **6** | `h_ls_imag[:, 0:1]` | Real (float32) | Phần ảo ước lượng kênh Least-Squares (LS) Anten Rx 0 |
| **7** | `h_ls_imag[:, 1:2]` | Real (float32) | Phần ảo ước lượng kênh Least-Squares (LS) Anten Rx 1 |
| **8** | `x_lmmse_real` | Real (float32) | Phần thực ký hiệu QAM cân bằng mềm giải tích LMMSE |
| **9** | `x_lmmse_imag` | Real (float32) | Phần ảo ký hiệu QAM cân bằng mềm giải tích LMMSE |
| **10** | `no_log` | Real (float32) | Phương sai tạp âm $\log_{10}(N_0)$ broadcast trên toàn lưới $(T 	imes F)$ |
| **11** | `pilot_mask` | Binary (0.0/1.0) | Mặt nạ vị trí pilot (1.0 tại ký hiệu OFDM thứ 2 và 11; 0.0 tại các vị trí data) |

> **Ghi chú**: Đối với Baseline CNN ResNet, số kênh đầu vào là **5 kênh**: `[y_real_0, y_real_1, y_imag_0, y_imag_1, no_log]`.

---

## 3. Kết luận và Hướng dẫn cho Task 5 (`config/config.yaml`)

Toàn bộ tham số trong file `config/config.yaml` sẽ lấy trực tiếp từ cột **Quyết định chốt** của bảng trên, phân thành các block:
- `phy`: tần số sóng mang 3.5 GHz, SCS 30 kHz, FFT 128, OFDM symbols 14, guards [5, 6], DC null true, QAM 64 (6 bits), coderate 0.9.
- `channel`: CDL-A (30 ns), CDL-B (100 ns), CDL-C (300 ns), speed [0.0, 50.0] m/s.
- `model_proposed`: d_model 128, nhead 4, num_layers 6, d_ff 256, dropout 0.1, in_channels 12.
- `model_cnn`: conv_channels 128, num_blocks 11, in_channels 5.
- `training`: lr 1e-4, wd 1e-4, batch_size 16, accumulation_steps 8, iterations 100000, seed 42.
