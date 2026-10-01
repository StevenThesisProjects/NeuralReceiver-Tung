# Research Roadmap 4 tháng — Vương Thanh Tùng

**Đề tài:** *Asymptotically Bounded Neural Receivers via LMMSE-Assisted Axial Attention for 6G Physical Layer*
**Sinh viên:** Vương Thanh Tùng (EEEEIU22079) — School of Electrical Engineering, IU-VNUHCMC
**Cố vấn:** TS. Huỳnh Võ Trung Dũng
**Ngày lập:** 01/10/2026 · **Phiên bản:** v1.0
**Tổng thời gian:** 4 tháng = 2 tháng Conference + 2 tháng Journal (05/10/2026 → 31/01/2027, 8 sprint × 2 tuần)
**Nguồn đầu vào đã đọc (toàn bộ folder `20252526_S3`):**

| Mã | File | Loại nguồn | Vai trò trong roadmap |
|---|---|---|---|
| [T] | `Senior-Project-Report_v2.docx` | **Nguồn sơ cấp** (thesis, 31 hình, 13 bảng, Phụ lục A–C) | Bằng chứng duy nhất về kết quả thực nghiệm |
| [R1] | `2026_09_22_research_advisor_report.md` | Nguồn thứ cấp (báo cáo cố vấn) | Định hướng, đề xuất EXP-1…4 |
| [R2] | `2026_09_22_VuongThanhTung_thesis_review_report.md` | Nguồn thứ cấp (review luận văn) | Danh sách lỗi trình bày, tái lập |
| [R3] | `2026_09_22_brainstorming.md` / `.pdf` (nội dung trùng nhau) | Nguồn thứ cấp | Ý tưởng cổng lồi, ablation 4 nhánh |
| [R4] | `2026_09_22_criticalthinking.md` | Nguồn thứ cấp | Thẩm định nguy cơ phản biện |

> **Quy ước:** Mọi con số trong roadmap được truy về [T] (kèm số hình/bảng) hoặc nguồn web (kèm link). Khi [R1]–[R4] nêu một con số không có trong [T], roadmap gắn nhãn `NEEDS VERIFICATION`. Nhận định của người lập roadmap được ghi rõ là *suy luận* hoặc *đánh giá*.

> **Ghi chú tên file:** mẫu yêu cầu là `[ten_sinh_vien]_12Month_ResearchRoadmap.md`, nhưng tổng thời gian thực là 4 tháng, nên file được đặt tên `VuongThanhTung_4Month_ResearchRoadmap.md` để không gây hiểu nhầm.

---

## 1. Executive Summary

**Kết luận chính (đọc trước):**

1. **Tuyên bố cốt lõi hiện tại chưa được dữ liệu của chính luận văn ủng hộ.** Project instructions nêu LMMSE “ngăn chặn sàn lỗi sụp đổ ở 40 m/s và CDL-D”. Đọc trực tiếp đồ thị trong [T] cho thấy:
   - Ở **40 m/s** (Fig. 24 CDL-C, Fig. 26 CDL-D; train 0 m/s), mô hình đề xuất **vẫn có sàn lỗi BLER ≈ 0.2**, trùng đường LS-LMMSE; trong khoảng 15–25 dB, CNN baseline còn **thấp hơn** (BLER ≈ 0.08–0.17).
   - Ở **CDL-D, 10 m/s** (Fig. 25), mô hình đề xuất chỉ đạt BLER ≈ 4–5×10⁻⁴ tại 29.5 dB, trong khi **baseline LS-LMMSE đạt 10⁻⁴ ở ≈ 14 dB**. Đọc từ đồ thị: tại BLER 10⁻³ mô hình đề xuất cần ≈ 25.5 dB so với ≈ 13.6 dB của LS-LMMSE (kém ≈ 12 dB); tại 10⁻⁴ mô hình đề xuất không đạt trong dải đo. Tức là mô hình đề xuất **kém hơn chính “mỏ neo” LMMSE** → cơ chế ghép tensor **không** tạo ra cận dưới LMMSE.
   - Caption Fig. 25 ghi “đạt 10⁻⁴ tại 29.5 dB” — đồ thị không cho thấy điều này.
2. **Tuyên bố hiệu quả (−90.9% tham số) so với “DeepRx” cần sửa.** DeepRx gốc của Honkala et al. có **1.2M tham số** ([arXiv:2005.01494](https://arxiv.org/pdf/2005.01494)); bản tái hiện trong [T] có 13.35M. Mô hình đề xuất 1.21M ≈ DeepRx gốc. Ngoài ra DeepRx gốc nhận cả Y, pilot và ước lượng kênh thô làm đầu vào, còn baseline CNN trong [T] chỉ nhận Y thô → baseline đang bị làm yếu.
3. **Phần còn giá trị khoa học thật:** (a) mô hình đề xuất vượt rõ CNN khi lệch vận tốc 0→10 m/s (Fig. 22–23) và trong CDL-D 4-QAM (Fig. 17–18); (b) hiện tượng “ghép đặc trưng giải tích ≠ bảo đảm an toàn OOD” là một **phát hiện thực nghiệm mới, có thể công bố** nếu được đo chặt chẽ.
4. **Định hướng đề xuất:** biến chữ “Asymptotically Bounded” từ một tuyên bố thành một **kết quả có chứng minh**: thay ghép tensor bằng **cổng lồi trong miền LLR** (LLR-domain convex gate). Vì binary cross-entropy lồi theo LLR, có thể chứng minh **cận dưới tốc độ BMD (bit-metric decoding rate)** của bộ thu lai theo tốc độ BMD của LMMSE khi cổng tiến về 1 (Mục 12). Đây là đóng góp chứng minh được trong 2 tháng.
5. **Conference (tháng 1–2):** Fair baselines + ablation 5 nhánh + LLR-gate + mệnh đề BMD-rate floor + lưới đánh giá OOD (5 CDL × 7 vận tốc). Venue chính: **IEEE VTC2027-Fall** (hạn nộp 01/02/2027; CORE2023 rank B) — nguồn ở Mục 28.
6. **Journal (tháng 3–4):** đóng góp mới = **khoảng cách phân bố có nhận biết Doppler** (MMD trên đặc trưng tương quan thời–tần thay vì PDP) dùng để (i) dự báo suy giảm BLER khi lệch miền và (ii) điều khiển cổng trực tuyến. Lý do: MMD trên PDP chuẩn hóa không chứa thông tin Doppler — Table 3 và Table 4 của [T] (0 m/s và 10 m/s) giống hệt nhau. Venue: IEEE TCCN hoặc IEEE TVT (Q1, SJR 2025).
7. **Tính khả thi tổng thể: 🟡 FEASIBLE WITH CONDITIONS.** Điều kiện then chốt: (C1) mã nguồn Colab phải được thu thập và tái lập được Fig. 23/25 trong Sprint 1; (C2) pilot benchmark trên T4 cho thấy ≤ ~40 GPU-giờ cho toàn bộ ma trận thí nghiệm conference; (C3) Gate 1 xác nhận LLR-gate không trùng với prior art về hybrid switching ([Obeed & Jian, arXiv:2509.18574](https://arxiv.org/html/2509.18574)).

**Việc cần làm ngay (tuần 05–09/10):** Tùng đưa toàn bộ notebook Colab vào một Git repo, chạy lại Fig. 25 với seed cố định, và báo cáo cho cố vấn trước 09/10. Nếu không tái lập được, toàn bộ roadmap chuyển sang nhánh Plan B ở Mục 27.

---

## 2. Input & Timeline

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Thời gian Conference | 2 tháng: 05/10/2026 → 29/11/2026 (Sprint 1–4) | Người dùng |
| Thời gian Journal | 2 tháng: 30/11/2026 → 31/01/2027 (Sprint 5–8 + 1 tuần buffer) | Người dùng |
| Mục tiêu Conference | Rank B trở lên | Người dùng |
| Mục tiêu Journal | Q1/Q2 | Người dùng |
| Compute | GPU Google Colab (NVIDIA Tesla T4), coi là tài nguyên cố định | [T] Fig. 30–31, Table 6–7, Table 13 |
| Hardware | Không dùng; không mua sắm | Nguyên tắc roadmap |
| Simulator | NVIDIA Sionna + PyTorch (phiên bản cụ thể `NEEDS VERIFICATION` — [T] không ghi version; [R1]/[R3] ghi “Sionna 2.0+”) | [T] §2.1.1, App. C |

```text
Tháng 1 (Oct)           Tháng 2 (Nov)            Tháng 3 (Dec)           Tháng 4 (Jan)
S1 05-18/10  S2 19/10-01/11  S3 02-15/11  S4 16-29/11  S5 30/11-13/12  S6 14-27/12  S7 28/12-10/01  S8 11-24/01  Buffer 25-31/01
[Gate1]      [Gate2,3]        [Gate4]      [Gate5]       [Gate6]                                   [Gate7]
|<----------- CONFERENCE ----------->|      |<-------------- JOURNAL ---------------->|
                                      Conference paper frozen 29/11 → nộp VTC2027-Fall trước 01/02/2027
```

---

## 3. Current Research Status

### 3.1. Bảng trạng thái thành phần

| Thành phần | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| Research problem (độ chính xác vs khả năng triển khai của neural receiver) | `COMPLETED` | [T] §1.2 | Cần viết lại xoay quanh **an toàn OOD** |
| Research gap | `PARTIAL` | [T] §4.4 (gap MMD cho họ CDL) | Gap “bounding” chưa được viết; prior art hybrid switching chưa được trích |
| Research questions | `NOT STARTED` (dạng chính thức) | [R3] có 1 câu hỏi tổng | Mục 5 của roadmap đề xuất RQ1–RQ5 |
| Kiến trúc LMMSE + Axial Transformer | `PARTIAL` | [T] §2.1.1, §5.3, Fig. 9–10 | Mâu thuẫn d_model (128 vs 64), số khối (N=6 vs 4) |
| Công thức toán (Eq. 1–13) | `PARTIAL` | [T] §2.1 | Eq. 13 sai chỉ số; thiếu công thức demapper LMMSE; không có công thức bound |
| Mã nguồn | `NEEDS VERIFICATION` | [T] nhắc Google Colab; **không có code trong folder** | Rủi ro số 1 |
| Dataset (synthetic Sionna CDL) | `COMPLETED` (cơ chế), `NEEDS VERIFICATION` (tham số) | [T] Table 8–11, A.2 | Delay spread: 10⁻⁷ s cho mọi CDL (Table 8–11) vs “30–300 ns” (Table A.2) |
| Baseline LS-LMMSE, Perfect CSI | `COMPLETED` | [T] Fig. 11–29 | Cần xác minh kiểu nội suy thời gian của LS estimator |
| Baseline CNN (DeepRx-style) | `PARTIAL` | [T] Fig. 19, 30 | 13.35M tham số, chỉ đầu vào Y thô → không phải DeepRx gốc |
| Baseline Axial thô (Yellapragada-style) | `NOT STARTED` | — | Cần cho ablation |
| Thí nghiệm 4-QAM, CDL-A/B/C/D, 10 m/s | `COMPLETED` (1 lần chạy) | [T] Fig. 11–18 | Không seed, không CI |
| Thí nghiệm 64-QAM R=0.9, train 0 m/s | `COMPLETED` (1 lần chạy) | [T] Fig. 21–26 | 97.2 m/s chỉ có CNN, **không có mô hình đề xuất** |
| Thí nghiệm 64-QAM R=0.9, train 10 m/s | `COMPLETED` (1 lần chạy) | [T] Fig. 27–29 | Chỉ vẽ mô hình đề xuất |
| MMD² trên PDP | `PARTIAL` | [T] Table 3–4, Fig. 1–2 | Table 3 ≡ Table 4; chưa tương quan với BLER |
| Đo độ phức tạp (params/FLOPs/latency T4) | `COMPLETED` | [T] Fig. 30–31 (log gốc) | Chưa rõ FLOPs có gồm khâu LMMSE |
| Ablation | `NOT STARTED` | [R1] EXP-1 đề xuất | — |
| Monte Carlo seeds / CI | `NOT STARTED` | [R2] Issue #8 | — |
| Cổng lồi (gate) | `NOT STARTED` | [R3] Ý TƯỞNG-03 | Mới là ý tưởng ở miền symbol |
| Web demo | `NOT STARTED` | — | — |
| Publication | `NOT STARTED` | — | Chưa có bản thảo IEEE |

### 3.2. Đối chiếu số liệu: nguồn sơ cấp vs báo cáo thứ cấp

Các mâu thuẫn dưới đây phải được xử lý trước khi viết paper. Cột “Hành động” là việc kiểm chứng trong code.

| # | Nội dung | [T] nói gì | [R1]–[R4] nói gì | Hành động |
|---|---|---|---|---|
| D1 | Hiệu năng mô hình đề xuất ở 40 m/s | Fig. 24, 26: sàn BLER ≈ 0.2, trùng LS; CNN thấp hơn ở 15–25 dB | [R3] bảng §4: “BLER ≤ 10⁻³ ở 40 m/s” | Bỏ tuyên bố của [R3]; chạy lại với seed |
| D2 | CDL-D 10 m/s (train 0 m/s) | Fig. 25: ≈ 4.5×10⁻⁴ tại 29.5 dB; LS-LMMSE đạt 10⁻⁴ tại ≈ 14 dB | [R1], [R3]: “BLER 10⁻⁴ tại 29.5 dB, phục hồi hoàn toàn” | Sửa caption; coi đây là bằng chứng *phản* lại bound |
| D3 | 97.2 m/s | Chỉ CNN được vẽ (Fig. 21) | [R2]: mô hình đề xuất “graceful” ở 97.2 m/s | `NOT STARTED` cho mô hình đề xuất |
| D4 | Số tham số CNN “full” | 13,352,198 (log Fig. 30–31) / 13,352,188 (caption) | — | Dùng số trong log; sửa caption |
| D5 | DeepRx gốc | — | Gọi bản 13.35M là “DeepRx SOTA” | DeepRx gốc = 1.2M ([arXiv:2005.01494](https://arxiv.org/pdf/2005.01494)) |
| D6 | d_model, số khối Axial | §2.1.1: d_model = 128, h = 4, d_h = 32; §5.3: N = 6; Table A.1: d_model = 64, 4 khối | [R1]: 4 khối, d_model 64, d_h 16 | Đọc từ checkpoint/code |
| D7 | Kích thước lưới | §2.1.1, §4.3: F = 128; Table A.1/A.2: 72 subcarrier, N_FFT 1024 | [R2] Issue #7 | Đọc từ code |
| D8 | Số kênh đầu vào | Eq. 1: 12; App. C: 6; Table A.1: (B, 2, N_sym, N_sub) | [R1], [R2]: “thống nhất 12” | **Không** thống nhất bằng văn bản; xác định cái code thực sự dùng |
| D9 | Delay spread | Table 8–11: 10⁻⁷ s cho mọi CDL; Table A.2: 30–300 ns | [R2] Issue #6: “chỉ ghi đơn vị s” và đề xuất 300/100/300/30 ns | Số trong [R2] không đến từ [T]; đọc từ code |
| D10 | MMD ở 10 m/s | Table 4 giống hệt Table 3; văn bản ghi trung bình 10 m/s = 0.148276 (không khớp bảng) | [R1]: dùng MMD làm đóng góp “NOVEL” | Tính lại; xem Mục 4.3 |
| D11 | Latency | 7.012 ± 1.003 ms (đề xuất) vs 9.651 ± 0.249 ms (CNN) trên T4, batch 1 | [R1]: “thỏa mãn ≤ 0.5 ms” | Không tuyên bố real-time; slot = 0.5 ms ([T] Table A.2) |
| D12 | Thông số dự đoán | — | “Axial đóng góp 2.5 dB, LMMSE 1.5 dB”, “σ ≤ 0.2 dB”, “Yellapragada ≈ 1.8M params, BLER ≈ 0.08 ở 40 m/s” | Đều là **dự đoán**, `TBD` |
| D13 | Huấn luyện | Table 8: lr 10⁻³; Table 9–11, A.1: lr 10⁻⁴; Eb/N0 train 0–20 dB và 8–22 dB | — | Ghi vào `config.yaml` |

---

## 4. Research Problem & Motivation

### 4.1. Bài toán

Neural receiver (NRX) thay chuỗi ước lượng kênh → cân bằng → giải ánh xạ bằng một mạng học sâu, xuất LLR cho bộ giải mã LDPC 5G NR. Trong phân bố huấn luyện, NRX gần đạt Perfect CSI ([T] Fig. 12, 14, 16). Ngoài phân bố (lệch vận tốc, lệch LOS/NLOS), NRX có thể **kém hơn cả bộ thu cổ điển** ([T] Fig. 22–26). Với trạm gốc, điều nguy hiểm không phải là NRX kém tối ưu, mà là NRX **kém hơn bộ thu mà nó thay thế** mà không có cơ chế nhận biết.

### 4.2. Động lực

- **Thực tế triển khai:** Wiesmayr et al. chỉ ra fine-tune theo site có thể làm giảm hiệu năng ở site cũ ([T] §1.2, ref [4]). Một NRX cần một **đảm bảo không tệ hơn baseline** để được chấp nhận.
- **Prior art cho thấy độ phủ dữ liệu huấn luyện quyết định phần lớn khả năng tổng quát** ([Al Rabby, Zenodo 2026](https://zenodo.org/records/22994791); [Yellapragada et al., arXiv:2510.12941](https://arxiv.org/html/2510.12941v2) huấn luyện 0–50 m/s nên chạy tốt ở 40 m/s). Nhưng không thể phủ mọi điều kiện triển khai → cần cơ chế cấu trúc.
- **Bằng chứng trong [T]:** ghép LMMSE vào tensor đầu vào giúp ở lệch vừa (0→10 m/s, Fig. 22–23) nhưng không bảo vệ ở lệch mạnh (Fig. 24–26).

### 4.3. Hai vấn đề khoa học phụ đã lộ ra khi đọc [T]

1. **MMD trên PDP chuẩn hóa không thấy Doppler.** PDP mô tả phân bố công suất theo trễ; vận tốc chỉ làm thay đổi tương quan theo thời gian. *Suy luận:* vì vậy Table 3 (0 m/s) và Table 4 (10 m/s) giống hệt nhau. Hệ quả: MMD-PDP có thể chọn miền huấn luyện theo delay spread/LOS nhưng **không thể** dự báo thất bại do Doppler — đúng loại thất bại nặng nhất trong [T].
2. **Thống kê Doppler đo được ngay từ DMRS.** Với DMRS ở symbol 2 và 11 ([T] Table A.2), khoảng cách 9 symbol ≈ 0.321 ms. Theo mô hình Jakes, hệ số tương quan ρ = J₀(2π f_d Δt) giữa hai DMRS là (tính toán của người lập roadmap, f_c = 3.5 GHz, SCS 30 kHz, CP thường):

| v (m/s) | f_d (Hz) | T_c ≈ 0.423/f_d (ms) | ρ(DMRS₂, DMRS₁₁) |
|---|---|---|---|
| 0 | 0 | ∞ | 1.000 |
| 10 | 116.7 | 3.63 | 0.986 |
| 20 | 233.3 | 1.81 | 0.945 |
| 30 | 350.0 | 1.21 | 0.879 |
| 40 | 466.7 | 0.91 | 0.790 |
| 60 | 700.0 | 0.60 | 0.560 |
| 97.2 | 1134.0 | 0.37 | 0.062 |

*Suy luận:* ở 40 m/s, T_c ≈ 0.91 ms vẫn lớn hơn slot 0.5 ms, nên kênh không “phi dừng” trong slot như [R1]/[R4] mô tả; vấn đề thực sự là **nội suy thời gian giữa hai DMRS** (ρ = 0.79) và mô hình tương quan tĩnh của LMMSE. ρ̂ ước lượng từ hai DMRS là một **đặc trưng Doppler gần như miễn phí** để điều khiển cổng (Mục 9).

---

## 5. Research Gap

| Gap | Bằng chứng | Mức độ chắc chắn |
|---|---|---|
| **G1.** Chưa có NRX nào kết hợp LMMSE với attention theo cách **có cận dưới chứng minh được** so với bộ thu LMMSE khi gặp OOD. | Prior art đã kiểm tra: hard-switch giữa NRX và bộ thu truyền thống bằng discriminator, **không** có bound ([Obeed & Jian, arXiv:2509.18574](https://arxiv.org/html/2509.18574)); detect-and-rollback dựa trên bất đồng bit/LLR, **không** có bảo đảm hình thức ([Elnashar, arXiv:2605.26157](https://pith.science/paper/2605.26157)); mixture-of-experts có dùng LS làm đầu vào phụ ([CARNet, arXiv:2608.02172](https://arxiv.org/html/2608.02172v1)). | Trung bình — cần literature search có hệ thống ở Sprint 1 (Gate 1) |
| **G2.** Chưa có đo lường công bằng cho câu hỏi “ghép đặc trưng giải tích vào đầu vào có thay thế được cơ chế an toàn không?” | [T] Fig. 25: ghép LMMSE vẫn kém LS-LMMSE ≈ 12 dB tại BLER 10⁻³ ở CDL-D | Cao (từ dữ liệu [T]), cần tái lập |
| **G3.** Khoảng cách phân bố dùng để chọn miền huấn luyện cho NRX hiện bỏ qua chiều Doppler. | [T] Table 3 ≡ Table 4; [T] §4.4 tự nêu gap “tương quan MMD với BLER” nhưng chưa làm | Cao cho [T]; trung bình cho literature rộng (Morais et al. dùng UMAP + Wasserstein, [T] ref [18]) |
| **G4.** Đánh đổi giữa chi phí tính toán và **hiệu năng trường hợp xấu nhất (worst-case OOD)** chưa được đo như một mặt Pareto. | Yellapragada so sánh FLOPs và BLER trung bình, không có worst-case ([arXiv:2510.12941](https://arxiv.org/html/2510.12941v2)) | Trung bình |

**Gap không còn đứng được:** “Axial attention giảm tham số so với CNN” — đã có ở Yellapragada et al. (giảm 2.81× FLOPs so với global MHSA, hiệu năng tốt hơn CNN-ResNet 0.20–0.30 dB ở 1% BLER — theo [bản HTML v2](https://arxiv.org/html/2510.12941v2)). Đây chỉ là bối cảnh, không là novelty.

---

## 6. Research Questions & Hypotheses

| RQ | Hypothesis | Phương pháp | Thí nghiệm | Metric | Bằng chứng kỳ vọng | Đóng góp paper |
|---|---|---|---|---|---|---|
| **RQ1 — Attribution.** Trong điều kiện khớp miền, bao nhiêu dB đến từ đặc trưng LMMSE và bao nhiêu từ axial attention, khi so với baseline công bằng? | H1: Với baseline DeepRx-đúng (Y + pilot + H_LS, ~1.2M) và Axial-thô, phần lớn chênh lệch so với CNN-13M trong [T] đến từ đầu vào, không phải kiến trúc. | Ablation 5 nhánh M1–M5 (Mục 11) | E1 | SNR@BLER 10⁻², 10⁻³; Δ dB; params; FLOPs | Bảng ablation có CI | Fair-baseline table (Conf.) |
| **RQ2 — Bounding by concatenation.** Ghép x̂_LMMSE vào tensor đầu vào có giữ hiệu năng ≥ LS-LMMSE ở OOD không? | H2: **Không.** Có ít nhất một ô OOD (vd. CDL-D/10 m/s, train CDL-C/0 m/s) mà M4 kém LS-LMMSE > 3 dB. | M4 vs LS-LMMSE | E2 (lưới OOD) | Worst-case gap Γ = max_ô [SNR_M4 − SNR_LMMSE] | Bản đồ nhiệt Γ theo (CDL, v) | **Empirical insight** (Conf.) |
| **RQ3 — LLR-domain gate.** Cổng lồi trong miền LLR có (a) bảo đảm cận dưới tốc độ BMD và (b) giữ worst-case gap BLER ≤ 1 dB mà vẫn giữ lợi ích trong miền? | H3a: Mệnh đề BMD-rate floor đúng (chứng minh). H3b: M5 đạt Γ ≤ 1 dB trên mọi ô OOD và mất ≤ 0.3 dB so với M4 trong miền. | M5 = M4 + gate g(φ) | E2, E3 | Γ, ΔR_BMD, SNR@10⁻² | Bảng + hình g theo v | **Core method** (Conf.) |
| **RQ4 — Gate extrapolation.** Cổng ràng buộc đơn điệu theo ρ̂ (Doppler proxy), huấn luyện chỉ với lệch nhẹ, có ngoại suy đúng sang lệch mạnh chưa thấy? | H4: Với ràng buộc đơn điệu, g tăng theo v và đạt ≥ 0.9 khi v ≥ 60 m/s dù chỉ thấy v ≤ 20 m/s lúc hiệu chỉnh cổng. | Gate đơn điệu vs gate tự do | E4 | g trung bình theo v; Γ | Đường g(v) | Conf. (nếu kịp) / Journal |
| **RQ5 — Doppler-aware distance (Journal).** Khoảng cách MMD trên đặc trưng tương quan thời–tần có dự báo suy giảm BLER khi lệch miền tốt hơn MMD-PDP không? | H5: Spearman(MMD-TF, ΔSNR) ≥ 0.8, cao hơn rõ rệt MMD-PDP. | MMD trên vector tương quan R̂_t, R̂_f (Mục 12.5) | E6 | Spearman, Pearson, R² | Scatter MMD vs ΔSNR, 20 cặp miền | **Journal new contribution** |

---

## 7. Novelty Analysis

### 7.1. Đóng góp khoa học (A)

| Đóng góp | Loại | Delta so với prior art | Trạng thái |
|---|---|---|---|
| A1. **LLR-domain convex gate** giữa demapper LMMSE và axial NRX, với **mệnh đề BMD-rate floor** | New fusion mechanism + New mathematical formulation | Obeed & Jian: hard switch theo RG, không bound. Elnashar: rollback theo heuristic, không bound. Đề tài: kết hợp mềm theo từng RE, có cận dưới giải tích. | `NOT STARTED` |
| A2. **Monotone Doppler-proxy gate** dùng ρ̂ từ hai DMRS | New robustness mechanism | Chưa thấy NRX nào dùng ràng buộc đơn điệu theo đặc trưng vật lý để ngoại suy cổng — `NEEDS VERIFICATION` ở Gate 1 | `NOT STARTED` |
| A3. **Phát hiện: concatenation ≠ bounding** | New empirical insight | [T] Fig. 25 là bằng chứng sơ bộ; chưa thấy công bố đo trực tiếp điều này — `NEEDS VERIFICATION` | `PARTIAL` |
| A4. **Doppler-aware MMD** để dự báo suy giảm và điều khiển cổng | New representation + New evaluation | Mở rộng [T] §4.4 (MMD-PDP) và Morais et al. sang chiều Doppler | `NOT STARTED` (Journal) |

### 7.2. Đóng góp kỹ thuật (B)

- Pipeline Sionna tái lập được, `config.yaml` đơn nguồn, seed cố định.
- Đo params/FLOPs/latency trên T4.
- Web demo Gradio.

Các mục này cần cho paper và demo nhưng **không** được trình bày là novelty.

### 7.3. Nếu bỏ web demo, còn lại gì?

Còn A1 (mệnh đề + cơ chế), A3 (phát hiện thực nghiệm có kiểm soát) và A4 (cho journal). Đây là đóng góp đủ cho một paper rank B, **với điều kiện** H2 và H3b được xác nhận. Nếu H3b thất bại (cổng không giữ được Γ ≤ 1 dB), đóng góp còn lại là A3 + mệnh đề — vẫn có thể viết thành bài “negative result + analysis”, nhưng sức nặng giảm (xem Kill Criteria, Mục 27).

### 7.4. Về tiêu đề

“Asymptotically Bounded” chỉ được giữ nếu Gate 4 xác nhận A1. Tiêu đề dự phòng:
- *LMMSE-Anchored Axial Attention Receivers with a Provable Bit-Metric Rate Floor under Doppler and LOS Mismatch*
- (nếu H3b thất bại) *Does an Analytical Prior Bound a Neural Receiver? An Out-of-Distribution Study of LMMSE-Assisted Axial Attention*

---

## 8. Feasibility Assessment

| Dimension | Đánh giá | Evidence | Risk | Mitigation |
|---|---|---|---|---|
| Research Gap | 🟡 | G1–G3 có bằng chứng; prior art hybrid gần kề (arXiv:2509.18574, 2605.26157) | Có thể đã có paper LLR-domain fusion có bound | Literature search có hệ thống ở S1 (IEEE Xplore, arXiv 2023–2026, từ khóa ở Mục 24, Sprint 1) |
| Novelty | 🟡 | A1 có chứng minh đơn giản nhưng chặt; A3 có dữ liệu sơ bộ | Reviewer có thể coi mệnh đề là “hiển nhiên” | Kết hợp mệnh đề + gate đơn điệu + bằng chứng OOD rộng; không bán mệnh đề như định lý lớn |
| Algorithmic Feasibility | 🟢 | Gate = MLP nhỏ + combine LLR; demapper LMMSE có sẵn trong Sionna | Gate học g ≈ 0 nếu chỉ train trong miền | Hiệu chỉnh cổng 2 giai đoạn + ràng buộc đơn điệu (Mục 10) |
| Model Feasibility | 🟢 | Mô hình 1.21M params đã train được trên T4 ([T] Fig. 31) | Mâu thuẫn cấu hình D6–D8 | Đọc cấu hình từ code ở S1 |
| Dataset | 🟢 | Dữ liệu synthetic Sionna CDL, sinh theo batch, không rò rỉ ([R1] §3.1) | Tham số delay spread chưa chắc (D9) | Cố định trong `config.yaml` |
| Experimental Feasibility | 🟡 | Đã có pipeline BLER | Monte Carlo tới 10⁻⁴ tốn ~10⁶ block/điểm | Báo cáo chính tại BLER 10⁻² và 10⁻³; 10⁻⁴ chỉ cho 2–3 đường tiêu biểu |
| Computational Feasibility | 🟡 | T4 16 GB; batch 128 chạy được | Thời gian train/eval chưa đo; Colab ngắt phiên | Pilot benchmark S1; checkpoint mỗi epoch; ngân sách ở Mục 16 |
| Baseline | 🟡 | LS-LMMSE, Perfect CSI có sẵn | DeepRx-đúng và Axial-thô chưa có | Dùng mã Sionna tutorial cho NRX + viết Axial-thô từ mã đề xuất (bỏ đặc trưng) |
| Reproducibility | 🔴 → 🟡 | Code không có trong folder | Không tái lập được Fig. 25 | Gate 1 bắt buộc; Plan B ở Mục 27 |
| Demo Feasibility | 🟢 | Gradio trên Colab/CPU | Sionna chậm trên CPU | Cache kết quả + chạy batch nhỏ trực tiếp |
| Conference Feasibility | 🟡 | 8 tuần; VTC2027-Fall hạn 01/02/2027 | Lịch dày | Khóa phạm vi: SIMO 1×2, 64-QAM R=0.9, 1 protocol train |
| Journal Feasibility | 🟡 | A4 dùng lại pipeline | 8 tuần ngắn cho Q1; quy định nộp trùng lặp | Phạm vi journal xoay quanh A4; nộp sau khi kiểm tra chính sách (Mục 28) |

---

## 9. Proposed Method

### 9.1. Ý tưởng một câu

Giữ nhánh axial NRX làm “bộ thu giỏi trong miền”, giữ demapper LMMSE làm “bộ thu an toàn”, và trộn **LLR** của hai nhánh bằng một cổng g ∈ [0, 1] mà (i) có cận dưới tốc độ BMD chứng minh được và (ii) buộc g = 1 khi đặc trưng Doppler đo từ DMRS vượt ngưỡng vật lý.

### 9.2. Pipeline

```text
Received grid Y (14 × F × 2), DMRS ở symbol {2, 11}
   │
   ├── [LS @ DMRS] ──► Ĥ_LS ──► [Nội suy + LMMSE equalizer] ──► x̂_LMMSE, σ̂²_eff
   │                                         │
   │                                         └──► [APP/max-log demapper] ──► ℓ_A   (nhánh an toàn)
   │
   ├── [Z = concat(features)] ──► [Linear → +P_time +P_freq → N × AxialBlock → Head] ──► ℓ_N  (nhánh NRX)
   │
   ├── [Gate features φ] = { log N̂₀, ρ̂(DMRS₂, DMRS₁₁), r̂ (pilot residual), E|ℓ_N|, H(ℓ_N) }
   │          └──► g = max( σ(a_ψ(φ)),  h(ρ̂) )        h: ramp vật lý cố định, đơn điệu
   │
   └── ℓ_H = g · ℓ_A + (1 − g) · clip_Λ(ℓ_N) ──► 5G NR LDPC BP decoder ──► bits
```

### 9.3. Vì sao trộn ở miền LLR mà không ở miền symbol

[R3]/[R4] đề xuất ŝ = g·x̂_LMMSE + (1 − g)·F_θ(Z) ở miền symbol. *Đánh giá:* demapper là ánh xạ phi tuyến, nên tổ hợp lồi ở miền symbol không cho ra cận nào trên loss bit. Ở miền LLR, BCE là hàm softplus của LLR nên lồi, cho phép chứng minh trực tiếp (Mục 12.3). Phương án miền symbol được giữ lại làm **ablation E4** để chứng minh lựa chọn này.

### 9.4. Đặc trưng cho cổng

| Đặc trưng | Công thức | Ý nghĩa vật lý | Chi phí |
|---|---|---|---|
| log N̂₀ | từ ước lượng nhiễu sẵn có | SNR thấp → LLR NRX kém tin cậy | ~0 |
| ρ̂ | Re⟨Ĥ_LS[2,:,:], Ĥ_LS[11,:,:]⟩ / √((P₂ − N̂₀)(P₁₁ − N̂₀)) | Proxy Doppler (Mục 4.3) | O(F·N_RX) |
| r̂ | ‖Ĥ_LS − Ĥ_interp‖² trên DMRS (leave-one-out) / N̂₀ | Lệch mô hình tương quan của LMMSE | O(F·N_RX) |
| E\|ℓ_N\| , H(ℓ_N) | trung bình độ lớn và entropy LLR của NRX | NRX quá tự tin hoặc lưỡng lự | O(T·F·m) |

*Lưu ý:* hiệu chỉnh bias nhiễu trong ρ̂ là cần thiết; nếu không, SNR thấp sẽ kéo ρ̂ xuống và đẩy g lên. Hướng sai lệch này là “an toàn” (fallback nhiều hơn), nhưng làm mất lợi ích NRX ở SNR thấp — đo trong E3.

---

## 10. Algorithm Design

### 10.1. Thuật toán A — Huấn luyện hai giai đoạn

```text
Algorithm A: Train-Gated-Axial-NRX
Input : protocol P (CDL, v-range, Eb/N0-range), Λ, ρ_hi, ρ_lo, seeds S
Stage 1 (backbone):
  for epoch in 1..E1:
     sample batch from Sionna(P)                 # synthetic, không lưu dataset
     ℓ_N ← f_θ(Z) ; loss ← BCE(ℓ_N, b)
     θ ← Adam(θ, ∇loss)                          # lr 1e-4 (theo [T])
  freeze θ
Stage 2 (gate calibration):
  calibration set 𝒞: CDL-C, CDL-A; v ∈ {0, 10, 20} m/s  (KHÔNG dùng CDL-B/D/E, KHÔNG dùng v ≥ 30)
  for epoch in 1..E2:
     ℓ_A ← LMMSE-demap(Y) ; ℓ_N ← f_θ(Z) ; φ ← features(Y, Ĥ_LS, ℓ_N)
     g ← max(σ(a_ψ(φ)), h(ρ̂)) ; ℓ_H ← g·ℓ_A + (1−g)·clip_Λ(ℓ_N)
     loss ← BCE(ℓ_H, b) + λ·E[g]   # λ nhỏ: phạt fallback không cần thiết
     ψ ← Adam(ψ, ∇loss)
Stage 3 (optional, journal): joint fine-tune θ, ψ với lr 1e-5
Output: θ, ψ
```

### 10.2. Ramp vật lý h(ρ̂)

h(ρ̂) = clip((ρ_hi − ρ̂)/(ρ_hi − ρ_lo), 0, 1).
Mặc định: ρ_hi = ρ(v_max,cal + 10 m/s) = ρ(30 m/s) ≈ 0.879; ρ_lo = ρ(60 m/s) ≈ 0.560 (giá trị từ bảng Mục 4.3). Đây là **siêu tham số có ý nghĩa vật lý**; độ nhạy được quét trong E4.

### 10.3. Độ phức tạp tăng thêm

- Nhánh LMMSE-demap: đã tính trong pipeline [T] (vì x̂_LMMSE đã là đầu vào); chỉ thêm demapper APP: O(T·F·|𝒞|) với |𝒞| = 64.
- Gate MLP: ~10³ tham số; đặc trưng O(T·F·m).
- *Kỳ vọng (cần đo, E5):* < 5% FLOPs so với backbone 1.45 GFLOPs.

---

## 11. Model Architecture

### 11.1. Họ mô hình dùng trong toàn bộ nghiên cứu

| ID | Tên | Đầu vào | Backbone | Đầu ra | Vai trò |
|---|---|---|---|---|---|
| B0 | LS-LMMSE | Y, DMRS | Cổ điển (Sionna) | ℓ_A | Baseline thực tế, “mỏ neo” |
| B1 | Perfect CSI + LMMSE | Y, H thật | Cổ điển | LLR | Cận trên |
| M1 | **DeepRx-đúng** | Y, X_pilot, Ĥ_raw (theo Honkala et al.) | 11 ResNet block, ~1.2M params | ℓ_N | Baseline CNN công bằng |
| M1′ | CNN-[T] | Y thô | ResNet 13.35M | ℓ_N | Tái lập kết quả [T] (chỉ dùng để so sánh với luận văn) |
| M2 | Axial-thô | Y (+ mask, N₀) | Axial, cùng cấu hình M4 | ℓ_N | Kiểu Yellapragada et al. |
| M3 | LS-Axial | Y, Ĥ_LS (+ mask, N₀) | Axial | ℓ_N | Tách vai trò LMMSE |
| M4 | LMMSE-Axial (concat) | Z theo Eq. 1 [T] (sau khi xác minh D8) | Axial | ℓ_N | Mô hình hiện tại |
| **M5** | **Gated LMMSE-Axial** | như M4 + φ | Axial + gate | ℓ_H | **Đề xuất** |

### 11.2. Cấu hình backbone (cần xác minh từ code — D6, D7)

| Tham số | Giá trị trong [T] | Ghi chú |
|---|---|---|
| T × F | 14 × 72 (Table A.1/A.2) hoặc 14 × 128 (§2.1.1) | `NEEDS VERIFICATION` |
| d_model, heads | 128, 4 (§2.1.1) hoặc 64, 4 (Table A.1) | `NEEDS VERIFICATION` |
| Số khối N | 6 (§5.3) hoặc 4 (Table A.1); minimal N = 3 | `NEEDS VERIFICATION` |
| FFN | r = 2 | Table A.1 |
| Norm | Post-LN (Eq. 8–10) | [R1] gợi ý Pre-LN — chỉ đổi nếu train không ổn định |
| Params / FLOPs | 1,213,318 / 1.4506 GFLOPs | log Fig. 31 |

**Quy tắc:** không đổi kiến trúc backbone trong giai đoạn conference trừ khi có hypothesis. Đóng góp nằm ở gate, không ở backbone.

---

## 12. Mathematical Formulation

### 12.1. Mô hình tín hiệu

Lưới tài nguyên sau FFT, SIMO 1 × N_RX (N_RX = 2):

$$Y_{t,f,r} = H_{t,f,r}\,X_{t,f} + W_{t,f,r},\qquad W_{t,f,r}\sim\mathcal{CN}(0, N_0)$$

với t ∈ {1..T}, f ∈ {1..F}, X_{t,f} ∈ 𝒞 (M-QAM, m = log₂M bit/symbol) ở RE dữ liệu và là DMRS đã biết ở symbol {2, 11}.

### 12.2. Hai nhánh LLR

LLR quy ước ℓ_i = log P(b_i = 0 | ·) / P(b_i = 1 | ·).

- **Nhánh giải tích** (sau LMMSE, nhiễu hiệu dụng σ̂²_eff):
$$\ell^{A}_{i} = \log\sum_{s\in\mathcal{C}^{0}_{i}} e^{-|\hat{x}-s|^{2}/\hat\sigma^{2}_{\mathrm{eff}}} - \log\sum_{s\in\mathcal{C}^{1}_{i}} e^{-|\hat{x}-s|^{2}/\hat\sigma^{2}_{\mathrm{eff}}}$$
- **Nhánh NRX:** ℓ^N = f_θ(Z), sau đó cắt biên ℓ̄^N = clip(ℓ^N, −Λ, Λ).
- **Hợp nhất:** ℓ^H = g ℓ^A + (1 − g) ℓ̄^N, với g = g(φ) ∈ [0, 1].

### 12.3. Hàm mất mát và tốc độ BMD

Per-bit BCE: 𝓛(ℓ; b) = log(1 + e^{−(1−2b)ℓ}).
Tốc độ BMD (Böcherer, được [T] dùng làm cơ sở cho loss):

$$R_{\mathrm{BMD}}(\ell) = m - \frac{1}{\ln 2}\sum_{i=1}^{m}\mathbb{E}\big[\mathcal{L}(\ell_i; b_i)\big]\quad\text{[bit/kênh sử dụng]}$$

### 12.4. Mệnh đề 1 — BMD-rate floor (đề xuất chứng minh trong paper)

**Phát biểu.** Với mọi cổng đo được g(φ) ∈ [0, 1] và |ℓ̄^N| ≤ Λ:

(a) Theo điểm: 𝓛(ℓ^H) ≤ g·𝓛(ℓ^A) + (1 − g)·𝓛(ℓ̄^N).

(b) Theo kỳ vọng:
$$R_{\mathrm{BMD}}(\ell^{H}) \;\ge\; R_{\mathrm{BMD}}(\ell^{A}) - \kappa_{\Lambda}\,\mathbb{E}[1-g],\qquad \kappa_{\Lambda} = m\log_{2}(1+e^{\Lambda})$$

(c) Trên tập con 𝒪 = {ρ̂ ≤ ρ_lo} (lệch Doppler mạnh), với g ≥ h(ρ̂) = 1: R_BMD(ℓ^H | 𝒪) = R_BMD(ℓ^A | 𝒪) — tức bộ thu lai **không tệ hơn LMMSE** trên vùng đó, theo nghĩa tốc độ BMD.

(d) Nếu g là hằng số: R_BMD(ℓ^H) ≥ g·R_BMD(ℓ^A) + (1 − g)·R_BMD(ℓ̄^N).

**Phác thảo chứng minh.** 𝓛 là softplus của hàm tuyến tính theo ℓ nên lồi → (a) theo bất đẳng thức Jensen hai điểm. Lấy kỳ vọng, dùng g·𝓛(ℓ^A) ≤ 𝓛(ℓ^A) và 𝓛(ℓ̄^N) ≤ log(1 + e^Λ), cộng qua m bit → (b). (c) là trường hợp g = 1. (d) là tuyến tính của kỳ vọng khi g hằng.

**Giới hạn phải ghi rõ trong paper:**
- Cận áp dụng cho **tốc độ BMD**, không trực tiếp cho BLER sau LDPC. BLER được kiểm chứng thực nghiệm (E2).
- Hằng số κ_Λ lớn (Λ = 8 → κ ≈ 69 bit với 64-QAM; Λ = 20 → κ ≈ 173 bit), nên (b) chỉ chặt khi E[1 − g] rất nhỏ trên vùng OOD. Đây là lý do cần ramp h(ρ̂) cho phần (c).
- Cận so với **LMMSE dưới cùng điều kiện ước lượng**. Nếu chính LMMSE sụp đổ (vd. 97.2 m/s, Fig. 21), bộ thu lai cũng sụp theo. Từ “bounded” nghĩa là “không tệ hơn mỏ neo”, không phải “không có sàn lỗi”.

### 12.5. Khoảng cách phân bố có nhận biết Doppler (Journal)

- MMD-PDP hiện tại ([T] Eq. 11–13, sau khi sửa chỉ số j ≠ i và tổng thứ hai chạy đến N): đặc trưng p ∈ ℝ^{L} là PDP chuẩn hóa.
- **Đề xuất:** đặc trưng q = [vec(R̂_t), vec(R̂_f)], với R̂_t ∈ ℝ^{T×T} là ma trận tương quan thời gian (trung bình theo f, r) và R̂_f là tương quan tần số (trung bình theo t, r), ước lượng từ kênh thật trong mô phỏng (phân tích offline) hoặc từ Ĥ_LS (online).
- MMD²_TF(𝒟_s, 𝒟_t) dùng cùng ước lượng không chệch, kernel RBF với bandwidth theo median heuristic (thay cho γ = 1.0 cố định của [T]).
- **Mục tiêu kiểm chứng (RQ5):** Spearman(MMD²_TF(s, t), ΔSNR_{s→t}) so với Spearman(MMD²_PDP(s, t), ΔSNR_{s→t}).

### 12.6. Metric tổng hợp OOD

- SNR yêu cầu: S_X(c, β) = Eb/N0 nhỏ nhất để BLER ≤ β của bộ thu X ở ô c = (CDL, v).
- **Worst-case gap:** Γ_X = max_{c ∈ 𝒪} [S_X(c, β) − S_B0(c, β)], β = 10⁻². Nếu X không đạt β trong dải SNR, gán S_X = +∞ và báo cáo riêng.
- **In-distribution gain:** G_X = S_B0(c₀, β) − S_X(c₀, β) tại ô huấn luyện c₀.

---

## 13. Dataset & Data Strategy

Tất cả dữ liệu là **synthetic**, sinh theo batch bằng Sionna (3GPP TR 38.901 CDL). Không có dataset công khai cố định; dữ liệu được định nghĩa bởi `config.yaml` + seed.

| Tập | Nguồn | Nhiệm vụ | Kích thước | Định dạng | Nhãn | Split / seed | Hạn chế | Vai trò |
|---|---|---|---|---|---|---|---|---|
| Development (P0) | Sionna CDL-C, v = 0 m/s | Train backbone (tái lập stress test của [T]) | Sinh online, batch 128 × số bước (theo pilot) | Tensor Y, Ĥ_LS, x̂, mask, N₀ | Bit thông tin b | seed 1000–1999 | Chỉ NLOS, 1 delay spread | Train |
| Development (P1) | CDL-C, v ~ U[0, 10] m/s | Train backbone cho E1 (trong miền) | như trên | như trên | b | seed 2000–2999 | — | Train |
| Validation | CDL-C, v như train | Chọn checkpoint, early stopping | 2000 slot/điểm SNR | — | b | seed 3000–3999 | — | Model selection |
| Calibration 𝒞 | CDL-A, CDL-C; v ∈ {0, 10, 20} | Train gate (Stage 2) | 20k slot | — | b | seed 4000–4999 | — | Gate |
| Test OOD | CDL-A..E × v ∈ {0, 10, 20, 30, 40, 60, 97.2} | Đánh giá cuối | Dừng ở 100 block error hoặc 5×10⁴ slot/điểm | — | b | seed 9000–9999 | SIMO, không impairment RF | **Chỉ dùng một lần** cho kết quả paper |
| External (Journal) | TDL-A/C (38.901), 16-QAM R=0.5 | Tổng quát hóa | như trên | — | b | seed 10000+ | — | Generalization |

**Tham số chung (theo [T] Table A.2, cần xác minh D7, D9):** f_c = 3.5 GHz, SCS 30 kHz, 14 symbol/slot, 6 RB = 72 subcarrier, DMRS symbol {2, 11}, LDPC 5G NR, 64-QAM R = 0.9 (chính), 4-QAM R = 0.5 (phụ).

**Delay spread:** chọn một quy ước duy nhất và ghi vào paper. *Đề xuất:* giữ 100 ns cho mọi CDL như Table 8–11 nếu code xác nhận; thêm quét {30, 100, 300} ns ở journal (E8).

**Bias đã biết:** link-level, SIMO, kênh CDL có cấu trúc cụm cố định; không có CFO, phase noise, IQ imbalance (nằm ngoài phạm vi theo [R3] §1). Không kết luận gì về hiệu năng trên dữ liệu đo thực.

---

## 14. Simulation / Software-Only Strategy

- 100% nghiên cứu chạy bằng mô phỏng Sionna + PyTorch trên Colab T4. Không có thành phần phần cứng trong critical path.
- Không dùng USRP/FPGA/Jetson. Benchmark TensorRT/Jetson mà [R1], [R3] đề xuất cho journal được chuyển thành **future work** (không thuộc roadmap này).
- Latency chỉ báo cáo trên T4 với phương pháp đo rõ ràng (warm-up, batch 1 và batch 128, có/không khâu LMMSE). Không tuyên bố “real-time” vì 7.0 ms > slot 0.5 ms ([T] Fig. 31, Table A.2).
- Tái lập: Git repo, `config.yaml` duy nhất, seed cố định cho cả TensorFlow/PyTorch/NumPy, log kết quả dạng CSV/Parquet, mỗi hình trong paper sinh bằng một script `plots/figX.py`.

---

## 15. Baseline Strategy

| Baseline | Tham chiếu | Dữ liệu | Code | Cấu hình | Độ khó | Metric | Hạn chế kỳ vọng | Vai trò |
|---|---|---|---|---|---|---|---|---|
| B0 LS-LMMSE | Sionna; [T] Obj. 1 | Như test | Sionna `LSChannelEstimator` + `LMMSEEqualizer` | **Xác minh** kiểu nội suy (nn / lin / lin_time_avg) | Thấp | S(c, β) | Sàn lỗi khi Doppler cao | Mỏ neo, tham chiếu Γ |
| B1 Perfect CSI | Sionna | Như test | có sẵn | — | Thấp | S(c, β) | Không triển khai được | Cận trên |
| M1 DeepRx-đúng | Honkala et al., [arXiv:2005.01494](https://arxiv.org/pdf/2005.01494) | P0 | Sionna NRX tutorial / tự viết theo paper | 11 ResNet block, ~1.2M params; đầu vào Y, X_p, Ĥ_raw | Trung bình | S, params, FLOPs | Receptive field cục bộ | Baseline CNN công bằng |
| M1′ CNN-[T] | [T] | P0 | Code [T] | 13.35M | Thấp (đã có) | như trên | — | Liên kết với luận văn |
| M2 Axial-thô | Yellapragada et al., [arXiv:2510.12941](https://arxiv.org/html/2510.12941v2) | P0 | Bỏ đặc trưng LS/LMMSE khỏi M4 | Cùng backbone | Thấp | như trên | Không có prior giải tích | Ablation kiến trúc |
| M3 LS-Axial | Ablation | P0 | Bỏ x̂_LMMSE khỏi M4 | Cùng backbone | Thấp | như trên | — | Ablation đầu vào |
| Symbol-gate | [R3] Ý TƯỞNG-03 | P0 | Biến thể M5 | — | Thấp | Γ | Không có cận | Ablation E4 |
| Hard-switch | Obeed & Jian, [arXiv:2509.18574](https://arxiv.org/html/2509.18574) | P0 | Tự cài đơn giản (discriminator nhỏ hoặc ngưỡng) | per-slot | Trung bình | Γ, G | Gián đoạn, không mềm | So với prior art gần nhất |

**Quy tắc công bằng:** mọi NRX dùng cùng protocol train, cùng số bước tối ưu (hoặc cùng ngân sách GPU), cùng chọn checkpoint theo validation, cùng lưới test. Không dùng số liệu của Yellapragada et al. trực tiếp vì cấu hình khác (64-QAM R = 0.5/0.67, train 0–50 m/s).

---

## 16. Computational Plan

Tài nguyên cố định: Colab NVIDIA T4 (16 GB VRAM). Không mua thêm.

### 16.1. Pilot benchmark (Sprint 1, bắt buộc)

```text
M4 backbone, 64-QAM R=0.9, CDL-C, batch 128
  ↓ train 2,000 bước → đo: s/bước, VRAM đỉnh, BCE validation
  ↓ eval 1 điểm SNR đến 100 lỗi → đo: slot/s cho B0, M4, M5
  ↓ ngoại suy ngân sách theo công thức 16.2
  ↓ quyết định kích thước lưới test (đầy đủ hoặc rút gọn)
```

### 16.2. Ngân sách (công thức; giá trị điền sau pilot)

| Hạng mục | Số lượng | Thời gian đơn vị | GPU-giờ |
|---|---|---|---|
| Train NRX conference (M1, M2, M3, M4) × 3 seed (P0) | 12 | t_train `TBD` | 12·t_train |
| Train NRX trong miền (P1) M1–M4 × 1 seed | 4 | t_train | 4·t_train |
| Gate calibration M5 (và biến thể E4) | ~8 | ≈ 0.1·t_train (ước tính) | 0.8·t_train |
| Eval lưới OOD: 7 bộ thu × 35 ô × ~8 điểm SNR (tìm S(c, 10⁻²) bằng bisection) | ~2,000 điểm | t_eval `TBD` | 2000·t_eval |
| Journal E6: train 10 miền nguồn × 1 seed | 10 | t_train | 10·t_train |

**Ngưỡng quyết định (Gate 3):** nếu tổng conference > 60 GPU-giờ, rút lưới test còn CDL {A, C, D} × v {0, 10, 20, 40, 97.2} và giảm seed còn 2 cho M2/M3. *Lý do:* Colab có giới hạn phiên; ~60 GPU-giờ trong 4 tuần là mức có thể chạy song song với việc viết.

### 16.3. Thực hành Colab

- Checkpoint mỗi N bước lên Google Drive; script resume.
- Một notebook = một thí nghiệm; tham số đọc từ `config.yaml`.
- Mixed precision (FP16 autocast) cho train nếu không làm mất ổn định (đã được [T] Table 13 đề xuất).

---

## 17. Web App Demo

**Vai trò:** demonstrator cho đóng góp A1–A2 (cổng chuyển dần sang LMMSE khi Doppler tăng). Không phải đóng góp khoa học.

```text
Gradio UI ──► FastAPI-free (gọi trực tiếp Python) ──► rx_service.py
   │  chọn: CDL {A..E}, v (0–100 m/s), Eb/N0, MCS, bộ thu {B0, M4, M5}
   ▼
sim_slots(n = 64–256 slot, seed) ──► B0 / M4 / M5 inference ──► kết quả
   ▼
Hiển thị: (1) BLER ước lượng nhanh + CI; (2) g trung bình và ρ̂; (3) histogram ℓ_A, ℓ_N, ℓ_H;
          (4) chòm sao x̂_LMMSE; (5) đường BLER đầy đủ lấy từ cache kết quả paper (Parquet)
```

| Thành phần | File | Ghi chú |
|---|---|---|
| UI | `demo/app.py` | Gradio Blocks, 1 trang |
| Service | `demo/rx_service.py` | Load checkpoint M4/M5 (CPU/GPU) |
| Cache | `results/*.parquet` | Sinh từ E2; đảm bảo demo khớp số liệu paper |
| Chạy | Colab (GPU) hoặc máy cá nhân (CPU, n slot nhỏ) | Không cần server riêng |

**Demo success criteria:** (1) chạy end-to-end trong ≤ 30 s/lần trên Colab T4; (2) gọi M5 thật; (3) khi kéo v từ 0 → 97.2 m/s, g tăng và BLER của M5 không vượt đáng kể BLER của B0 (khớp E2); (4) đường cong cache trùng hình trong paper; (5) có nút “Reproduce Fig. X”.

Thời gian tối đa dành cho demo: **3 ngày công** (S4) + 2 ngày (S8).

---

## 18. Evaluation Framework

| Metric | Định nghĩa | RQ phục vụ | Lý do chọn |
|---|---|---|---|
| BLER | Tỷ lệ transport block lỗi sau LDPC | Tất cả | Metric chuẩn 3GPP của [T] |
| S(c, β) | Eb/N0 cần để BLER ≤ β, β ∈ {10⁻², 10⁻³} | RQ1–RQ3 | So sánh dB thay vì nhìn đường cong |
| Γ (worst-case gap) | max trên ô OOD của S_X − S_B0 | RQ2, RQ3 | Đo trực tiếp ý nghĩa “bounded” |
| G (in-dist gain) | S_B0 − S_X tại ô huấn luyện | RQ1, RQ3 | Đo cái giá của an toàn |
| R_BMD | Mục 12.3, ước lượng Monte Carlo | RQ3 | Kiểm chứng Mệnh đề 1 bằng số |
| ḡ(v), ḡ(CDL) | Trung bình cổng theo ô | RQ3, RQ4 | Giải thích hành vi cổng |
| Spearman/Pearson | Giữa MMD và ΔS | RQ5 | Năng lực dự báo của khoảng cách |
| Params, FLOPs, latency T4 | thop/fvcore + đo thời gian (warm-up 50, lặp 500) | RQ1, G4 | Đánh đổi hiệu quả |

**Rigor thống kê:**
- BLER: khoảng tin cậy 95% Clopper–Pearson; dừng ở ≥ 100 block error hoặc 5×10⁴ slot.
- Seeds huấn luyện: 3 seed cho M1, M4, M5 (bảng chính); 2 seed cho M2, M3 nếu Gate 3 yêu cầu rút gọn. Báo cáo S(c, β) dạng trung bình ± độ lệch chuẩn qua seed.
- Không chọn seed tốt nhất. Mọi seed được báo cáo.
- So sánh “có ý nghĩa” chỉ khi chênh lệch vượt 2 × độ lệch chuẩn giữa seed.

---

## 19. Experiment Matrix

| ID | Thí nghiệm | Train | Test | Bộ thu | RQ | Bằng chứng tạo ra | Paper | Sprint |
|---|---|---|---|---|---|---|---|---|
| **E0** | Tái lập [T] | P0 (CDL-C, 0 m/s) | CDL-C/D × {10, 40} m/s | B0, B1, M1′, M4 | Tiền đề | Fig. 23–26 có seed + CI; xác nhận D1–D3 | Conf. (bối cảnh) | S1 |
| **E1** | Ablation trong miền | P1 | CDL-C × {0, 10} | B0, B1, M1, M1′, M2, M3, M4, M5 | RQ1 | Bảng ablation (S, params, FLOPs) | Conf. Table I | S2–S3 |
| **E2** | Lưới OOD | P0 | 5 CDL × 7 v | B0, B1, M1, M2, M3, M4, M5 | RQ2, RQ3 | Heatmap Γ; Fig. BLER chọn lọc | Conf. Fig. 2–3 | S3 |
| **E3** | Phân tích cổng + kiểm chứng Mệnh đề 1 | P0 | Lưới E2 | M5 | RQ3 | ḡ(v), R_BMD(ℓ^H) ≥ cận | Conf. Fig. 4 | S3–S4 |
| **E4** | Biến thể cổng | P0 | Lưới E2 | M5-free, M5-ramp, M5-symbol, Hard-switch, g_min | RQ3, RQ4 | Bảng ablation cổng | Conf. Table II | S3–S4 |
| **E5** | Độ phức tạp | — | — | M1, M1′, M2–M5 | RQ1 | Params, FLOPs (có/không LMMSE), latency T4 | Conf. Table I | S2 |
| **E6** | Ma trận lệch miền | 10 nguồn: CDL {A..E} × v {0, 30} | 35 ô | M5 backbone | RQ5 | ΔS cho 10 × 35 cặp | Journal | S5–S6 |
| **E7** | MMD-TF vs MMD-PDP | — | Dữ liệu E6 | — | RQ5 | Spearman, scatter | Journal | S6 |
| **E8** | Tổng quát hóa | P0 | TDL-A/C; 16-QAM R = 0.5; delay spread {30, 100, 300} ns | B0, M4, M5 | RQ3 | Γ trên điều kiện mới | Journal | S6–S7 |
| **E9** | Pareto hiệu quả–an toàn | P0 | Lưới E2 | M1, M2, M4, M5 × N ∈ {2, 4, 6} | G4 | Đồ thị FLOPs vs Γ | Journal | S7 |
| **E10** | Lệch ước lượng nhiễu | P0 | N̂₀ sai lệch ±3 dB | B0, M4, M5 | RQ3 | Độ nhạy cổng với N̂₀ | Journal | S7 |
| E11 | MMD-driven gate | P0 | Lưới E2 | M5 + đặc trưng MMD-TF online | RQ5 | Γ, G so với ρ̂-gate | Journal | S7 |
| E12 | MIMO 2×2 | — | — | — | — | — | `OPTIONAL` (chỉ khi S7 dư ≥ 1 tuần) | — |

---

## 20. Algorithm Development Plan

| Version | Vấn đề giải quyết | Hypothesis | Thay đổi thuật toán | Thay đổi toán | Cải thiện kỳ vọng | Thí nghiệm | Tiêu chí thành công |
|---|---|---|---|---|---|---|---|
| v0 — Baseline verify | Không chắc kết quả [T] tái lập được | — | Không | Không | — | E0 | Fig. 23 và 25 tái lập trong ±1 dB tại BLER 10⁻² |
| v1 — Fair baselines | Baseline CNN bị làm yếu | H1 | Thêm M1, M2, M3 | — | Bảng attribution trung thực | E1, E5 | Mọi mô hình hội tụ (val BCE ổn định); ablation đủ 3 seed |
| v2 — LLR gate (free) | Concatenation không bound | H3a | ℓ^H = gℓ^A + (1−g)ℓ̄^N, g học tự do | Mệnh đề 1 (a, b, d) | Γ giảm so với M4 | E2, E3 | Γ_M5 < Γ_M4 |
| v3 — LLR gate + ramp vật lý | Gate tự do học g ≈ 0 ngoài miền | H3b, H4 | g = max(σ(a_ψ(φ)), h(ρ̂)) | Mệnh đề 1 (c) | Γ ≤ 1 dB | E2, E4 | Γ_M5 ≤ 1 dB **và** G_M5 ≥ G_M4 − 0.3 dB |
| v4 — Distance-aware gate (Journal) | ρ̂ chỉ bắt Doppler, không bắt lệch LOS | H5 | Thêm đặc trưng MMD-TF online vào φ | §12.5 | Γ giảm thêm trên CDL-D/E | E11 | Γ_v4 < Γ_v3 trên ô LOS |

Không phát triển thêm version nào ngoài bảng này trong 4 tháng.

---

## 21. Model Development Plan

| Hạng mục | Kế hoạch | Gắn với hypothesis |
|---|---|---|
| Kiến trúc | Giữ backbone của [T] (sau khi xác minh D6–D8). Không đổi Post-LN → Pre-LN trừ khi train không ổn định | Tránh confound với H1, H3 |
| Đầu vào | M1: (Y, X_p, Ĥ_raw); M2: Y; M3: Y, Ĥ_LS; M4/M5: Z theo code | H1 |
| Loss | BCE trên LLR (= tối đa R_BMD); Stage 2 thêm λE[g] với λ ∈ {0, 10⁻³, 10⁻²} | H3 |
| Training | Adam lr 10⁻⁴, batch 128, Eb/N0 ~ U[0, 20] dB (thống nhất D13); early stopping theo val BCE | — |
| LLR clipping | Λ ∈ {8, 12, 20}, mặc định 12 | Mệnh đề 1 (b) |
| Augmentation | Không dùng augmentation vận tốc cho P0 (giữ tính “stress test”); P1 dùng v ~ U[0, 10] | Tách training coverage khỏi structural safety |
| Ablation mô hình | M1–M5 + biến thể cổng E4 | H1, H3, H4 |
| Độ phức tạp | Báo cáo FLOPs **gồm** và **không gồm** LMMSE + demapper | Trung thực về chi phí |
| Latency | T4, batch 1 và 128, warm-up 50, 500 lần lặp, trung bình ± std | Không tuyên bố real-time |

---

## 22. Conference Roadmap (tháng 1–2)

### 22.1. Đóng góp conference

```text
C1. Fair attribution: bảng ablation 5 nhánh + DeepRx-đúng (RQ1)
C2. Empirical insight: concatenating an LMMSE prior does not bound OOD error (RQ2)
C3. LLR-domain convex gate + physics ramp, với Mệnh đề 1 (BMD-rate floor) (RQ3)
C4. Lưới OOD 5 CDL × 7 vận tốc có CI (RQ2, RQ3)
```

### 22.2. Dàn ý paper (IEEE conference, 5 trang + tối đa 2 trang trả phí theo quy định VTC)

| Mục | Nội dung | Nguồn bằng chứng | Độ dài |
|---|---|---|---|
| I. Introduction | Vấn đề an toàn OOD; prior art (DeepRx, Yellapragada, hybrid switch, rollback); C1–C4 | Mục 4–5 | 0.75 trang |
| II. System Model | Eq. 12.1–12.3 | Mục 12 | 0.5 trang |
| III. Proposed Receiver | Backbone, gate, ramp, Mệnh đề 1 + chứng minh ngắn | Mục 9–12 | 1.25 trang |
| IV. Simulation Setup | Bảng tham số, protocol P0/P1, Monte Carlo | Mục 13, 18 | 0.5 trang |
| V. Results | Table I (ablation + complexity), Fig. 2 (heatmap Γ), Fig. 3 (BLER CDL-C/D × 10/40 m/s), Fig. 4 (ḡ theo v), Table II (biến thể cổng) | E1–E5 | 1.75 trang |
| VI. Conclusion | Giới hạn: BMD ≠ BLER; SIMO; synthetic | — | 0.25 trang |

### 22.3. Đầu ra bắt buộc tại 29/11/2026 (Gate 5)

- Bản thảo LaTeX IEEEtran hoàn chỉnh, đã qua review nội bộ 1 vòng.
- Repo có tag `conf-v1`, mọi hình sinh lại bằng 1 lệnh.
- Web demo chạy được (Mục 17).
- Bảng kết quả có CI và đủ seed.

---

## 23. Journal Extension Roadmap (tháng 3–4)

```text
Conference Contribution  (C1–C4: gated LMMSE-Axial NRX + BMD-rate floor)
        +
New Scientific Contribution
   J1. Doppler-aware distribution distance (MMD-TF) — dự báo suy giảm lệch miền (RQ5)
   J2. Distance-aware gate (v4) — dùng MMD-TF online để mở rộng an toàn sang lệch LOS/delay spread
   J3. Phân tích lý thuyết: cận cho trường hợp g phụ thuộc dữ liệu có lỗi ước lượng ρ̂ (xác suất fallback sai theo SNR)
        +
Additional Evidence
   E6–E11: ma trận 10 × 35 cặp miền, TDL, 16-QAM, delay spread, Pareto FLOPs–Γ, lệch N̂₀
        =
Journal Contribution
```

**Vì sao đây không phải “conference + thêm thí nghiệm”:** J1 là một biểu diễn và một công cụ dự báo mới, kiểm chứng được bằng tương quan; J2 là một cơ chế mới dựa trên J1; J3 mở rộng Mệnh đề 1. Nếu bỏ toàn bộ thí nghiệm mới, J1–J3 vẫn là nội dung khoa học độc lập.

**Thứ tự ưu tiên khi thiếu thời gian:** J1 + E6 + E7 (bắt buộc) → J3 (lý thuyết, chi phí GPU thấp) → J2 + E11 → E8–E10. E12 (MIMO) là `OPTIONAL`.

**Dàn ý journal (IEEE TCCN/TVT, ~12–14 trang 2 cột):** Intro → Related work (NRX, hybrid, domain generalization trong wireless) → System model → Gated receiver + Mệnh đề 1 + mở rộng J3 → Doppler-aware MMD (J1) → Distance-aware gate (J2) → Setup → Results (E2–E11) → Discussion (giới hạn, khả năng triển khai) → Conclusion.

---

## 24. Biweekly Sprint Plan

**Cấu trúc repo dùng chung cho mọi sprint**

```text
nrx-bounded/
├── config/config.yaml              # nguồn tham số duy nhất (writing-as-code, [R1] §2.3)
├── src/sim/channels.py             # make_cdl(model, v, delay_spread, seed)
├── src/sim/link.py                 # transmitter, LDPC, resource grid, batch generator
├── src/rx/classical.py             # B0 (LS-LMMSE), B1 (Perfect CSI), demap_lmmse() -> ℓ_A
├── src/rx/features.py              # build_Z(), rho_hat(), pilot_residual()
├── src/models/axial.py             # AxialBlock, AxialNRX (M2, M3, M4 qua cờ input_set)
├── src/models/deeprx.py            # DeepRx 11 ResNet blocks (M1), CNN-[T] (M1′)
├── src/models/gate.py              # GateMLP, physics_ramp(), combine_llr()
├── src/train/train_backbone.py     # Stage 1
├── src/train/train_gate.py         # Stage 2
├── src/eval/sweep.py               # bisection tìm S(c,β), dừng 100 lỗi, Clopper–Pearson
├── src/eval/metrics.py             # S, Γ, G, R_BMD
├── src/analysis/mmd.py             # MMD² không chệch; đặc trưng PDP và TF
├── src/complexity/profile.py       # params, FLOPs, latency
├── plots/figX_*.py                 # mỗi hình paper = 1 script
├── demo/app.py, demo/rx_service.py
└── tests/                          # pytest
```

---

### Sprint 1 — 05/10 → 18/10/2026 · Reproduce, Verify, Literature

**Objective:** Xác nhận tiền đề: code tồn tại, kết quả [T] tái lập được, gap G1 còn mở, ngân sách GPU khả thi.

**Research tasks**
- Literature search có hệ thống (IEEE Xplore, arXiv 2023–2026). Từ khóa: *neural receiver fallback*, *hybrid neural classical receiver*, *model-based deep learning receiver guarantee*, *LLR fusion convex*, *safe neural receiver out-of-distribution*, *LMMSE aided neural receiver*, *domain generalization channel MMD Doppler*. Đọc kỹ: arXiv:2509.18574, 2605.26157, 2608.02172, 2510.12941, 2409.02912, Zenodo 22994791.
- Viết bảng “closest prior art” (≥ 10 bài) với cột: fusion domain, có bound không, OOD protocol.

**Algorithm/Model tasks**
- Đọc code, chốt D6–D9, D13 vào `config.yaml`.
- Xác định kiểu nội suy LS và cách tính LMMSE (single-tap vs 2D Wiener như App. C).

**Coding tasks**
| Module | Hàm/lớp | Input → Output | Test |
|---|---|---|---|
| `src/sim/channels.py` | `make_cdl()` | (model, v, ds, seed) → Sionna channel | `test_cdl_seed_determinism` |
| `src/rx/classical.py` | `b0_receiver()`, `demap_lmmse()` | Y → ℓ_A | So khớp BLER với Fig. 23 (đường LS) |
| `src/rx/features.py` | `rho_hat()` | Ĥ_LS → ρ̂ | `test_rho_hat_vs_jakes` (sai số ≤ 0.05 với v ∈ {0, 10, 40, 97.2}) |
| `src/eval/sweep.py` | `bler_point()`, `clopper_pearson()` | (rx, c, snr) → (BLER, CI) | `test_ci_bounds` |

**Data/Simulation:** Chạy E0 (B0, B1, M1′, M4; P0; CDL-C/D × 10, 40 m/s) với 1 seed. Pilot benchmark (Mục 16.1).

**Evaluation:** S(c, 10⁻²) cho 4 ô; so với đồ thị [T].
**Expected results:** Tái lập Fig. 23, 25 trong ±1 dB; xác nhận hoặc bác bỏ D1–D2.
**Deliverables:** Repo Git + `config.yaml`; báo cáo 2 trang “Reproduction & Discrepancy Note”; bảng prior art; số đo pilot (s/bước, VRAM, slot/s).
**Milestone:** **Gate 1** (16/10).
**Risk & Plan B:** Code mất/không chạy → dựng lại pipeline từ Sionna tutorial (NRX) + backbone theo Eq. 1–10, mất thêm 1 tuần; giảm E4 xuống 2 biến thể.

---

### Sprint 2 — 19/10 → 01/11/2026 · Fair Baselines & Theory Draft

**Objective:** Có baseline công bằng (RQ1) và bản chứng minh Mệnh đề 1.

**Research tasks:** Viết chứng minh đầy đủ Mệnh đề 1 (a)–(d) trong LaTeX; cố vấn rà soát.
**Algorithm/Model tasks:** Cài M1 (DeepRx-đúng, ~1.2M params), M2, M3; giữ M4.

**Coding tasks**
| Module | Hàm/lớp | Input → Output | Test |
|---|---|---|---|
| `src/models/deeprx.py` | `DeepRx` | (Y, X_p, Ĥ_raw) → ℓ_N | `test_deeprx_params` (1.1M–1.3M) |
| `src/models/axial.py` | `AxialNRX(input_set=...)` | Z → ℓ_N | `test_shapes_all_input_sets` |
| `src/complexity/profile.py` | `profile(model, with_classical)` | model → params, FLOPs, latency | So khớp 1,213,318 params của [T] |
| `src/train/train_backbone.py` | `train()` | config → checkpoint | Smoke test 200 bước |

**Data/Simulation:** Train M1–M4 trên P1 (1 seed) và P0 (seed 1 của 3).
**Evaluation:** E1 sơ bộ; E5 đầy đủ.
**Expected results:** Bảng params/FLOPs có/không LMMSE; S(c₀, 10⁻²) của M1–M4 trong miền.
**Deliverables:** Table I bản nháp; chứng minh Mệnh đề 1 (PDF 2 trang); checkpoint M1–M4.
**Milestone:** **Gate 2** (Prototype) và **Gate 3** (Computational) — 30/10.
**Risk & Plan B:** M1 không hội tụ trong ngân sách → dùng NRX Sionna tutorial làm CNN baseline và ghi rõ trong paper; nếu chứng minh có lỗi → giữ (a) và (c), bỏ (b).

---

### Sprint 3 — 02/11 → 15/11/2026 · Gated Receiver & OOD Grid

**Objective:** Kiểm chứng H2, H3 (cốt lõi conference).

**Research tasks:** Phân tích kết quả E2 theo từng ô; xác định ô nào M4 vi phạm bound.
**Algorithm/Model tasks:** Cài v2 (gate tự do) và v3 (gate + ramp).

**Coding tasks**
| Module | Hàm/lớp | Input → Output | Test |
|---|---|---|---|
| `src/models/gate.py` | `GateMLP`, `physics_ramp()`, `combine_llr()` | (φ, ℓ_A, ℓ_N) → (g, ℓ_H) | `test_bce_convexity` (BCE(ℓ_H) ≤ gBCE(ℓ_A) + (1−g)BCE(ℓ_N), 10⁶ mẫu ngẫu nhiên); `test_ramp_monotone` |
| `src/train/train_gate.py` | `calibrate_gate()` | checkpoint θ, 𝒞 → ψ | Smoke test |
| `src/eval/metrics.py` | `gamma_worst()`, `rbmd()` | kết quả sweep → Γ, R_BMD | `test_rbmd_perfect_llr` (R → m) |

**Data/Simulation:** Train seed 2–3 cho M1, M4 (P0); calibrate M5; chạy E2 (lưới đầy đủ hoặc rút gọn theo Gate 3); E3.
**Evaluation:** Γ, G cho M1–M5; ḡ(v); R_BMD thực nghiệm so với cận (b).
**Expected results:** H2 được xác nhận (≥ 1 ô Γ_M4 > 3 dB); M5 đạt Γ ≤ 1 dB (H3b) — **chưa biết**, đây là điểm quyết định.
**Deliverables:** Heatmap Γ (Fig. 2), BLER chọn lọc (Fig. 3), ḡ(v) (Fig. 4), log thí nghiệm.
**Milestone:** **Gate 4** (Conference Research) — 13/11.
**Risk & Plan B:** M5 không đạt Γ ≤ 1 dB → (i) quét ρ_hi, ρ_lo, Λ; (ii) chuyển gate sang per-RE; (iii) nếu vẫn thất bại, đổi khung paper sang “negative result + analysis” (tiêu đề dự phòng Mục 7.4).

---

### Sprint 4 — 16/11 → 29/11/2026 · Conference Paper & Demo

**Objective:** Bản thảo conference hoàn chỉnh, đóng băng kết quả.

**Research tasks:** Viết đủ 6 mục paper; review nội bộ với cố vấn (1 vòng, 3 ngày).
**Algorithm/Model tasks:** Chạy E4 (free / ramp / symbol-gate / hard-switch / g_min).

**Coding tasks**
| Module | Hàm/lớp | Input → Output | Test |
|---|---|---|---|
| `plots/fig*.py` | 1 script/hình | Parquet → PDF | Chạy lại toàn bộ bằng `make figures` |
| `demo/app.py`, `demo/rx_service.py` | Gradio UI, `run_demo()` | config UI → hình + số | Demo checklist Mục 17 |

**Data/Simulation:** E4; bổ sung 10⁻⁴ cho 2–3 đường tiêu biểu nếu ngân sách cho phép.
**Evaluation:** Table II (biến thể cổng).
**Expected results:** LLR-gate tốt hơn symbol-gate về Γ (kiểm chứng lựa chọn Mục 9.3).
**Deliverables:** `paper_conf_v1.pdf` (IEEEtran), repo tag `conf-v1`, demo chạy được.
**Milestone:** **Gate 5** (Conference Readiness) — 27/11.
**Risk & Plan B:** Viết chậm → cắt Fig. 4 thành 1 subplot, chuyển Table II thành 1 đoạn văn; demo chỉ giữ chức năng (1)–(3).

---

### Sprint 5 — 30/11 → 13/12/2026 · Journal: Doppler-aware Distance

**Objective:** Cài J1 và bắt đầu E6.

**Research tasks:** Hoàn chỉnh định nghĩa MMD-TF; median heuristic; phân tích tại sao PDP không chứa Doppler (viết thành đoạn có công thức).
**Algorithm/Model tasks:** Đặc trưng R̂_t, R̂_f từ kênh mô phỏng và từ Ĥ_LS.

**Coding tasks**
| Module | Hàm/lớp | Input → Output | Test |
|---|---|---|---|
| `src/analysis/mmd.py` | `mmd2_unbiased()`, `pdp_features()`, `tf_corr_features()` | mẫu kênh → MMD² | `test_mmd_zero_same_dist`, `test_mmd_symmetry`; tái tạo Table 3 của [T] |

**Data/Simulation:** Train 5 / 10 mô hình nguồn E6 (M5 backbone, 1 seed).
**Evaluation:** MMD-PDP và MMD-TF cho 10 × 35 cặp.
**Expected results:** MMD-PDP không đổi theo v (khớp Table 3 ≡ Table 4); MMD-TF tăng đơn điệu theo |Δv|.
**Deliverables:** Bảng MMD mới; 5 checkpoint nguồn; technical note J1.
**Milestone:** **Gate 6** (Journal Extension) — 11/12.
**Risk & Plan B:** MMD-TF không tách được các miền → thử đặc trưng scattering function (delay–Doppler) rút gọn; nếu vẫn thất bại, đổi J1 thành “phân tích giới hạn của MMD-PDP” và đẩy trọng tâm journal sang J3 + E8–E10.

---

### Sprint 6 — 14/12 → 27/12/2026 · Journal: Cross-domain Matrix & Generalization

**Objective:** Hoàn thành E6, E7, E8.

**Research tasks:** Phân tích tương quan; kiểm định ý nghĩa (permutation test cho Spearman).
**Algorithm/Model tasks:** —
**Coding tasks:** `src/analysis/correlate.py` (`spearman_perm_test()`); mở rộng `channels.py` cho TDL-A/C và delay spread.
**Data/Simulation:** Train 5 mô hình nguồn còn lại; eval 10 × 35; E8 (TDL, 16-QAM, delay spread).
**Evaluation:** Spearman/Pearson MMD-TF vs MMD-PDP; Γ trên E8.
**Expected results:** H5 được xác nhận hoặc bác bỏ có định lượng.
**Deliverables:** Fig. scatter MMD vs ΔS; bảng E8.
**Milestone:** Kết quả J1 đóng băng (24/12).
**Risk & Plan B:** Thiếu GPU-giờ → giảm nguồn E6 còn 6 (CDL {A, C, D} × v {0, 30}); E8 chỉ giữ TDL-C + 16-QAM.

---

### Sprint 7 — 28/12/2026 → 10/01/2027 · Journal: Distance-aware Gate & Theory

**Objective:** J2, J3, E9, E10, E11.

**Research tasks:** J3 — cận khi ρ̂ có lỗi ước lượng: xác suất fallback sai P(h(ρ̂) < 1 | v ≥ v_lo) theo SNR (xấp xỉ Gauss của ρ̂).
**Algorithm/Model tasks:** v4 — thêm MMD-TF online vào φ.
**Coding tasks:** `features.py::online_tf_distance()`; mở rộng `gate.py`; `profile.py` cho N ∈ {2, 4, 6}.
**Data/Simulation:** E9 (train M4/M5 với N = 2, 4), E10, E11.
**Evaluation:** Pareto FLOPs–Γ; độ nhạy N̂₀; Γ_v4 vs Γ_v3.
**Expected results:** v4 giảm Γ trên ô LOS (H5 mở rộng); Pareto cho thấy cổng giữ Γ thấp ở mọi kích thước.
**Deliverables:** Phụ lục chứng minh J3; Fig. Pareto; bảng E10–E11.
**Milestone:** Toàn bộ kết quả journal đóng băng (10/01).
**Risk & Plan B:** v4 không cải thiện → báo cáo như kết quả âm có phân tích; giữ v3 làm phương pháp chính.

---

### Sprint 8 — 11/01 → 24/01/2027 · Journal Paper

**Objective:** Bản thảo journal hoàn chỉnh; chuẩn bị nộp conference.

**Research tasks:** Viết journal (12–14 trang); review nội bộ 2 vòng; kiểm tra chính sách trùng lặp conference–journal của venue đích.
**Coding tasks:** Tag `journal-v1`; README tái lập; cập nhật demo với v4 và cache E6–E11.
**Evaluation:** Rà soát mọi số trong paper khớp Parquet (script `check_numbers.py`).
**Deliverables:** `paper_journal_v1.pdf`, cover letter, repo công khai (hoặc sẵn sàng công khai), demo v2.
**Milestone:** **Gate 7** (Journal Readiness) — 22/01.
**Buffer 25–31/01:** Định dạng lần cuối và nộp conference (VTC2027-Fall, hạn 01/02/2027). Journal nộp theo Mục 28.3.
**Risk & Plan B:** Chậm → nộp conference đúng hạn, lùi journal 2–3 tuần (không ảnh hưởng hạn conference).

---

## 25. Milestones & Feasibility Gates

| Gate | Ngày | Điều kiện GREEN | YELLOW | RED → hành động |
|---|---|---|---|---|
| **G1 Research & Novelty** | 16/10 | Code chạy; Fig. 23/25 tái lập ±1 dB; không tìm thấy bài có LLR-gate + bound; pilot cho thấy ≤ 60 GPU-giờ | Tái lập ±2 dB; có bài gần nhưng khác cơ chế | Không tái lập được hoặc đã có bài trùng → Plan B Mục 27 (R1, R2) |
| **G2 Prototype** | 30/10 | M1–M4 hội tụ; E1 sơ bộ; chứng minh Mệnh đề 1 được cố vấn duyệt | 1 baseline chưa hội tụ | M4 không tái lập được → dừng gate, quay lại S1 |
| **G3 Computational** | 30/10 | Ngân sách đo ≤ 60 GPU-giờ cho conference | 60–90 GPU-giờ → lưới rút gọn | > 90 GPU-giờ → giảm protocol còn CDL {C, D} × v {10, 40, 97.2}, 2 seed |
| **G4 Conference Research** | 13/11 | H2 xác nhận; Γ_M5 ≤ 1 dB; G_M5 ≥ G_M4 − 0.3 dB | Γ_M5 trong 1–3 dB | Γ_M5 ≥ Γ_M4 → khung “negative result” (Mục 7.4) |
| **G5 Conference Readiness** | 27/11 | Paper đủ mục, mọi hình sinh lại được, demo chạy, đủ seed/CI | Thiếu Table II | Thiếu kết quả chính → lùi 1 tuần, cắt E4 |
| **G6 Journal Extension** | 11/12 | MMD-TF tách miền theo v; ≥ 5 nguồn E6 đã train | Tách yếu | Không tách → chuyển trọng tâm sang J3 + E8–E10 |
| **G7 Journal Readiness** | 22/01 | J1 + (J2 hoặc J3) có bằng chứng; paper đủ; repo sẵn sàng | Thiếu J2 | Thiếu J1 và J3 → không nộp Q1; nộp IEEE Access hoặc lùi |

Người duyệt mọi gate: TS. Huỳnh Võ Trung Dũng. Người chuẩn bị bằng chứng: Vương Thanh Tùng (gửi 2 ngày trước ngày gate).

---

## 26. Critical Path

```text
[S1] Code + tái lập E0 ──► [S1] Pilot GPU ──► [S2] M1–M4 baselines ──► [S3] Gate (v2, v3) ──► [S3] E2 lưới OOD
        │                                          │                         │
        └──► [S1] Literature (song song)            └──► [S2] Chứng minh      └──► [S4] E4 ──► [S4] Paper conf
                                                         Mệnh đề 1 (song song)                    │
                                                                                                  ▼
[S5] MMD-TF (J1) ──► [S5–S6] E6 train 10 nguồn ──► [S6] E7 tương quan ──► [S7] v4 / J3 ──► [S8] Paper journal
```

| Loại | Nội dung |
|---|---|
| Critical tasks | Tái lập E0; M4 checkpoint; gate v3; E2; E6 |
| Phụ thuộc chính | E2 cần M1–M5; E6 cần backbone M5 ổn định; J2 cần J1 |
| Song song được | Literature (S1); chứng minh (S2); demo (S4); viết Intro/Related work (S3–S4, S7) |
| Bottleneck | GPU Colab cho E2 và E6 |
| Buffer | 1 tuần (25–31/01) + Plan B rút lưới ở mỗi sprint |
| Kill criteria | Xem Mục 27 |

---

## 27. Risk & Contingency

| # | Risk | Trigger | Plan A | Plan B | Kill Criteria |
|---|---|---|---|---|---|
| R1 | Không tái lập được [T] | E0 lệch > 2 dB hoặc code thiếu | Debug cấu hình (D6–D9) | Dựng lại pipeline từ Sionna tutorial, coi kết quả [T] là sơ bộ | Đến 23/10 chưa có pipeline chạy → giảm phạm vi conference còn RQ2 + RQ3 trên CDL {C, D} |
| R2 | Novelty yếu | Tìm thấy bài có LLR-domain fusion + bound | Khác biệt hóa bằng ramp vật lý + đánh giá OOD | Chuyển trọng tâm sang A3 + J1 | Có bài trùng cả A1, A2 và A3 |
| R3 | Gate học g ≈ 0 ngoài miền | ḡ(v ≥ 40) < 0.5 với gate tự do | Ramp vật lý h(ρ̂) | Hard floor g_min theo SNR | — (ramp bảo đảm g = 1 theo cấu trúc) |
| R4 | M5 không giữ được Γ ≤ 1 dB | Γ_M5 > 1 dB ở Gate 4 | Quét ρ_hi, ρ_lo, Λ; gate per-RE | Khung negative result | Γ_M5 ≥ Γ_M4 trên đa số ô |
| R5 | Mất lợi ích trong miền | G_M5 < G_M4 − 0.3 dB | Thêm λE[g], hiệu chỉnh bias ρ̂ | Chấp nhận đánh đổi, báo cáo Pareto | — |
| R6 | Baseline M1 không hội tụ | Val BCE không giảm sau 2 ngày | Lr warm-up, kiểm tra input scaling | NRX Sionna tutorial | Không có CNN baseline đáng tin → báo cáo M2 làm baseline chính |
| R7 | Chi phí GPU quá cao | Gate 3 > 90 GPU-giờ | Bisection SNR, lưới rút gọn | 2 seed, bỏ 10⁻⁴ | — |
| R8 | Colab ngắt phiên / mất dữ liệu | Mất checkpoint | Checkpoint lên Drive mỗi N bước | Chạy ban đêm, chia nhỏ job | — |
| R9 | Demo quá phức tạp | > 3 ngày công | Chỉ chức năng (1)–(3) | Notebook tương tác thay Gradio | Demo không gọi được M5 → không đưa demo vào paper |
| R10 | Evidence conference yếu | H2 không xác nhận (M4 không vi phạm bound khi tái lập) | Mở rộng lưới (v = 60, 97.2; CDL-E) | Khung paper sang “efficiency–safety Pareto” (G4) | Không có ô nào vi phạm và không có lợi ích Pareto |
| R11 | Journal novelty yếu | Gate 6 RED | J3 lý thuyết + E8–E10 | Nộp journal Q2 (IEEE Access) hoặc lùi | Không có J1 và J3 |
| R12 | Trùng lặp nộp conference–journal | Chính sách venue cấm review song song | Nộp journal sau khi có kết quả conference | Chọn journal cho phép kèm khai báo | — |
| R13 | Tuyên bố quá mức | Paper dùng “guarantee BLER”, “real-time” | Checklist từ ngữ trước nộp | Cố vấn rà soát | — |

---

## 28. Publication Strategy

> Thông tin dưới đây được kiểm tra ngày 01/10/2026. Hạn nộp và ranking có thể thay đổi; kiểm tra lại trên trang chính thức trước khi nộp. Không có venue nào bảo đảm acceptance.

### 28.1. Conference (rank B trở lên)

| Venue | Ngày & địa điểm | Hạn nộp | Rank | Phù hợp | Khả thi với timeline |
|---|---|---|---|---|---|
| **IEEE VTC2027-Fall** (khuyến nghị) | 27–30/09/2027, Osaka | Regular paper **01/02/2027**; thông báo 14/04/2027 ([VTC2027-Fall](https://events.vtsociety.org/vtc2027-fall/)) | **CORE2023: B** ([ICORE portal](https://portal.core.edu.au/conf-ranks/757/)); trạng thái ICORE2026 `NEEDS VERIFICATION` | Track AI/ML for Communications, Signal Processing for Wireless; chủ đề mobility | ✅ Paper xong 29/11, còn 2 tháng buffer |
| EUSIPCO 2027 (thay thế) | 30/08–03/09/2027, Darmstadt | **06/02/2027** ([eusipco2027.de](https://eusipco2027.de/)) | `NEEDS VERIFICATION` (portal CORE chặn truy cập tự động) | Khung signal processing | ✅ |
| IEEE GLOBECOM 2027 (dự phòng nếu bị từ chối) | 06–10/12/2027, Abu Dhabi ([aconf](https://www.aconf.org/conf_196005.GLOBECOM_2027_-_2027_IEEE_Global_Communications_Conference.html)) | `TBD` — nguồn tổng hợp không đáng tin; kiểm tra trang ComSoc | CORE2023: B ([ICORE portal](https://portal.core.edu.au/conf-ranks/2030/)) | Chủ đề rộng | Chỉ làm phương án sau |
| IEEE ICC 2027 | 30/05–03/06/2027, Washington DC | 02/10/2026 ([beri.net](https://www.beri.net/events/ieee-icc-2027), nguồn thứ cấp) | — | — | ❌ Không kịp |
| IEEE VTC2027-Spring | Hamburg | 30/09/2026 (đã gia hạn) ([CfP](https://events.vtsociety.org/vtc2027-spring/call-for-papers-2/)) | — | — | ❌ Đã qua |

**Khuyến nghị:** VTC2027-Fall. Yếu tố quyết định: là venue rank B duy nhất đã kiểm chứng có hạn nộp sau mốc 2 tháng, và có track AI/ML for Communications khớp với chủ đề mobility. Chỉ nộp **một** trong VTC2027-Fall hoặc EUSIPCO 2027 (không nộp trùng).

**Yêu cầu định dạng VTC (theo CfP VTC2027-Spring, cần kiểm tra lại cho Fall):** 5 trang tiêu chuẩn, tối đa 7 trang (trả phí trang thêm), trên 8 trang không được review.

### 28.2. Journal (Q1/Q2)

| Journal | SJR 2025 | Quartile | Phù hợp | Mô hình xuất bản |
|---|---|---|---|---|
| **IEEE Transactions on Cognitive Communications and Networking** (khuyến nghị) | 2.359 | Q1 (AI; Computer Networks & Communications; Hardware & Architecture) ([SJR](https://www.scimagojr.com/journalsearch.php?q=21100854831&tip=sid&clean=0)) | ML cho truyền thông — khớp J1–J3 | Hybrid; APC `NEEDS VERIFICATION` |
| IEEE Transactions on Vehicular Technology | 2.052 | Q1 ([SJR](https://www.scimagojr.com/journalsearch.php?q=17393&tip=sid)) | Mobility, Doppler | Hybrid; APC `NEEDS VERIFICATION` |
| IEEE Open Journal of the Communications Society | 1.723 | Q1 ([SJR](https://www.scimagojr.com/journalsearch.php?q=21101070921&tip=sid&clean=0)) | Rộng, review nhanh | Open access, APC ước tính 3,910 USD (2025, theo trang SJR) |
| IEEE Wireless Communications Letters | 1.894 | Q1 ([SJR](https://www.scimagojr.com/journalsearch.php?q=21100203111&tip=sid)) | Dạng letter; không hợp cho bản mở rộng | Hybrid |
| IEEE Communications Letters | 1.601 | Q1 ([SJR](https://www.scimagojr.com/journalsearch.php?q=18896&tip=sid)) | Như trên | Hybrid |

**Khuyến nghị:** IEEE TCCN (chính), IEEE TVT (thay thế). Lý do: đóng góp journal là phương pháp học máy có bảo đảm và công cụ đo khoảng cách phân bố — đúng phạm vi TCCN; TVT phù hợp nếu reviewer conference đánh giá cao phần mobility.

### 28.3. Thứ tự nộp và chính sách trùng lặp

1. Conference nộp trước (≤ 01/02/2027).
2. Trước khi nộp journal, Tùng đọc “Information for Authors” của TCCN/TVT về bản mở rộng của bài hội nghị và việc review song song. `NEEDS VERIFICATION`.
3. Nếu được phép: nộp journal tháng 02/2027, khai báo bài conference trong cover letter, nêu rõ J1–J3 là nội dung mới.
4. Nếu không được phép review song song: chờ thông báo VTC (14/04/2027), trong thời gian đó hoàn thiện E12 (MIMO) hoặc mở rộng E8.

---

## 29. Final Feasibility Report

| Category | Status | Evidence | Risk | Mitigation | Confidence |
|---|---|---|---|---|---|
| Research Gap | 🟡 | G1–G3; prior art gần (arXiv:2509.18574, 2605.26157, 2608.02172) không có bound | Có bài chưa tìm thấy | Literature search S1, Gate 1 | Trung bình |
| Novelty | 🟡 | A1 có chứng minh; A3 có dữ liệu sơ bộ ([T] Fig. 25) | Mệnh đề bị coi là đơn giản | Kết hợp với ramp vật lý + đánh giá OOD rộng | Trung bình |
| Algorithm | 🟢 | Gate + LLR fusion là thay đổi nhỏ trên pipeline có sẵn | Gate học sai | Ramp cấu trúc | Cao |
| Model | 🟡 | Backbone 1.21M đã train trên T4 ([T] Fig. 31) | Mâu thuẫn cấu hình D6–D8 | Đọc từ code S1 | Trung bình |
| Dataset | 🟢 | Synthetic Sionna, sinh theo seed | Tham số D9 | `config.yaml` | Cao |
| Simulation | 🟢 | Pipeline Sionna đã dùng trong [T] | Version Sionna chưa rõ | Ghi version trong repo | Cao |
| Computation | 🟡 | T4 chạy được batch 128 | Chưa đo GPU-giờ | Pilot S1; lưới rút gọn | Trung bình |
| Baseline | 🟡 | B0, B1, M1′, M4 có sẵn | M1 DeepRx-đúng chưa có | Sionna tutorial làm dự phòng | Trung bình |
| Web Demo | 🟢 | Gradio đơn giản | Sionna chậm trên CPU | Cache + n slot nhỏ | Cao |
| Conference | 🟡 | 8 tuần, venue đã xác minh hạn nộp | H3b chưa biết | Khung negative result dự phòng | Trung bình |
| Journal | 🟡 | J1 có cơ sở từ [T] Table 3 ≡ Table 4 | 8 tuần ngắn; chính sách trùng lặp | Ưu tiên J1 + J3; lùi nộp nếu cần | Trung bình–thấp |

**Kết luận: 🟡 FEASIBLE WITH CONDITIONS.**
Ba điều kiện bắt buộc: (C1) tái lập [T] trước 16/10; (C2) ngân sách conference ≤ 60–90 GPU-giờ; (C3) không có prior art trùng A1. Nếu C1 hoặc C3 thất bại, phạm vi được điều chỉnh theo Mục 27 trước khi tiếp tục.

---

## 30. Success Criteria

### 30.1. Research Success
- Mọi mâu thuẫn D1–D13 được giải quyết và ghi trong `config.yaml`.
- H2 được xác nhận hoặc bác bỏ bằng lưới OOD có CI.
- Mệnh đề 1 được chứng minh và kiểm chứng số (R_BMD thực nghiệm ≥ cận ở mọi ô).
- Toàn bộ hình/bảng sinh lại bằng một lệnh từ repo.

### 30.2. Conference Success
- Bảng ablation M1–M5 với baseline DeepRx-đúng, 3 seed, CI.
- M5 đạt Γ ≤ 1 dB trên lưới OOD và G_M5 ≥ G_M4 − 0.3 dB; **hoặc** (khung dự phòng) phân tích định lượng vì sao không đạt.
- Không có tuyên bố “real-time”, “guaranteed BLER”, hay so sánh tham số với DeepRx 13.35M như “SOTA”.
- Paper IEEEtran hoàn chỉnh trước 29/11/2026; nộp VTC2027-Fall trước 01/02/2027.
- Web demo gọi M5 thật và tái tạo được ít nhất 1 hình của paper.

### 30.3. Journal Success
- J1: Spearman(MMD-TF, ΔS) được báo cáo với kiểm định hoán vị; so sánh trực tiếp với MMD-PDP.
- Ít nhất một trong J2 (gate theo khoảng cách) hoặc J3 (cận khi ρ̂ có lỗi) hoàn chỉnh.
- E8 cho thấy kết luận giữ được trên TDL và 16-QAM (hoặc chỉ ra giới hạn).
- Bản thảo journal hoàn chỉnh trước 24/01/2027; kế hoạch nộp tuân thủ chính sách trùng lặp.

---

## Phụ lục A — Việc sửa luận văn (tách khỏi roadmap nghiên cứu)

Các lỗi trình bày trong [R2] (Abstract ghi ResCNN, thiếu Table 1–2, Eq. 13 sai chỉ số, Hình 11–20 nằm trong Table 12, ACKNOWLEGMENTS, định nghĩa LMMSE/LS/MSE…) cần sửa cho bản lưu chiểu. Bổ sung từ lần đọc này:
- Tham chiếu Böcherer trong §4.1 được đánh số [11], nhưng [11] trong danh mục là Luan & Thompson — sửa đánh số.
- Caption Fig. 25 (“đạt 10⁻⁴ tại 29.5 dB”) và Fig. 23 cần sửa cho khớp đồ thị; Fig. 30 caption ghi 13,352,188 trong khi log ghi 13,352,198.
- Không dùng các giá trị delay spread mà [R2] đề xuất (300/100/300/30 ns) nếu code không dùng chúng.

## Phụ lục B — Nguồn web đã dùng

- Honkala et al., DeepRx — [arXiv:2005.01494](https://arxiv.org/pdf/2005.01494)
- Yellapragada et al., Axial Self-Attention NRX — [arXiv:2510.12941v2](https://arxiv.org/html/2510.12941v2)
- Obeed & Jian, Hybrid Neural/Traditional OFDM Receiver with Learnable Decider — [arXiv:2509.18574](https://arxiv.org/html/2509.18574)
- Elnashar, Detect-and-Rollback for 5G/6G NR — [arXiv:2605.26157 (Pith)](https://pith.science/paper/2605.26157)
- Jiang et al., CARNet — [arXiv:2608.02172](https://arxiv.org/html/2608.02172v1)
- Al Rabby, Training Coverage, Not Architecture… — [Zenodo 22994791](https://zenodo.org/records/22994791)
- Wiesmayr et al., Real-Time NRX for 5G NR — [arXiv:2409.02912](https://arxiv.org/abs/2409.02912)
- VTC2027-Fall — [events.vtsociety.org/vtc2027-fall](https://events.vtsociety.org/vtc2027-fall/); VTC2027-Spring CfP — [link](https://events.vtsociety.org/vtc2027-spring/call-for-papers-2/)
- EUSIPCO 2027 — [eusipco2027.de](https://eusipco2027.de/)
- ICC 2027 — [beri.net](https://www.beri.net/events/ieee-icc-2027)
- GLOBECOM 2027 — [aconf.org](https://www.aconf.org/conf_196005.GLOBECOM_2027_-_2027_IEEE_Global_Communications_Conference.html)
- ICORE/CORE: VTC — [portal.core.edu.au/conf-ranks/757](https://portal.core.edu.au/conf-ranks/757/); GLOBECOM — [conf-ranks/2030](https://portal.core.edu.au/conf-ranks/2030/); ICORE2026 update — [core.edu.au](https://www.core.edu.au/icore-portal/icore-portal-2026-rankings-updates)
- SCImago 2025: [TCCN](https://www.scimagojr.com/journalsearch.php?q=21100854831&tip=sid&clean=0), [TVT](https://www.scimagojr.com/journalsearch.php?q=17393&tip=sid), [OJ-COMS](https://www.scimagojr.com/journalsearch.php?q=21101070921&tip=sid&clean=0), [WCL](https://www.scimagojr.com/journalsearch.php?q=21100203111&tip=sid), [Commun. Letters](https://www.scimagojr.com/journalsearch.php?q=18896&tip=sid)
