# Hướng dẫn đóng góp & Quy trình làm việc nhóm (DevDesk)

Tài liệu này quy định quy trình phối hợp phát triển dự án giữa các thành viên.

---

## 1. Quy ước đặt tên nhánh (Branching Convention)

- Nhánh chính: `main` (chỉ chứa code đã test và được nhóm trưởng duyệt).
- Nhánh tính năng: `feature/<tên-tính-năng>` (ví dụ: `feature/ticket-api`, `feature/docker-compose`).
- Nhánh sửa lỗi: `fix/<tên-lỗi>` (ví dụ: `fix/login-redirect`).
- Nhánh cá nhân (nếu cần): `<username>/<nhiệm-vụ>`.

---

## 2. Quy ước Commit (Conventional Commits)

- `feat:` Thêm tính năng mới.
- `fix:` Sửa lỗi.
- `docs:` Thay đổi hoặc bổ sung tài liệu.
- `refactor:` Tối ưu, cơ cấu lại code không đổi logic.
- `test:` Bổ sung unit test / integration test.
- `ci:` Cấu hình CI/CD (GitHub Actions, Docker, Helm, Argo CD).

---

## 3. Quy trình tạo Pull Request (PR)

1. Cập nhật code mới nhất từ `main`:
   ```bash
   git checkout main
   git pull origin main
   ```
2. Tạo nhánh riêng:
   ```bash
   git checkout -b feature/<tên-tính-năng>
   ```
3. Code, test kỹ lưỡng ở local, sau đó commit:
   ```bash
   git add .
   git commit -m "feat: mô tả ngắn gọn thay đổi"
   ```
4. Đẩy nhánh lên GitHub:
   ```bash
   git push -u origin feature/<tên-tính-năng>
   ```
5. Mở Pull Request trên GitHub, chọn Reviewer là nhóm trưởng hoặc thành viên liên quan.
6. Sau khi được duyệt (**Approve**), tiến hành merge vào `main`.

---

## 4. Phương án Rollback / Khôi phục khi có sự cố

Nếu code mới sau khi merge phát hiện có lỗi nghiêm trọng:

- **Cách 1: Revert commit bị lỗi trên Git (Khuyên dùng - An toàn nhất)**
  ```bash
  git revert <commit-hash-bị-lỗi>
  git push origin main
  ```
  *(Cách này tạo commit mới hủy bỏ thay đổi cũ, không làm mất lịch sử git của nhóm)*

- **Cách 2: Khôi phục nhanh từ nhánh backup cục bộ**
  ```bash
  git checkout backup/initial-clean
  ```
