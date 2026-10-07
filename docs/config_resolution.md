# Báo Cáo Chuẩn Hóa Tham Số Kỹ Thuật (System Parameter & Architecture Resolution) — `nrx-bounded`

Tài liệu này tổng hợp quá trình phân tích kỹ thuật, đối soát và chuẩn hóa các tham số then chốt của hệ sinh thái máy thu nơ-ron giữa văn bản Luận văn, mã nguồn thực nghiệm và trọng số checkpoint thực tế (`weight_proposed_model_64_QAM`, `neural_receiver_weights`). Đây là **Single Source of Truth** do tác giả tự xây dựng làm cơ sở thiết lập tệp cấu hình trung tâm `config/config.yaml`.

---

## 1. Bảng đối soát tổng hợp (Conflict Resolution Table)

| ID | Tham số | Giá trị trong Luận văn | Giá trị trong Code / Notebook | Trọng số Checkpoint thực tế | Quyết định chốt | Cơ sở kỹ thuật & Lý do |
|---|---|---|---|---|---|---|
| **D6** | **Kiến trúc mạng (Proposed)**<br>- `d_model`<br>- Số đầu chú ý (`nhead`)<br>- Số khối chú ý (`num_layers`)<br>- Feedforward dim (`d_ff`)<br>- Dropout | Luận văn ghi 64 hoặc 128;<br>N = 4 hoặc 6 khối | `d_model = 128`<br>`nhead = 4`<br>`num_layers = 6`<br>`dim_feedforward = 256`<br>`dropout = 0.1` | `input_proj`: `[128, 12]`<br>`axial_layers`: 6 khối (`0..5`)<br>`freq_attn/time_attn`: 128<br>`ffn`: `128 -> 256 -> 128` | **`d_model = 128`**<br>**`nhead = 4`**<br>**`num_layers = 6`**<br>**`d_ff = 256`**<br>**`dropout = 0.1`** | Khớp 100% cấu trúc checkpoint đã huấn luyện hội tụ 100,000 steps cho 64-QAM. Model 6 khối cho dung lượng biểu diễn tối ưu trên lưới OFDM. |
| **D6_CNN** | **Kiến trúc mạng Baseline (CNN)**<br>- Số kênh conv<br>- Số khối ResBlock | Luận văn ghi 4 khối | `num_conv_channels = 128`<br>`num_blocks = 11` (hoặc 4 ở bản rút gọn) | `_input_conv`: `[128, 5, 3, 3]`<br>`_res_block`: 11 khối trong checkpoint hoàn chỉnh | **`num_conv_channels = 128`**<br>**`num_blocks = 11`** (hỗ trợ eval)<br>**`num_blocks = 4`** (lightweight) | Giữ 11 khối tương thích checkpoint `weights_cnn` của notebook so sánh, đồng thời hỗ trợ tham số hóa qua config. |
| **D7** | **Lưới tài nguyên & FFT**<br>- Số ký hiệu OFDM ($T$)<br>- Kích thước FFT ($F = N_{FFT}$)<br>- Khoảng cách sóng mang (SCS)<br>- Guard subcarriers<br>- DC Null<br>- Số sóng mang khả dụng | $F = 72$ hoặc $128$;<br>$T = 14$ | `num_ofdm_symbols = 14`<br>`fft_size = 128`<br>`scs = 30e3` Hz<br>`guard = [5, 6]`<br>`dc_null = True` | `pos_encoder_2d.time_embed`: `[1, 14, 1, 128]`<br>`pos_encoder_2d.freq_embed`: `[1, 1, 128, 128]` | **$T = 14$**<br>**$F = 128$**<br>**SCS = 30 kHz**<br>**Guard = [5, 6]**<br>**DC Null = 1**<br>**Khả dụng = 116** | Khớp hoàn toàn tensor positional embedding 2D trong checkpoint. 116 subcarriers dữ liệu + pilot. |
| **D8** | **Kênh đầu vào & thứ tự**<br>- Số kênh vào ($C_{in}$)<br>- Danh sách các kênh | Luận văn ghi 6 hoặc 12 kênh | 12 kênh ghép nối (`torch.cat`) | `input_proj.weight`: `[128, 12]` | **12 kênh ghép nối** (Proposed)<br>**5 kênh ghép nối** (CNN) | Checkpoint yêu cầu chính xác 12 kênh đầu vào. Chi tiết thứ tự xem mục 2. |
| **D9** | **Trải trễ kênh (Delay Spread)** | Luận văn ghi $10^{-7}$ s (100 ns) | `delay_spread = 100e-9` (100 ns) | Đồng nhất 100 ns ($10^{-7}$ s) | **`delay_spread = 100e-9`** ($1.0 \times 10^{-7}$ s / 100 ns) | Mã nguồn gốc ở mọi notebook và luận văn đồng nhất sử dụng trải trễ 100 ns. Không áp đặt phân rã bảng CDL-A/B/C (30/100/300 ns) gây sai lệch mô phỏng so với code thực nghiệm gốc. Mô hình kênh chốt: `cdl_model = "C"`. |
| **D13** | **Huấn luyện & SNR**<br>- Optimizer<br>- Learning rate ($\eta$)<br>- Weight decay<br>- Dải $E_b/N_0$ train<br>- Batch size / Accumulation | Luận văn ghi $10^{-3}$ vs $10^{-4}$;<br>Dải SNR cố định vs động | `AdamW`<br>`lr = 1e-4`<br>`weight_decay = 1e-4`<br>`ebno_db_min ≈ 8.8 dB`<br>`ebno_db_max ≈ 22.0 dB`<br>`batch = 16`, `accum = 8` | Checkpoint train 100k iters với AdamW lr 1e-4 | **AdamW**<br>**$\text{lr} = 10^{-4}$**<br>**$\text{wd} = 10^{-4}$**<br>**Batch = 16 (Accum 8 -> 128)**<br>**Dải $E_b/N_0$: 0 dB đến 20 dB** (hoặc [8.8, 22.0] dB theo Shannon) | Tránh phân kỳ gradient khi train Transformer/Axial Attention. Dải Eb/N0 động bao phủ toàn bộ vùng thác lỗi (waterfall region) của 64-QAM rate 0.9. |
| **D14** | **Kiểu nội suy LS (LS Interpolation)**<br>- `interpolation_type` | Luận văn không nêu rõ thuật toán nội suy cụ thể | `interpolation_type = "nn"` (Cell 25, Cell 28, Cell 36) | Không phụ thuộc trọng số NN | **`interpolation_type = "nn"`** (Nearest Neighbor) | Mã nguồn thực nghiệm gốc trong notebook sử dụng `LSChannelEstimator(resource_grid, interpolation_type="nn")`. Nội suy lân cận gần nhất theo thời gian (symbols $0..6$ dùng pilot symbol 2, symbols $7..13$ dùng pilot symbol 11). |
| **D15** | **Kiến trúc San bằng LMMSE (Equalizer Architecture)**<br>- Dạng bộ lọc san bằng | Luận văn ghi LMMSE | Cell 24 (`LMMSEFeatureExtractor`) & Cell 36 (`LMMSEEqualizer`) | Không phụ thuộc trọng số NN | **Single-tap SIMO Wiener Filter per RE**:<br>$\hat{x} = \frac{\mathbf{h}^H \mathbf{y}}{\|\mathbf{h}\|^2 + N_0}$ | Đối với hệ SIMO 1 phát nhiều thu per-carrier, bộ lọc LMMSE rút gọn thành bộ lọc Wiener một tap giải tích trên từng phần tử tài nguyên. Biểu thức không chệch (unbiased) $\hat{x}_{ub} = \frac{\mathbf{h}^H \mathbf{y}}{\|\mathbf{h}\|^2}$ kết hợp phương sai tạp âm hiệu dụng $\sigma_{eff}^2 = \frac{N_0 + \sigma_e^2}{\|\mathbf{h}\|^2}$ cung cấp đầu vào chuẩn xác cho bộ giải ánh xạ Demapper (APP / Max-Log). |
| **D16** | **Quy trình Quét BLER & Khoảng tin cậy**<br>- Chuẩn tin cậy binomial<br>- Điều kiện dừng sớm<br>- Dải SNR & 1-lệnh DoD | Luận văn không nêu chi tiết CI | `num_target_block_errors = 100`<br>`batch_size = 128`<br>`ebno_db_step = 0.5` | Không phụ thuộc trọng số | **Clopper-Pearson 95% CI** (Beta quantile)<br>**Dừng sớm**: $\ge 100$ block errors hoặc $50,000$ slots<br>**Runner 1-lệnh**: `run_b0_cdlc_benchmark` | Đảm bảo tính chặt chẽ thống kê chuẩn 3GPP cho đường cong BLER thác lỗi (waterfall curve), kẹp chặt $0 \le CI_{low} \le \text{BLER} \le CI_{high} \le 1$. |

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
| **10** | `no_log` | Real (float32) | Phương sai tạp âm $\log_{10}(N_0)$ broadcast trên toàn lưới $(T \times F)$ |
| **11** | `pilot_mask` | Binary (0.0/1.0) | Mặt nạ vị trí pilot (1.0 tại ký hiệu OFDM thứ 2 và 11; 0.0 tại các vị trí data) |

> **Ghi chú**: Đối với Baseline CNN ResNet, số kênh đầu vào là **5 kênh**: `[y_real_0, y_real_1, y_imag_0, y_imag_1, no_log]`.

---

## 3. Kết luận & Cấu Trúc Cấu Hình Đơn Nguồn (`config/config.yaml`)

Toàn bộ tham số trong file `config/config.yaml` sẽ lấy trực tiếp từ cột **Quyết định chốt** của bảng trên, phân thành các block:
- `phy`: tần số sóng mang 3.5 GHz, SCS 30 kHz, FFT 128, OFDM symbols 14, guards [5, 6], DC null true, QAM 64 (6 bits), coderate 0.9.
- `channel`: cdl_model "C", delay_spread 100 ns (100e-9 s), speed [0.0, 50.0] m/s.
- `model_proposed`: d_model 128, nhead 4, num_layers 6, d_ff 256, dropout 0.1, in_channels 12.
- `model_cnn`: conv_channels 128, num_blocks 11, in_channels 5.
- `training`: lr 1e-4, wd 1e-4, batch_size 16, accumulation_steps 8, iterations 100000, seed 42.

---

## 4. Đặc tả kỹ thuật Bộ thu Cổ điển: Ước lượng kênh LS & Bộ san bằng LMMSE (D14, D15)

Nhằm đảm bảo tính tái lập 100% giữa mã nguồn thực nghiệm gốc tại notebook tham chiếu (`Working/nrx-bounded/notebooks/Compare/Neural_Receiver_compare_debugged(collab).ipynb`) và module `src/rx/classical.py`, các đặc tả sau đã được chốt và hiện thực:

### 4.1. Ước lượng kênh Least-Squares (LS) & Kiểu nội suy `interpolation_type="nn"` (D14)
- **Vị trí Pilot**: Pilot được phân bổ trên 2 ký hiệu OFDM: $t \in \{2, 11\}$ (Kronecker pilot pattern) trên toàn bộ 116 sóng mang khả dụng (loại trừ 5 sóng mang bảo vệ trái, 6 sóng mang bảo vệ phải và sóng mang trung tâm DC null).
- **Ước lượng LS tại Pilot**:
  $$\hat{H}_{LS}(r, t_p, f) = \frac{Y(r, t_p, f)}{X_p(t_p, f)}$$
  Trong đó $X_p$ là các ký hiệu pilot chuẩn QPSK đơn vị năng lượng.
- **Nội suy lân cận gần nhất (`"nn"`)**:
  Do kênh truyền có độ dịch Doppler thấp (tốc độ người dùng $v = 0$ m/s), thuật toán nội suy nearest-neighbor theo thời gian được áp dụng trực tiếp:
  $$\hat{H}_{LS}(r, t, f) = \begin{cases} \hat{H}_{LS}(r, 2, f), & 0 \le t \le 6 \\ \hat{H}_{LS}(r, 11, f), & 7 \le t \le 13 \end{cases}$$
- **Phương sai sai số ước lượng kênh**:
  $$\sigma_e^2 = \mathbb{E}\left[|H - \hat{H}_{LS}|^2\right] = N_0$$
  Giá trị này được truyền vào bộ san bằng LMMSE dưới dạng tham số `err_var` để bù trừ suy hao công suất do sai số ước lượng kênh (ở Baseline B1 genie-aided, `err_var = 0.0`).

### 4.2. Bộ san bằng giải tích LMMSE (Single-tap SIMO Wiener Filter) (D15)
- **Mô hình SIMO tại từng RE $(t, f)$**:
  Tín hiệu thu tại $M = 2$ anten: $\mathbf{y} = \mathbf{h} x + \mathbf{w}$, với hiệp phương sai nhiễu $\mathbf{S} = (N_0 + \sigma_e^2) \mathbf{I}_M$.
- **Biểu thức san bằng Wiener**:
  $$\hat{x}_{LMMSE} = \frac{\mathbf{h}^H \mathbf{y}}{\|\mathbf{h}\|^2 + N_0 + \sigma_e^2}$$
  Công thức này trùng khớp hoàn toàn với `LMMSEFeatureExtractor` trong Cell 24 của notebook tham chiếu:
  `num = torch.sum(torch.conj(h_ls) * y, dim=1, keepdim=True)`
  `denom = torch.sum(torch.abs(h_ls)**2, dim=1, keepdim=True) + no`
  `x_lmmse = num / (denom + 1e-8)`
- **Dạng không chệch (Unbiased) & Phương sai hiệu dụng cấp cho Demapper**:
  Để cấp cho Demapper (Sionna `Demapper("app", "qam")` hoặc PyTorch APP fallback), tín hiệu được hiệu chỉnh không chệch:
  $$\hat{x} = \frac{\mathbf{h}^H \mathbf{y}}{\|\mathbf{h}\|^2}$$
  $$\sigma_{eff}^2 = \frac{N_0 + \sigma_e^2}{\|\mathbf{h}\|^2}$$
  Biểu thức khoảng cách bình phương chuẩn hóa tương đương:
  $$\frac{|\hat{x} - c|^2}{\sigma_{eff}^2} = \frac{|\mathbf{h}^H \mathbf{y} - \|\mathbf{h}\|^2 c|^2}{(N_0 + \sigma_e^2)\|\mathbf{h}\|^2}$$
  giúp khôi phục xác suất hậu nghiệm (APP) và LLR mềm $\ell_A$ với độ chính xác số học tối ưu.

---

## 5. Đặc tả Kỹ thuật Đánh giá Hiệu năng BLER/BER & Khoảng Tin cậy Clopper-Pearson 95% (D16)

Nhằm đảm bảo các đường cong thực nghiệm BLER/BER phản ánh chính xác hiệu năng đường truyền không dây và thỏa mãn tiêu chí Definition of Done (DoD) của Issue #3:

### 5.1. Khoảng tin cậy Clopper-Pearson 95% (`clopper_pearson`)
- Sử dụng phân phối xác suất Beta quantile nghịch đảo (`scipy.stats.beta.ppf`):
  - Khi $k = 0$: $CI_{low} = 0.0, \quad CI_{high} = 1.0 - (\alpha/2)^{1/n}$
  - Khi $k = n$: $CI_{low} = (\alpha/2)^{1/n}, \quad CI_{high} = 1.0$
  - Khi $0 < k < n$:
    $$CI_{low} = \text{Beta.ppf}\left(\frac{\alpha}{2}, k, n - k + 1\right)$$
    $$CI_{high} = \text{Beta.ppf}\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)$$
- Khẳng định tính toán chặt: $0.0 \le CI_{low} \le \frac{k}{n} \le CI_{high} \le 1.0$.

### 5.2. Tiêu chuẩn Dừng Sớm Monte Carlo (Early Stopping Criteria)
- Tại mỗi mốc $E_b/N_0$, hàm `bler_point` mô phỏng lặp theo batch và dừng sớm ngay khi một trong hai điều kiện được thỏa mãn:
  - Số khối lỗi đạt ngưỡng $\ge 100$ (`block_errors >= target_errors`), HOẶC
  - Tổng số khe truyền đạt trần $50,000$ (`total_blocks >= max_slots`).

### 5.3. Thực thi Đo kiểm 1 Lệnh (1-Command Runner)
- Hàm `run_b0_cdlc_benchmark(v=10.0, ...)` tự động khởi tạo mô hình kênh 3GPP CDL-C tại vận tốc $10\text{ m/s}$, lưới tài nguyên 64-QAM $R=0.9$, quét dải SNR, tính toán khoảng tin cậy 95% và xuất đồ thị PNG chuẩn vào `plots/evaluation/b0_cdlc_10ms_bler.png`, thỏa mãn trọn vẹn DoD của Issue #3.

