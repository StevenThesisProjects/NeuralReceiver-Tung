# TASK 9 SUMMARY: Trích xuất nguyên bản & Phân loại toàn bộ đồ thị Results từ Luận văn vào plots/

## 1. Thông tin chung
- **Ngày thực hiện**: 2026-10-07
- **Repo Git**: `C:\Users\thanh\Documents\antigravity\Thesis Folder\Working\nrx-bounded`
- **Người thực hiện**: Agent A (Vuong Thanh Tung)

## 2. Các thành phần đã thực hiện
1. **Trích xuất nguyên bản 100% 20 đồ thị Results (`plots/*.png`)**:
   - Nguồn: File Luận văn chính thức `Storage/Senior-Project-Report(Design Specification AI fabrication).docx`.
   - Trích xuất trực tiếp byte-for-byte từ `word/media/image15.png` đến `image34.png`.
   - Chuẩn hóa tên tệp theo số hiệu Figure và cấu hình thí nghiệm:
     - `fig11_cdl_a_baseline_qpsk_r05_10mps.png` (Figure 11, CDL-A Baseline QPSK R=0.5 10m/s)
     - `fig12_cdl_a_proposed_qpsk_r05_10mps.png` (Figure 12, CDL-A Proposed QPSK R=0.5 10m/s)
     - `fig13_cdl_b_baseline_qpsk_r05_10mps.png` (Figure 13, CDL-B Baseline QPSK R=0.5 10m/s)
     - `fig14_cdl_b_proposed_qpsk_r05_10mps.png` (Figure 14, CDL-B Proposed QPSK R=0.5 10m/s)
     - `fig15_cdl_c_baseline_qpsk_r05_10mps.png` (Figure 15, CDL-C Baseline QPSK R=0.5 10m/s)
     - `fig16_cdl_c_proposed_qpsk_r05_10mps.png` (Figure 16, CDL-C Proposed QPSK R=0.5 10m/s)
     - `fig17_cdl_d_baseline_qpsk_r05_10mps.png` (Figure 17, CDL-D Baseline QPSK R=0.5 10m/s)
     - `fig18_cdl_d_proposed_qpsk_r05_10mps.png` (Figure 18, CDL-D Proposed QPSK R=0.5 10m/s)
     - `fig19_complexity_baseline_qpsk.png` (Figure 19, Baseline Complexity QPSK)
     - `fig20_complexity_proposed_qpsk.png` (Figure 20, Proposed Complexity QPSK)
     - `fig21_cdl_c_64qam_r09_train0mps_test97mps.png` (Figure 21, CDL-C 64-QAM R=0.9 Train 0 -> Test 97.2m/s)
     - `fig22_cdl_a_64qam_r09_train0mps_test10mps.png` (Figure 22, CDL-A 64-QAM R=0.9 Train 0 -> Test 10m/s)
     - `fig23_cdl_c_64qam_r09_train0mps_test10mps.png` (Figure 23, CDL-C 64-QAM R=0.9 Train 0 -> Test 10m/s)
     - `fig24_cdl_c_64qam_r09_train0mps_test40mps.png` (Figure 24, CDL-C 64-QAM R=0.9 Train 0 -> Test 40m/s)
     - `fig25_cdl_d_64qam_r09_train0mps_test10mps.png` (Figure 25, CDL-D 64-QAM R=0.9 Train 0 -> Test 10m/s)
     - `fig26_cdl_d_64qam_r09_train0mps_test40mps.png` (Figure 26, CDL-D 64-QAM R=0.9 Train 0 -> Test 40m/s)
     - `fig27_cdl_a_64qam_r09_train10mps_test10mps.png` (Figure 27, CDL-A 64-QAM R=0.9 Train 10 -> Test 10m/s)
     - `fig28_cdl_c_64qam_r09_train10mps_test10mps.png` (Figure 28, CDL-C 64-QAM R=0.9 Train 10 -> Test 10m/s)
     - `fig29_cdl_d_64qam_r09_train10mps_test10mps.png` (Figure 29, CDL-D 64-QAM R=0.9 Train 10 -> Test 10m/s)
     - `fig30_31_benchmark_resnet11_vs_proposed.png` (Figure 30 & 31, Benchmark ResNet-11 vs Proposed)
   - Đã gỡ bỏ file giữ chỗ `.gitkeep`.
2. **Thiết lập Danh mục Tra cứu 4 chiều (`plots/README.md` & `docs/plots_catalog.md`)**:
   - Phân loại rõ ràng theo 4 chiều:
     1. Môi trường kênh CDL (CDL-A, B, C, D, hoặc Tổng hợp).
     2. Loại điều chế QAM (4-QAM / QPSK hay 64-QAM).
     3. Tỷ lệ mã hóa Coderate (R=0.5 hay R=0.9).
     4. Mối quan hệ tốc độ (In-distribution: train=test hay Out-of-distribution: train≠test).
3. **Cập nhật `config/config.yaml`**:
   - Bổ sung `paths.plots_dir = "plots"` và `evaluation.plots_dir = "plots"`, `evaluation.save_plots = true`.
4. **Bổ sung Automated Test trong `tests/test_smoke.py`**:
   - Thêm `test_plots_artifacts()` kiểm tra sự tồn tại của thư mục `plots/`, đủ đúng 20 file `.png`, và có `README.md`.
   - Kết quả thực thi `pytest`: **4/4 passed (100%)**.

## 3. Git Commit Log
```
commit e4d17d5ae138a415ff66ea9d1e57c6dd8cf7e0f2
Author: Vuong Thanh Tung <tung.vuong@example.com>
Date:   Wed Oct 7 00:06:11 2026 +0700

    feat(plots): extract authentic thesis result plots (Fig 11-31) and add 4-way classification catalog

 25 files changed, 128 insertions(+)
 create mode 100644 docs/plots_catalog.md
 delete mode 100644 plots/.gitkeep
 create mode 100644 plots/README.md
 create mode 100644 plots/fig11_cdl_a_baseline_qpsk_r05_10mps.png
 ...
 create mode 100644 plots/fig30_31_benchmark_resnet11_vs_proposed.png
```

## 4. Xác nhận tiêu chí nghiệm thu (Definition of Done)
1. Thư mục `Working/nrx-bounded/plots/` chứa đủ 20 tệp `.png` trích xuất nguyên bản: ✅ ĐẠT.
2. File `plots/README.md` và `docs/plots_catalog.md` phân loại đầy đủ theo 4 tiêu chí: ✅ ĐẠT.
3. `config/config.yaml` có khai báo `plots_dir`: ✅ ĐẠT.
4. Toàn bộ test suite `pytest -v` đạt **4/4 passed**: ✅ ĐẠT.
5. Lệnh `git status` trong `Working/nrx-bounded` trả về `working tree clean` (sau commit summary): ✅ ĐẠT.
6. Toàn bộ thay đổi được đồng bộ sang `Directory/nrx-bounded/`: ✅ ĐẠT.
7. Báo cáo `TASK_9_SUMMARY.md` đầy đủ: ✅ ĐẠT.
