from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 🏠 HOME / POSTS
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/edit/", views.post_update, name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),

    # ❤️ LIKES (AJAX)
    path("post/<int:pk>/like/ajax/", views.ajax_toggle_like, name="ajax_post_like"),

    # 💬 COMMENTS (AJAX)
    path("post/<int:pk>/comment/ajax/", views.ajax_add_comment, name="ajax_post_comment"),
    path("comment/<int:pk>/delete/", views.ajax_delete_comment, name="ajax_delete_comment"),

    # 👤 PROFILE
    path("profile/", views.profile_detail, name="profile_detail"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # 🔐 AUTHENTICATION
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="post_list"), name="logout"),
    path("register/", views.register, name="register"),
]
