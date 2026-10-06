# Official Thesis Result Plots Catalog (`plots/`)

Tài liệu này quản lý danh mục toàn bộ 20 hình ảnh kết quả thực nghiệm nguyên bản được trích xuất trực tiếp byte-for-byte từ Chương VI (CHAPTER VI - RESULTS) của file Luận văn chính thức:  
`Storage/Senior-Project-Report(Design Specification AI fabrication).docx` (tương ứng `word/media/image15.png` đến `image34.png`).

> [!IMPORTANT]
> Toàn bộ các tệp đồ thị và bảng biểu được giữ nguyên bản gốc 100%, không re-plot, không thay đổi kích thước và không chỉnh sửa pixel nhằm đảm bảo tính toàn vẹn và giá trị khoa học của bằng chứng nghiên cứu.

---

## 1. Bảng phân loại đa chiều 20 đồ thị Results

| STT | Media ID DOCX | Số hiệu & Caption trong Luận văn | Tên file chuẩn hóa trong `plots/` | Mô hình CDL | Điều chế QAM | Coderate R | Tốc độ Train $\rightarrow$ Test | Phân loại Tốc độ |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | `image15.png` | **Figure 11**: CDL-A baseline | `fig11_cdl_a_baseline_qpsk_r05_10mps.png` | **CDL-A** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 2 | `image16.png` | **Figure 12**: CDL-A proposed | `fig12_cdl_a_proposed_qpsk_r05_10mps.png` | **CDL-A** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 3 | `image17.png` | **Figure 13**: CDL-B baseline | `fig13_cdl_b_baseline_qpsk_r05_10mps.png` | **CDL-B** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 4 | `image18.png` | **Figure 14**: CDL-B proposed | `fig14_cdl_b_proposed_qpsk_r05_10mps.png` | **CDL-B** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 5 | `image19.png` | **Figure 15**: CDL-C baseline | `fig15_cdl_c_baseline_qpsk_r05_10mps.png` | **CDL-C** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 6 | `image20.png` | **Figure 16**: CDL-C proposed | `fig16_cdl_c_proposed_qpsk_r05_10mps.png` | **CDL-C** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 7 | `image21.png` | **Figure 17**: CDL-D baseline | `fig17_cdl_d_baseline_qpsk_r05_10mps.png` | **CDL-D** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 8 | `image22.png` | **Figure 18**: CDL-D proposed | `fig18_cdl_d_proposed_qpsk_r05_10mps.png` | **CDL-D** | **4-QAM (QPSK)** | R=0.5 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 9 | `image23.png` | **Figure 19**: Baseline Model Complexity | `fig19_complexity_baseline_qpsk.png` | N/A | **4-QAM (QPSK)** | N/A | N/A | Bảng độ phức tạp Baseline |
| 10 | `image24.png` | **Figure 20**: Proposed Model Complexity | `fig20_complexity_proposed_qpsk.png` | N/A | **4-QAM (QPSK)** | N/A | N/A | Bảng độ phức tạp Proposed |
| 11 | `image25.png` | **Figure 21**: 64-QAM, R=0.9, 97.2 m/s, CDL-C | `fig21_cdl_c_64qam_r09_train0mps_test97mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 97.2 m/s | **Khác speed (Out-of-distribution)** |
| 12 | `image26.png` | **Figure 22**: 64-QAM, R=0.9, 10 m/s, CDL-A | `fig22_cdl_a_64qam_r09_train0mps_test10mps.png` | **CDL-A** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | **Khác speed (Out-of-distribution)** |
| 13 | `image27.png` | **Figure 23**: 64-QAM, R=0.9, 10 m/s, CDL-C | `fig23_cdl_c_64qam_r09_train0mps_test10mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | **Khác speed (Out-of-distribution)** |
| 14 | `image28.png` | **Figure 24**: 64-QAM, R=0.9, 40 m/s, CDL-C | `fig24_cdl_c_64qam_r09_train0mps_test40mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 40 m/s | **Khác speed (Out-of-distribution)** |
| 15 | `image29.png` | **Figure 25**: 64-QAM, R=0.9, 10 m/s, CDL-D | `fig25_cdl_d_64qam_r09_train0mps_test10mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 10 m/s | **Khác speed (Out-of-distribution)** |
| 16 | `image30.png` | **Figure 26**: 64-QAM, R=0.9, 40 m/s, CDL-D | `fig26_cdl_d_64qam_r09_train0mps_test40mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 0 m/s $\rightarrow$ Test 40 m/s | **Khác speed (Out-of-distribution)** |
| 17 | `image31.png` | **Figure 27**: 64-QAM, R=0.9, 10 m/s, CDL-A | `fig27_cdl_a_64qam_r09_train10mps_test10mps.png` | **CDL-A** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 18 | `image32.png` | **Figure 28**: 64-QAM, R=0.9, 10 m/s, CDL-C | `fig28_cdl_c_64qam_r09_train10mps_test10mps.png` | **CDL-C** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 19 | `image33.png` | **Figure 29**: 64-QAM, R=0.9, 10 m/s, CDL-D | `fig29_cdl_d_64qam_r09_train10mps_test10mps.png` | **CDL-D** | **64-QAM** | R=0.9 | Train 10 m/s $\rightarrow$ Test 10 m/s | **Cùng speed (In-distribution)** |
| 20 | `image34.png` | **Figure 30 & 31**: ResNet-11 & Proposed Benchmark | `fig30_31_benchmark_resnet11_vs_proposed.png` | **Tất cả CDL** | **64-QAM** | R=0.9 | Đa tốc độ (0, 10, 40, 97 m/s) | Bảng Benchmark tổng hợp |

---

## 2. Quy tắc phân nhóm 4 chiều

1. **Theo Môi trường Kênh CDL**:
   - **CDL-A**: Figures 11, 12, 22, 27
   - **CDL-B**: Figures 13, 14
   - **CDL-C**: Figures 15, 16, 21, 23, 24, 28
   - **CDL-D**: Figures 17, 18, 25, 26, 29
   - **Tổng hợp / Toàn bộ kênh**: Figure 30 & 31
2. **Theo Loại Điều chế**:
   - **4-QAM (QPSK)**: Figures 11 đến 20
   - **64-QAM**: Figures 21 đến 31
3. **Theo Tỷ lệ Mã hóa R (Coderate)**:
   - **R = 0.5**: Figures 11 đến 18 (QPSK)
   - **R = 0.9**: Figures 21 đến 31 (64-QAM)
4. **Theo Quan hệ Tốc độ Huấn luyện vs Kiểm thử**:
   - **In-distribution (Cùng tốc độ train = test)**:
     - QPSK 10 m/s: Figures 11–18
     - 64-QAM 10 m/s: Figures 27–29
   - **Out-of-distribution (Khác tốc độ / Domain shift train $\neq$ test)**:
     - 64-QAM Train 0 m/s $\rightarrow$ Test 10, 40, 97.2 m/s: Figures 21–26
