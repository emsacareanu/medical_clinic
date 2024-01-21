from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import page1, page2, login_view, find_patient, submit_employee_form, show_query_result


urlpatterns = [
    path('login/', login_view, name='login'),
    path('page1/', page1, name='page1'),
    path('page2/', page2, name='page2'),
    path('find_patient/', find_patient, name='find_patient'),
    path('submit_employee_form/', submit_employee_form, name='submit_employee_form'),
    path('show_query_result/', show_query_result, name='show_query_result'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
