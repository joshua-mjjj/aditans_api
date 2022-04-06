import notifications.urls
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from api.views import (
    AccountLoginAPIView,
    SignUp,
    UserProfile,
    ChangePasswordApi,
    ProjectTypeList,
    ProfileViewset,
    MentorProfileViewset,
    ClusterViewset
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewset, basename="students")
router.register(r"mentor-profiles", MentorProfileViewset, basename="mentor-profiles")
router.register(r"clusters", ClusterViewset, basename="clusters")

schema_view = get_swagger_view(title="VIPPU API")

urlpatterns = [
    path("login/", AccountLoginAPIView.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="api-signup"),

    path("token/refresh/", refresh_jwt_token),
    path("users/me/", UserProfile.as_view()),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/", include("rest_framework_social_oauth2.urls")),
    path("auth/password/change/", ChangePasswordApi.as_view()),
    path("project-types", ProjectTypeList.as_view(), name="student-types"),
    path("", include(router.urls)),
]


# path("auth/accounts/confirm/", AccountActivation.as_view()),
# path("auth/password/request/reset/", RequestPasswordReset.as_view()),
# path("auth/password/reset/request/confirm/", ConfirmPasswordResetRequest.as_view()),
# path("auth/password/reset/", ResetPasswordApi.as_view()),