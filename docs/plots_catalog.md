# Danh mục Tra cứu Toàn diện Đồ thị Kết quả Luận văn (`docs/plots_catalog.md`)

Tài liệu này đóng vai trò Single Source Catalog đối soát toàn bộ 20 đồ thị và bảng biểu kết quả trong Chương VI (CHAPTER VI - RESULTS) của Luận văn:  
`Storage/Senior-Project-Report(Design Specification AI fabrication).docx`.

Toàn bộ 20 hình ảnh đã được chuẩn hóa tên tệp để **phân biệt rõ ràng từng mô hình máy thu nơ-ron (Neural Receiver Architecture)** và sắp xếp vào các thư mục phân loại trong [`plots/`](file:///C:/Users/thanh/Documents/antigravity/Thesis%20Folder/Working/nrx-bounded/plots/).

---

## 1. Cấu trúc cây thư mục phân loại trong `plots/`

```text
plots/
├── benchmark/
│   ├── complexity/
│   │   ├── fig19_complexity_baseline_rescnn_qpsk.png
│   │   └── fig20_complexity_proposed_axial_transformer_qpsk.png
│   └── resnet11_vs_proposed/
│       └── fig30_31_benchmark_resnet11_vs_proposed.png
└── evaluation/
    ├── sec6_1_1_minimal_4qam_r05_train10mps_test10mps/
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
    ├── sec6_1_2_train_speed_0mps_64qam_r09/
    │   ├── cdl_a/
    │   │   └── fig22_cdl_a_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │   ├── cdl_c/
    │   │   ├── fig21_cdl_c_proposed_axial_transformer_64qam_r09_train0mps_test97mps.png
    │   │   ├── fig23_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │   │   └── fig24_cdl_c_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png
    │   └── cdl_d/
    │       ├── fig25_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test10mps.png
    │       └── fig26_cdl_d_rescnn_vs_proposed_axial_64qam_r09_train0mps_test40mps.png
    └── sec6_1_3_train_speed_10mps_64qam_r09/
        ├── cdl_a/
        │   └── fig27_cdl_a_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
        ├── cdl_c/
        │   └── fig28_cdl_c_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
        └── cdl_d/
            └── fig29_cdl_d_proposed_axial_transformer_64qam_r09_train10mps_test10mps.png
```

---

## 2. Bảng đối chiếu chi tiết 20 hình ảnh Results

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

## 3. Tiêu chí phân loại 5 chiều

1. **Kiến trúc Neural Receiver**:
   - **`baseline_rescnn`**: Mạng tích chập phần dư DeepRx ResCNN.
   - **`proposed_axial_transformer`**: Mạng nơ-ron kết hợp LMMSE-assisted Axial Transformer.
   - **`rescnn_vs_proposed_axial`**: Đồ thị đối sánh 2 kiến trúc máy thu nơ-ron.
2. **Phân hệ Mục đích**:
   - **`benchmark/`**: Đối chuẩn độ phức tạp mô hình (tham số, FLOPs, bộ nhớ, độ trễ).
   - **`evaluation/`**: Đánh giá độ tin cậy thu nhận tín hiệu thông qua đường cong BLER theo $E_b/N_0$.
3. **Môi trường kênh CDL**:
   - **CDL-A, B, C, D**: Tương ứng 4 mô hình truyền sóng chuẩn hóa của 3GPP TR 38.901.
4. **Loại Điều chế & Coderate**:
   - **4-QAM (QPSK), $R = 0.5$** (Figures 11–20).
   - **64-QAM, $R = 0.9$** (Figures 21–31).
5. **Mối quan hệ Vận tốc**:
   - **In-distribution**: Train 10 m/s = Test 10 m/s (Figures 11–18, 27–29).
   - **Out-of-distribution**: Train 0 m/s $\rightarrow$ Test 10, 40, 97.2 m/s (Figures 21–26).
