# Official Thesis Result Plots Catalog (`plots/`)

Tài liệu này quản lý danh mục toàn bộ 20 hình ảnh kết quả thực nghiệm nguyên bản được trích xuất trực tiếp byte-for-byte từ Chương VI (CHAPTER VI - RESULTS) của file Luận văn chính thức:  
`Storage/Senior-Project-Report(Design Specification AI fabrication).docx` (tương ứng `word/media/image15.png` đến `image34.png`).

> [!IMPORTANT]
> Toàn bộ 20 tệp đồ thị và bảng biểu được giữ nguyên bản gốc 100%, không re-plot, không can thiệp pixel và không thêm bất kỳ ảnh ngoại lai nào. Tên các tệp hình ảnh đã được chuẩn hóa để **phân biệt rõ ràng từng kiến trúc máy thu nơ-ron** (Neural Receiver Architectures):
> - **`baseline_rescnn`**: Máy thu nơ-ron DeepRx Residual CNN baseline (Honkala et al.).
> - **`proposed_axial_transformer`**: Máy thu nơ-ron đề xuất tích hợp LMMSE-assisted Axial Transformer (Self-Attention).
> - **`rescnn_vs_proposed_axial`**: Đồ thị đối sánh trực tiếp giữa hai kiến trúc nơ-ron DeepRx ResCNN và Proposed Axial Transformer.

---

## 1. Cấu trúc cây thư mục chuẩn hóa (`plots/`)

```text
plots/
├── benchmark/                                                 # Nhóm đối chuẩn kỹ thuật kiến trúc mô hình
│   ├── complexity/                                            # Độ phức tạp không gian (Parameters, FP32/FP16 Memory)
│   │   ├── fig19_complexity_baseline_rescnn_qpsk.png
│   │   └── fig20_complexity_proposed_axial_transformer_qpsk.png
│   └── resnet11_vs_proposed/                                  # Đối chuẩn toàn diện: FLOPs, Latency (T4), Throughput
│       └── fig30_31_benchmark_resnet11_vs_proposed.png
└── evaluation/                                                # Nhóm đánh giá đường cong BLER / BER theo kênh truyền
    ├── sec6_1_1_minimal_4qam_r05_train10mps_test10mps/       # Mục 6.1.1: 4-QAM (QPSK), R=0.5, Train 10 m/s = Test 10 m/s
    │   ├── cdl_a/
    │   │   ├── fig11_cdl_a_baseline_rescnn_qpsk_r05_10mps.png
    │   │   └── fig12_cdl_a_proposed_axial_transformer_qpsk_r05_10mps.png
    │   ├── cdl_b/
    │   │   ├── fig13_cdl_b_baseline_rescnn_qpsk_r05_10mps.png
    │   │   └── fig14_cdl_b_proposed_axial_transformer_qpsk_r05_10mps.png
    │   ├── cdl_c/
    │   │   ├── fig15_cdl_c_baseline_rescnn_qpsk_r05_10mps.png
    │   │   └── fig16_cdl_c_proposed_axial_transformer_qpsk_r05_10mps.png
    │   └── cdl_d/
    │       ├── fig17_cdl_d_baseline_rescnn_qpsk_r05_10mps.png
    │       └── fig18_cdl_d_proposed_axial_transformer_qpsk_r05_10mps.png
    ├── sec6_1_2_train_speed_0mps_64qam_r09/                  # Mục 6.1.2: 64-QAM, R=0.9, Train 0 m/s (Out-of-distribution Doppler)
    │   ├── cdl_a/
    │   │   └── fig22_cdl_a_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │   ├── cdl_c/
    │   │   ├── fig21_cdl_c_proposed_axial_transformer_64qam_r09_train0mps_test97mps.png
    │   │   ├── fig23_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │   │   └── fig24_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png
    │   └── cdl_d/
    │       ├── fig25_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │       └── fig26_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png
    └── sec6_1_3_train_speed_10mps_64qam_r09/                 # Mục 6.1.3: 64-QAM, R=0.9, Train 10 m/s = Test 10 m/s (In-distribution)
        ├── cdl_a/
        │   └── fig27_cdl_a_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
        ├── cdl_c/
        │   └── fig28_cdl_c_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
        └── cdl_d/
            └── fig29_cdl_d_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
```

---

## 2. Bảng phân loại chi tiết 20 đồ thị Results theo tiêu chuẩn Luận văn

| STT | Media ID DOCX | Số hiệu & Caption trong Luận văn | Đường dẫn tương đối chuẩn hóa trong `plots/` | Mô hình CDL | Điều chế & R | Vận tốc Train $\rightarrow$ Test | Mô hình Neural Receiver được đánh giá |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---|
| 1 | `image15.png` | **Figure 11**: CDL-A baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_a/fig11_cdl_a_baseline_rescnn_qpsk_r05_10mps.png` | **CDL-A** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **DeepRx ResCNN** (Baseline n=4) |
| 2 | `image16.png` | **Figure 12**: CDL-A proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_a/fig12_cdl_a_proposed_axial_transformer_qpsk_r05_10mps.png` | **CDL-A** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed N=3) |
| 3 | `image17.png` | **Figure 13**: CDL-B baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_b/fig13_cdl_b_baseline_rescnn_qpsk_r05_10mps.png` | **CDL-B** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **DeepRx ResCNN** (Baseline n=4) |
| 4 | `image18.png` | **Figure 14**: CDL-B proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_b/fig14_cdl_b_proposed_axial_transformer_qpsk_r05_10mps.png` | **CDL-B** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed N=3) |
| 5 | `image19.png` | **Figure 15**: CDL-C baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_c/fig15_cdl_c_baseline_rescnn_qpsk_r05_10mps.png` | **CDL-C** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **DeepRx ResCNN** (Baseline n=4) |
| 6 | `image20.png` | **Figure 16**: CDL-C proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_c/fig16_cdl_c_proposed_axial_transformer_qpsk_r05_10mps.png` | **CDL-C** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed N=3) |
| 7 | `image21.png` | **Figure 17**: CDL-D baseline | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_d/fig17_cdl_d_baseline_rescnn_qpsk_r05_10mps.png` | **CDL-D** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **DeepRx ResCNN** (Baseline n=4) |
| 8 | `image22.png` | **Figure 18**: CDL-D proposed | `evaluation/sec6_1_1_minimal_4qam_r05_train10mps_test10mps/cdl_d/fig18_cdl_d_proposed_axial_transformer_qpsk_r05_10mps.png` | **CDL-D** | QPSK, R=0.5 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed N=3) |
| 9 | `image23.png` | **Figure 19**: Baseline Model Complexity | `benchmark/complexity/fig19_complexity_baseline_rescnn_qpsk.png` | N/A | QPSK | N/A | **DeepRx ResCNN** (Space Complexity) |
| 10 | `image24.png` | **Figure 20**: Proposed Model Complexity | `benchmark/complexity/fig20_complexity_proposed_axial_transformer_qpsk.png` | N/A | QPSK | N/A | **Axial Transformer** (Space Complexity) |
| 11 | `image25.png` | **Figure 21**: 64-QAM, R=0.9, 97.2 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig21_cdl_c_proposed_axial_transformer_64qam_r09_train0mps_test97mps.png` | **CDL-C** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 97.2 m/s | **Axial Transformer** (Proposed Extreme Robustness) |
| 12 | `image26.png` | **Figure 22**: 64-QAM, R=0.9, 10 m/s, CDL-A | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_a/fig22_cdl_a_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png` | **CDL-A** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 10 m/s | **Đối sánh ResCNN vs Proposed Axial** |
| 13 | `image27.png` | **Figure 23**: 64-QAM, R=0.9, 10 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig23_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png` | **CDL-C** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 10 m/s | **Đối sánh ResCNN vs Proposed Axial** |
| 14 | `image28.png` | **Figure 24**: 64-QAM, R=0.9, 40 m/s, CDL-C | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_c/fig24_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png` | **CDL-C** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 40 m/s | **Đối sánh ResCNN vs Proposed Axial** |
| 15 | `image29.png` | **Figure 25**: 64-QAM, R=0.9, 10 m/s, CDL-D | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_d/fig25_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png` | **CDL-D** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 10 m/s | **Đối sánh ResCNN vs Proposed Axial** |
| 16 | `image30.png` | **Figure 26**: 64-QAM, R=0.9, 40 m/s, CDL-D | `evaluation/sec6_1_2_train_speed_0mps_64qam_r09/cdl_d/fig26_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png` | **CDL-D** | 64-QAM, R=0.9 | 0 m/s $\rightarrow$ 40 m/s | **Đối sánh ResCNN vs Proposed Axial** |
| 17 | `image31.png` | **Figure 27**: 64-QAM, R=0.9, 10 m/s, CDL-A | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_a/fig27_cdl_a_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png` | **CDL-A** | 64-QAM, R=0.9 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed Model Focusing) |
| 18 | `image32.png` | **Figure 28**: 64-QAM, R=0.9, 10 m/s, CDL-C | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_c/fig28_cdl_c_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png` | **CDL-C** | 64-QAM, R=0.9 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed Model Focusing) |
| 19 | `image33.png` | **Figure 29**: 64-QAM, R=0.9, 10 m/s, CDL-D | `evaluation/sec6_1_3_train_speed_10mps_64qam_r09/cdl_d/fig29_cdl_d_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png` | **CDL-D** | 64-QAM, R=0.9 | 10 m/s $\rightarrow$ 10 m/s | **Axial Transformer** (Proposed Model Focusing) |
| 20 | `image34.png` | **Figure 30 & 31**: ResNet-11 & Proposed Benchmark | `benchmark/resnet11_vs_proposed/fig30_31_benchmark_resnet11_vs_proposed.png` | **Tất cả CDL** | 64-QAM, R=0.9 | Đa tốc độ (0, 10, 40, 97 m/s) | **Đối chuẩn toàn diện: ResNet-11 vs Proposed** |

---

## 3. Bản đồ các tiêu chí phân biệt đa chiều

1. **Phân biệt Kiến trúc Neural Receiver**:
   - **`baseline_rescnn`**: Kiến trúc DeepRx ResCNN kế thừa từ Honkala et al. (xử lý trên lưới thời gian - tần số bằng chuỗi khối tích chập residual).
   - **`proposed_axial_transformer`**: Kiến trúc đề xuất tích hợp tiền xử lý LMMSE kết hợp cơ chế chú ý trục thời gian - tần số (Axial Self-Attention).
   - **`rescnn_vs_proposed_axial`**: Đồ thị đánh giá tương quan trực tiếp chứng minh tính bền vững vượt trội của Axial Transformer khi dịch Doppler thay đổi.
2. **Phân biệt Phân hệ Mục đích**:
   - **`benchmark/`**: Đối chuẩn tham số phần cứng, dung lượng bộ nhớ FP32/FP16, số phép tính FLOPs và thông lượng suy luận khung OFDM.
   - **`evaluation/`**: Đánh giá đường cong xác suất lỗi khối BLER theo tỷ số $E_b/N_0$ trên 4 mô hình kênh CDL.
3. **Phân biệt Môi trường Kênh truyền CDL**:
   - **CDL-A** (Kênh chọn lọc tần số và trải trễ ngắn): Figures 11, 12, 22, 27.
   - **CDL-B** (Kênh trải trễ trung bình): Figures 13, 14.
   - **CDL-C** (Kênh đô thị NLOS trải trễ dài 300 ns): Figures 15, 16, 21, 23, 24, 28.
   - **CDL-D** (Kênh nông thôn / LOS): Figures 17, 18, 25, 26, 29.
4. **Phân biệt Điều chế & Coderate**:
   - **4-QAM (QPSK), $R = 0.5$**: Cấu hình tối thiểu (Mục 6.1.1, Figures 11–20).
   - **64-QAM, $R = 0.9$**: Cấu hình kiểm thử chuyên sâu cho 6G (Mục 6.1.2 & 6.1.3, Figures 21–31).
5. **Phân biệt Vận tốc (Training vs Evaluation Speed)**:
   - **In-distribution**: Train 10 m/s = Test 10 m/s (Figures 11–18, 27–29).
   - **Out-of-distribution (Domain Shift)**: Train 0 m/s $\rightarrow$ Test 10, 40, 97.2 m/s (Figures 21–26).
