from django.urls import path
from .views import AuthenticateView, UserView, LeadView, ProjectView, ProjectStatusPercentageView, ProjectStatusView

urlpatterns = [
    path('authenticate', AuthenticateView.as_view()),
    path('user', UserView.as_view()),
    path('user/<int:user_id>', UserView.as_view()),
    path('lead', LeadView.as_view()),
    path('lead/<int:lead_id>', LeadView.as_view()),
    path('project', ProjectView.as_view()),
    path('project/<int:project_id>', ProjectView.as_view()),
    path('project-status-percentage', ProjectStatusPercentageView.as_view()),
    path('project-status', ProjectStatusView.as_view()),
]
