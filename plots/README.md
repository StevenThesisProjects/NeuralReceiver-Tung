# Official Thesis Result Plots Catalog (`plots/`)

Tài liệu này quản lý danh mục toàn bộ 20 hình ảnh kết quả thực nghiệm nguyên bản được trích xuất trực tiếp byte-for-byte từ Chương VI (CHAPTER VI - RESULTS) của file Luận văn chính thức:  
`Storage/Senior-Project-Report(Design Specification AI fabrication).docx` (tương ứng `word/media/image15.png` đến `image34.png`).

> [!IMPORTANT]
> Toàn bộ 20 tệp đồ thị và bảng biểu được giữ nguyên bản gốc 100%, không re-plot, không can thiệp pixel và không thêm bất kỳ ảnh ngoại lai/hoang tưởng nào. Toàn bộ ảnh đã được phân loại chuẩn xác vào cây thư mục chuyên biệt.

---

## 1. Cấu trúc cây thư mục chuẩn hóa (`plots/`)

Cấu trúc thư mục được phân định rõ ràng giữa nhóm **Đánh giá Hiệu năng (Evaluation)** và **Đối chuẩn Kỹ thuật (Benchmark)**, bám sát các đề mục thực nghiệm trong Chương VI của Luận văn:

```text
plots/
├── benchmark/                                                 # Nhóm đối chuẩn kỹ thuật kiến trúc mô hình
│   ├── complexity/                                            # Độ phức tạp không gian (Parameters, FP32/FP16 Memory)
│   │   ├── fig19_complexity_baseline_qpsk.png
│   │   └── fig20_complexity_proposed_qpsk.png
│   └── resnet11_vs_proposed/                                  # Đối chuẩn toàn diện: FLOPs, Latency (T4), Throughput
│       └── fig30_31_benchmark_resnet11_vs_proposed.png
└── evaluation/                                                # Nhóm đánh giá đường cong BLER / BER theo kênh truyền
    ├── sec6_1_1_minimal_4qam_r05_train10mps_test10mps/       # Mục 6.1.1: 4-QAM (QPSK), R=0.5, Train 10 m/s = Test 10 m/s
    │   ├── cdl_a/
    │   │   ├── fig11_cdl_a_baseline_qpsk_r05_10mps.png
    │   │   └── fig12_cdl_a_proposed_qpsk_r05_10mps.png
    │   ├── cdl_b/
    │   │   ├── fig13_cdl_b_baseline_qpsk_r05_10mps.png
    │   │   └── fig14_cdl_b_proposed_qpsk_r05_10mps.png
    │   ├── cdl_c/
    │   │   ├── fig15_cdl_c_baseline_qpsk_r05_10mps.png
    │   │   └── fig16_cdl_c_proposed_qpsk_r05_10mps.png
    │   └── cdl_d/
    │       ├── fig17_cdl_d_baseline_qpsk_r05_10mps.png
    │       └── fig18_cdl_d_proposed_qpsk_r05_10mps.png
    ├── sec6_1_2_train_speed_0mps_64qam_r09/                  # Mục 6.1.2: 64-QAM, R=0.9, Train 0 m/s (Out-of-distribution Doppler)
    │   ├── cdl_a/
    │   │   └── fig22_cdl_a_64qam_r09_train0mps_test10mps.png
    │   ├── cdl_c/
    │   │   ├── fig21_cdl_c_64qam_r09_train0mps_test97mps.png
    │   │   ├── fig23_cdl_c_64qam_r09_train0mps_test10mps.png
    │   │   └── fig24_cdl_c_64qam_r09_train0mps_test40mps.png
    │   └── cdl_d/
    │       ├── fig25_cdl_d_64qam_r09_train0mps_test10mps.png
    │       └── fig26_cdl_d_64qam_r09_train0mps_test40mps.png
    └── sec6_1_3_train_speed_10mps_64qam_r09/                 # Mục 6.1.3: 64-QAM, R=0.9, Train 10 m/s = Test 10 m/s (In-distribution)
        ├── cdl_a/
        │   └── fig27_cdl_a_64qam_r09_train10mps_test10mps.png
        ├── cdl_c/
        │   └── fig28_cdl_c_64qam_r09_train10mps_test10mps.png
        └── cdl_d/
            └── fig29_cdl_d_64qam_r09_train10mps_test10mps.png
```

---

## 2. Bảng phân loại chi tiết 20 đồ thị Results theo tiêu chuẩn Luận văn

| STT | Media ID DOCX | Số hiệu & Caption trong Luận văn | Đường dẫn tương đối mới trong `plots/` | Mô hình CDL | Điều chế QAM | Coderate R | Tốc độ Train $\rightarrow$ Test | Phân loại & Vai trò |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| 1 | `image15.png` | **Figure 11**: CDL-A baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_a/fig11_cdl_a_baseline_qpsk_r05_10mps.png` | **CDL-A** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Baseline |
| 2 | `image16.png` | **Figure 12**: CDL-A proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_a/fig12_cdl_a_proposed_qpsk_r05_10mps.png` | **CDL-A** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 3 | `image17.png` | **Figure 13**: CDL-B baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_b/fig13_cdl_b_baseline_qpsk_r05_10mps.png` | **CDL-B** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Baseline |
| 4 | `image18.png` | **Figure 14**: CDL-B proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_b/fig14_cdl_b_proposed_qpsk_r05_10mps.png` | **CDL-B** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 5 | `image19.png` | **Figure 15**: CDL-C baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_c/fig15_cdl_c_baseline_qpsk_r05_10mps.png` | **CDL-C** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Baseline |
| 6 | `image20.png` | **Figure 16**: CDL-C proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_c/fig16_cdl_c_proposed_qpsk_r05_10mps.png` | **CDL-C** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 7 | `image21.png` | **Figure 17**: CDL-D baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_d/fig17_cdl_d_baseline_qpsk_r05_10mps.png` | **CDL-D** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Baseline |
| 8 | `image22.png` | **Figure 18**: CDL-D proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_d/fig18_cdl_d_proposed_qpsk_r05_10mps.png` | **CDL-D** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 9 | `image23.png` | **Figure 19**: Baseline Model Complexity | `benchmark/complexity/fig19_complexity_baseline_qpsk.png` | N/A | **4-QAM (QPSK)** | N/A | N/A | **Benchmark** — Complexity Baseline |
| 10 | `image24.png` | **Figure 20**: Proposed Model Complexity | `benchmark/complexity/fig20_complexity_proposed_qpsk.png` | N/A | **4-QAM (QPSK)** | N/A | N/A | **Benchmark** — Complexity Proposed |
| 11 | `image25.png` | **Figure 21**: 64-QAM, R=0.9, 97.2 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig21_cdl_c_64qam_r09_train0mps_test97mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 97.2 m/s | Evaluation — Out-of-distribution (Cực đoan) |
| 12 | `image26.png` | **Figure 22**: 64-QAM, R=0.9, 10 m/s, CDL-A | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_a/fig22_cdl_a_64qam_r09_train0mps_test10mps.png` | **CDL-A** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | Evaluation — Out-of-distribution |
| 13 | `image27.png` | **Figure 23**: 64-QAM, R=0.9, 10 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig23_cdl_c_64qam_r09_train0mps_test10mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | Evaluation — Out-of-distribution |
| 14 | `image28.png` | **Figure 24**: 64-QAM, R=0.9, 40 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig24_cdl_c_64qam_r09_train0mps_test40mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 40 m/s | Evaluation — Out-of-distribution |
| 15 | `image29.png` | **Figure 25**: 64-QAM, R=0.9, 10 m/s, CDL-D | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_d/fig25_cdl_d_64qam_r09_train0mps_test10mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | Evaluation — Out-of-distribution |
| 16 | `image30.png` | **Figure 26**: 64-QAM, R=0.9, 40 m/s, CDL-D | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_d/fig26_cdl_d_64qam_r09_train0mps_test40mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 40 m/s | Evaluation — Out-of-distribution |
| 17 | `image31.png` | **Figure 27**: 64-QAM, R=0.9, 10 m/s, CDL-A | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_a/fig27_cdl_a_64qam_r09_train10mps_test10mps.png` | **CDL-A** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 18 | `image32.png` | **Figure 28**: 64-QAM, R=0.9, 10 m/s, CDL-C | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_c/fig28_cdl_c_64qam_r09_train10mps_test10mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 19 | `image33.png` | **Figure 29**: 64-QAM, R=0.9, 10 m/s, CDL-D | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_d/fig29_cdl_d_64qam_r09_train10mps_test10mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | Evaluation — In-distribution Proposed |
| 20 | `image34.png` | **Figure 30 & 31**: ResNet-11 & Proposed Benchmark | `benchmark/resnet11_vs_proposed/fig30_31_benchmark_resnet11_vs_proposed.png` | **Tất cả CDL** | **64-QAM** | R=0.9 | Đa tốc độ (0, 10, 40, 97 m/s) | **Benchmark** — So sánh ResNet-11 & Proposed |

---

## 3. Bản đồ các tiêu chí phân biệt 5 chiều

1. **Phân biệt Phân hệ Mục đích**:
   - **`benchmark/`**: Bảng tham số phần cứng, độ phức tạp bộ nhớ, FLOPs và độ trễ suy luận (Figures 19, 20, 30 & 31).
   - **`evaluation/`**: Đường cong hiệu năng liên lạc BLER/BER theo tỷ số $E_b/N_0$ trên các kênh truyền multipath (Figures 11–18, 21–29).
2. **Phân biệt Môi trường Kênh truyền CDL**:
   - **CDL-A**: Đô thị NLOS trải trễ ngắn (Figures 11, 12, 22, 27).
   - **CDL-B**: Kênh trải trễ trung bình (Figures 13, 14).
   - **CDL-C**: Đô thị NLOS trải trễ dài 300 ns (Figures 15, 16, 21, 23, 24, 28).
   - **CDL-D**: Nông thôn LOS có thành phần trực diện mạnh (Figures 17, 18, 25, 26, 29).
3. **Phân biệt Loại Điều chế QAM**:
   - **4-QAM (QPSK)**: 2 bit/symbol, cấu hình tối thiểu phục vụ kiểm thử đơn giản (Mục 6.1.1, Figures 11–20).
   - **64-QAM**: 6 bit/symbol, cấu hình chuẩn cao cấp 6G chịu ảnh hưởng lớn từ can nhiễu pha (Mục 6.1.2 & 6.1.3, Figures 21–31).
4. **Phân biệt Tỷ lệ Mã hóa Coderate**:
   - **$R = 0.5$**: Tỷ lệ dư thừa bảo vệ 50% (áp dụng với 4-QAM).
   - **$R = 0.9$**: Tỷ lệ mã hóa cực cao (90% tải hữu ích, chỉ 10% parity bits), kiểm chứng độ nhạy máy thu AI.
5. **Phân biệt Tương quan Vận tốc (Training vs Evaluation Speed)**:
   - **In-distribution (Cùng vận tốc $v_{train} = v_{test} = 10\text{ m/s}$)**:
     - Mục 6.1.1 (QPSK, R=0.5): Figures 11–18.
     - Mục 6.1.3 (64-QAM, R=0.9): Figures 27–29.
   - **Out-of-distribution (Lệch vận tốc / Doppler Shift Unawareness)**:
     - Mục 6.1.2: Train ở $0\text{ m/s}$ (kênh tĩnh) nhưng Test ở $10\text{ m/s}$, $40\text{ m/s}$, $97.2\text{ m/s}$ (Figures 21–26) để đánh giá khả năng tổng quát hóa và cơ chế bảo vệ vật lý LMMSE.
