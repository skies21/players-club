from django.contrib import admin
from django.urls import path, include
from . import views
from playersclub.views import IndexView, SearchView, AddRecordView, EditRecordView, IndexPositionView, \
    EditRecordPositionView, AddRecordPositionView, delete_record, delete_record_position, HomeView, \
    AddRecordMedcineView, EditRecordMedcineView, MedcineView, FinancesView, DeleteRecordMedcineView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('', include('shop.urls')),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('index/', IndexView.as_view(), name='index'),
    path('position/', IndexPositionView.as_view(), name='position'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/result', SearchView.as_view(template_name='search_result.html'),
         name='search_result'),
    path('delete/<int:pk>/', delete_record, name='delete_record'),
    path('delete_position/<int:pk>/', delete_record_position,
         name='delete_record_position'),
    path('add_record/', AddRecordView.as_view(), name='add_record'),
    path('add_record_position/', AddRecordPositionView.as_view(),
         name='add_record_position'),
    path('edit_record/<int:pk>/', EditRecordView.as_view(), name='edit_record'),
    path('edit_record_position/<int:pk>/', EditRecordPositionView.as_view(), name='edit_record_position'),
    path('add_record_medcine/', AddRecordMedcineView.as_view(),
         name='add_record_medcine'),
    path('medcine/', MedcineView.as_view(), name='medcine'),
    path('medcine/edit/<int:pk>/', EditRecordMedcineView.as_view(), name='edit_record_medcine'),
    path('medcine/delete/<int:pk>/', DeleteRecordMedcineView.as_view(), name='delete_record_medcine'),
    path('finances/', FinancesView.as_view(), name='finances'),
]
