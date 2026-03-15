# 🚀 Freelance Marketplace API (Mini Upwork)

Django Rest Framework asosida qurilgan to'liq freelance marketplace backend API.

---

## 📖 Loyiha haqida

Bu platforma mijozlar (client) va frilanserlar (freelancer) o'rtasida ko'prik vazifasini o'taydi:
- Mijozlar loyiha joylaydi
- Frilanserlar taklif (bid) yuboradi
- Mijoz eng yaxshi taklifni tanlab shartnoma tuzadi
- Loyiha tugagach mijoz frilanserga baho beradi

---

## 🛠 Texnologiyalar

| Texnologiya | Versiya |
|---|---|
| Python | 3.10+ |
| Django | 4.2.7 |
| Django Rest Framework | 3.14.0 |
| PostgreSQL | 14+ |
| JWT (SimpleJWT) | 5.3.0 |
| Swagger (drf-yasg) | 1.21.7 |
| django-filter | 23.3 |

---

## 👤 Test foydalanuvchilar

| Role | Username | Password |
|---|---|---|
| Client | `client1` | `client123` |
| Client | `client2` | `client123` |
| Freelancer | `freelancer1` | `freelancer123` |
| Freelancer | `freelancer2` | `freelancer123` |
| Freelancer | `freelancer3` | `freelancer123` |
| Admin | `admin` | `admin123` |

---

## ⚙️ Loyihani ishga tushirish

### 1. Repositoryni clone qilish
```bash
git clone https://github.com/yourusername/freelance-marketplace-drf.git
cd freelance-marketplace-drf
```

### 2. Virtual environment yaratish
```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. .env fayl yaratish
```bash
cp .env.example .env
```
`.env` faylni oching va ma'lumotlarni to'ldiring:
```
SECRET_KEY=your-secret-key-here
DB_NAME=freelance_marketplace
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. PostgreSQL database yaratish
```bash
psql -U postgres
CREATE DATABASE freelance_marketplace;
\q
```

### 6. Migratsiya qilish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Test ma'lumotlarini yuklash
```bash
python manage.py seed_data
```

### 8. Serverni ishga tushirish
```bash
python manage.py runserver
```

Server `http://127.0.0.1:8000` da ishlaydi.

---

## 📚 API Dokumentatsiya

| URL | Tavsif |
|---|---|
| `/swagger/` | Swagger UI — interaktiv API tester |
| `/redoc/` | ReDoc — chiroyli API dokumentatsiya |
| `/admin/` | Django Admin panel |

---

## 📋 API Endpointlar ro'yxati

### 🔐 Authentication — `/api/v1/auth/`

| Method | Endpoint | Tavsif | Auth |
|---|---|---|---|
| POST | `/register/` | Ro'yxatdan o'tish | ❌ |
| POST | `/login/` | Kirish (JWT token olish) | ❌ |
| POST | `/logout/` | Chiqish (token blacklist) | ✅ |
| POST | `/token/refresh/` | Access token yangilash | ❌ |
| GET | `/profile/` | O'z profilini ko'rish | ✅ |
| PUT/PATCH | `/profile/` | Profilni tahrirlash | ✅ |
| GET | `/profile/<id>/` | Boshqa foydalanuvchi profili | ✅ |
| POST | `/change-password/` | Parolni o'zgartirish | ✅ |
| POST | `/forgot-password/` | Parolni unutdim (email yuborish) | ❌ |
| POST | `/reset-password/` | Yangi parol o'rnatish (token bilan) | ❌ |
| GET | `/freelancers/` | Barcha frilanserlar ro'yxati | ✅ |

### 📁 Projects — `/api/v1/projects/`

| Method | Endpoint | Tavsif | Role |
|---|---|---|---|
| GET | `/` | Barcha open loyihalar (search, filter, pagination) | ✅ All |
| POST | `/create/` | Yangi loyiha yaratish | 👤 Client |
| GET | `/my/` | Mening loyihalarim | 👤 Client |
| GET | `/all/` | Barcha loyihalar (har xil statusda) | ✅ All |
| GET | `/<id>/` | Loyiha tafsilotlari | ✅ All |
| PUT/PATCH | `/<id>/update/` | Loyihani tahrirlash | 👤 Client (owner) |
| PATCH | `/<id>/cancel/` | Loyihani bekor qilish | 👤 Client (owner) |

**Search va Filter parametrlari:**
- `?search=` — title yoki description bo'yicha qidirish
- `?budget_min=` — minimal budget
- `?budget_max=` — maksimal budget
- `?status=` — open / in_progress / completed / cancelled
- `?deadline_before=` — berilgan sanadan avvalgi deadline
- `?deadline_after=` — berilgan sanadan keyingi deadline
- `?ordering=budget` — tartiblash (budget, deadline, created_at)

### 💰 Bids — `/api/v1/bids/`

| Method | Endpoint | Tavsif | Role |
|---|---|---|---|
| POST | `/` | Loyihaga bid yuborish | 👷 Freelancer |
| GET | `/my/` | Mening bidlarim | 👷 Freelancer |
| GET | `/<id>/` | Bid tafsilotlari | ✅ All |
| PUT/PATCH | `/<id>/update/` | Bidni tahrirlash | 👷 Freelancer |
| DELETE | `/<id>/delete/` | Bidni o'chirish | 👷 Freelancer |
| POST | `/<id>/accept/` | Bidni qabul qilish | 👤 Client |
| GET | `/project/<project_id>/` | Loyihaga kelgan bidlar | 👤 Client |

### 📄 Contracts — `/api/v1/contracts/`

| Method | Endpoint | Tavsif | Role |
|---|---|---|---|
| GET | `/` | Mening shartnomalarim | ✅ All |
| GET | `/<id>/` | Shartnoma tafsilotlari | ✅ (ishtirokchi) |
| POST | `/<id>/finish/` | Shartnomani tugatish | 👤 Client |
| POST | `/<id>/cancel/` | Shartnomani bekor qilish | 👤 Client |

### ⭐ Reviews — `/api/v1/reviews/`

| Method | Endpoint | Tavsif | Role |
|---|---|---|---|
| POST | `/` | Frilanserga baho berish | 👤 Client |
| GET | `/my/received/` | Menga yozilgan baholar | 👷 Freelancer |
| GET | `/my/given/` | Men yozgan baholar | 👤 Client |
| GET | `/<id>/` | Baho tafsilotlari | ✅ All |
| GET | `/freelancer/<id>/` | Frilanserning barcha baholari | ✅ All |

---

## 🔄 Asosiy iş oqimi (Workflow)

```
1. Client ro'yxatdan o'tadi (role: client)
2. Freelancer ro'yxatdan o'tadi (role: freelancer)
3. Client loyiha yaratadi → status: open
4. Freelancer loyihani ko'radi va bid yuboradi
5. Client bidlar ro'yxatini ko'radi va birini qabul qiladi
   → Qabul qilingan bid: accepted
   → Boshqa bidlar: rejected
   → Loyiha: in_progress
   → Shartnoma yaratiladi: active
6. Loyiha bajarilgach client finish bosadi
   → Shartnoma: finished
   → Loyiha: completed
7. Client frilanserga baho beradi (1-5 yulduz)
```

---

## 🔑 Autentifikatsiya

API JWT (JSON Web Token) orqali ishlaydi.

**Token olish:**
```bash
POST /api/v1/auth/login/
{
  "username": "client1",
  "password": "client123"
}
```

**So'rovlarda token ishlatish:**
```
Authorization: Bearer <access_token>
```

**Token yangilash:**
```bash
POST /api/v1/auth/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

---

## 🔒 Parolni tiklash

```bash
# 1. Email yuborish
POST /api/v1/auth/forgot-password/
{"email": "user@example.com"}

# 2. Emaildagi link orqali yangi parol o'rnatish
POST /api/v1/auth/reset-password/
{
  "uid": "<uid_from_email>",
  "token": "<token_from_email>",
  "new_password": "newpassword123",
  "new_password2": "newpassword123"
}
```

> **Debug rejimda:** forgot-password javobi uid va tokenni ham qaytaradi (test uchun qulay).

---

## 📮 Postman Collection

Postman collection fayli: `postman_collection.json`

Import qilish:
1. Postman → Import → Upload Files
2. `postman_collection.json` faylini tanlang
3. Environment o'rnating: `base_url = http://127.0.0.1:8000`

---

## 🗂 Loyiha strukturasi

```
freelance-marketplace-drf/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── User/
│   ├── models.py       # Custom User model
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/seed_data.py
├── Project/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── permissions.py
├── Bid/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── Contract/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── Review/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```
