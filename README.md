# DevDesk

Hệ thống quản lý yêu cầu hỗ trợ kỹ thuật (Django), phục vụ đồ án **CI/CD & GitOps**.

## Phase 2 (hiện tại)

Ứng dụng web: đăng nhập / đăng ký / phân quyền, ticket + comment (Bootstrap), dashboard, `GET /health/`.

Chưa có: REST API (Phase 3), Docker Compose (Phase 4), GitHub Actions, Helm, Argo CD.

## Chạy local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py test
python manage.py runserver
```

Mở [http://localhost:8000/](http://localhost:8000/) — sẽ chuyển tới trang đăng nhập.

Tài khoản demo (sau `seed_demo`):

| User | Role | Password |
|------|------|----------|
| `admin` | Admin | `Devdesk-demo-1` |
| `agent` | Agent | `Devdesk-demo-1` |
| `customer` | Customer | `Devdesk-demo-1` |

Health check: [http://localhost:8000/health/](http://localhost:8000/health/)

`runserver` chỉ dùng local. Gunicorn ở Phase 4.
