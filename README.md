Prepared by Ivory Plush 	Prepared by Coria Alles 
 
Introduction 
# 🌐 SocialHub 
Mini social media platform (Facebook-like) built with *Django 4.2*.   
Users can register, post updates with images, like & comment, manage privacy settings, and interact socially with friends 
--- 
## 🚀 Features 
### 🔑 Core 
- 🔐 User Authentication (register, login, logout, password reset via email)   
- 👤 User profile with bio + profile picture   
- 📝 Post creation (text + image uploads)   
- ❤ Like / Unlike functionality   
- 💬 Comment system   
- 📧 Email integration (welcome email, password reset)   
- ⚙ User settings (privacy controls + notification preferences)   
- 🏠 Home feed with all posts
-  💬 Messaging system
### 🎁 Bonus (Implemented) 
- 👥 Friend / Follow system   
- 🔔 Real-time notifications   
- 🔍 Search functionality   
 
 
Objectives 
## 🛠 Tech Stack 
- *Backend*: Django 4.2   
- *Database*: SQLite (development)   
- *Image Handling*: Pillow   
- *Secrets Management*: python-decouple   
- *Frontend*: Django Templates + CSS framework (Bootstrap/Tailwind)   
--- 
## 📂 Project Structure. 
 
project/
 │── core/ # Main project folder
 │ │── core/ # Django project settings (settings.py, urls.py, etc.)
 │ │── media/ # User-uploaded media (profile pictures, post images, etc.)
 │ │── social/ # Main social app
 │ │ │── migrations/ # Database migrations
 │ │ │── static/ # Static files (CSS, JS, images)
 │ │ │ │── css/
 │ │ │ │ │── styles.css # Main stylesheet
 │ │ │ │── images/ # Example images
 │ │ │ │── js/ # (Your custom JS files if any)
 │ │ │── templates/ # HTML templates
 │ │ │ │── registration/ # Auth-related templates
 │ │ │ │ │── base1.html
 │ │ │ │ │── login.html
 │ │ │ │ │── register.html
 │ │ │ │ │── password_reset_*.html # Reset password flow
 │ │ │ │── user/ # Core app templates
 │ │ │ │ │── base.html
 │ │ │ │ │── home.html
 │ │ │ │ │── profile.html
 │ │ │ │ │── profile_detail.html
 │ │ │ │ │── edit_profile.html
 │ │ │ │ │── post_detail.html
 │ │ │ │ │── notifications.html
 │ │ │ │ │── inbox.html
 │ │ │ │ │── send_message.html
 │ │ │ │ │── search_results.html
 │ │ │ │ │── settings.html
 │ │ │── admin.py
 │ │ │── apps.py
 │ │ │── context_processors.py
 │ │ │── forms.py
 │ │ │── models.py
 │ │ │── tests.py
 │ │ │── urls.py
 │ │ │── views.py
 │── db.sqlite3 # SQLite database
 │── manage.py # Django management script
 │── requirements.txt # Project dependencies
 │── venv/ # Virtual environment (ignored in Git) 
 
## ⚙ Setup Guide 
 
### 1. Clone the repository 
bash 
git clone https://github.com/your-username/socialhub.git 
cd socialhub 
______________________________ 
2. Create virtual environment 
python -m venv venv 
venv\Scripts\activate     
3. Install dependencies 
pip install -r requirements.txt 
______________________________ 
4. Configure environment variables 
Create .env file in the project root: 
SECRET_KEY=your_django_secret_key 
DEBUG=True 
EMAIL_HOST=smtp.gmail.com 
EMAIL_PORT=587 
EMAIL_USE_TLS=True 
EMAIL_HOST_USER=your_gmail@gmail.com 
EMAIL_HOST_PASSWORD=your_app_password 
______________________________ 
5. Apply migrations 
python manage.py makemigrations 
python manage.py migrate 
______________________________ 
6. Create superuser 
python manage.py createsuperuser 
______________________________ 
7. Run development server 
python manage.py runserver 
App will be available at 👉 http://127.0.0.1:8000/ 
_______________________________ 
## 📸 Screenshots 
 
| الصفحة | صورة | 
|--------|-------| 
| 🏠 Home Feed | ![Home](static\images\pictures\photo_2025-09-16_17-55-42.jpg) | 
| 👤 Profile Page | ![Profile](static\images\pictures\photo_2025-09-16_17-55-24.jpg) | 
| ✍ Create Post | ![Create Post](static\images\pictures\photo_2025-09-16_17-55-42.jpg) | 
| 💬 Post Detail (Comments + Likes) | ![Post Detail] (static\images\pictures\photo_2025-09-16_17-55-42.jpg) | 
| 👥 Friends / Follow List | ![Friends](static\images\pictures\Screenshot 2025-09-15 224104.png) | 
| 🔍 Search Results | ![Search](static\images\pictures\Screenshot 2025-09-16 143503.png) | 
| 🔔 Notifications | ![Notifications](static\images\pictures\photo_2025-09-16_17-56-02.jpg) | 
| 📩 Inbox (Messages) | ![Inbox](static\images\pictures\Screenshot 2025-09-16 143414.png) | 
| ✉ Send Message | ![Send Message](static\images\pictures\Screenshot 2025-09-16 143414.png) | 
| ⚙ Settings Page | ![Settings](static\images\pictures\Screenshot 2025-09-16 143435.png) | 
| 🙍‍♂ Edit Profile | ![Edit Profile](static/images/screenshots/edit_profile.png) | 
| 🔑 Login | ![Login](static\images\pictures\photo_2025-09-16_17-55-45.jpg) | 
| 📝 Register | ![Register](static\images\pictures\photo_2025-09-16_17-55-26.jpg) | 
_________________
 bash 
 Git clone https://github.com/Malak-Saied
Git clone https://github.com/karemabdelwahab09

Git clone  https://github.com/basantmoha


 Cd social hub
