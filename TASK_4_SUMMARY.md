# TASK 4 SUMMARY: Chốt giá trị thực tế D6–D9, D13 vào docs/config_resolution.md

## 1. Thông tin chung
- **Ngày thực hiện**: 2026-10-06
- **Repo Git**: `C:\Users\thanh\Documents\antigravity\Thesis Folder\Working\nrx-bounded`
- **Người thực hiện**: Agent A (Vuong Thanh Tung)

## 2. Kết quả chốt tham số (Single Source of Truth)
- **D6 (Proposed Model)**: `d_model = 128`, `nhead = 4`, `num_layers = 6`, `d_ff = 256`, `dropout = 0.1` (Khớp 100% checkpoint 114 keys).
- **D7 (Lưới tài nguyên & FFT)**: $T = 14$ symbols, $F = 128$ subcarriers, SCS 30 kHz, Guard [5, 6], DC Null 1, Useful 116.
- **D8 (Kênh đầu vào)**: Đúng 12 kênh theo thứ tự: `y_real[0,1]`, `y_imag[0,1]`, `h_ls_real[0,1]`, `h_ls_imag[0,1]`, `x_lmmse_real,imag`, `no_log`, `pilot_mask`.
- **D9 (Delay Spread)**: CDL-A (30 ns), CDL-B (100 ns), CDL-C (300 ns).
- **D13 (Huấn luyện & SNR)**: AdamW (lr 1e-4, wd 1e-4), batch 16, accum 8 (effective 128), dải SNR [0, 20] dB / Shannon [8.8, 22.0] dB.

## 3. Git Commit Log
```
commit 07840ea87e0a7ad4840a0293750e4aa7133ba03c
Author: Vuong Thanh Tung <tung.vuong@example.com>
Date:   Tue Oct 6 18:47:30 2026 +0700

    docs(infra): resolve config conflicts D6-D9, D13 in docs/config_resolution.md

 docs/config_resolution.md | 50 +++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 50 insertions(+)
```

## 4. Xác nhận tiêu chí nghiệm thu (Definition of Done)
1. File `docs/config_resolution.md` tồn tại trong repo `nrx-bounded`: ✅ ĐẠT.
2. Bảng đối chiếu D6–D9, D13 có đầy đủ các cột yêu cầu: ✅ ĐẠT.
3. D8 nêu chính xác danh sách và thứ tự 12 kênh đầu vào: ✅ ĐẠT.
4. `git status` clean: ✅ ĐẠT.
5. Commit mới xuất hiện trong `git log -1`: ✅ ĐẠT.
