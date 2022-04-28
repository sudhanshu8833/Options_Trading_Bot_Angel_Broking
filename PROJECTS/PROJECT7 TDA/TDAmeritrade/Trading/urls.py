from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='redirect_login'),
    url(r'^login_account/$', views.login_account, name='login_account'),
    url(r'^trading/$', views.trading, name='trading'),
    url(r'^strategy/$', views.strategy, name='strategy'),
    url(r'^add_bot/$', views.add_bot, name='add_bot'),
    url(r'^delete_bot/(?P<id>\w+)$', views.delete_bot, name='delete_bot'),
    url(r'^update_bot_status/$', views.update_bot_status, name='update_bot_status'),
    url(r'^add_strategy/$', views.add_strategy, name='add_strategy'),
    url(r'^run_backtest/$', views.run_backtest, name='run_backtest'),
    #url(r'^add_strategy_3_entry/$', views.add_strategy_1_entry, name='add_strategy_3_entry'),
    #url(r'^add_strategy_1_close/$', views.add_strategy_1_entry, name='add_strategy_1_close'),
    #url(r'^add_strategy_2_close/$', views.add_strategy_1_entry, name='add_strategy_2_close'),
    #url(r'^add_strategy_3_close/$', views.add_strategy_1_entry, name='add_strategy_3_close'),
    url(r'^delete_strategy/(?P<id>\w+)$', views.delete_strategy, name='delete_strategy'),
    url(r'^account/$', views.account, name='account'),
    url(r'^update_broker_info/$', views.update_broker_info, name='update_broker_info'),
    url(r'^backtest/$', views.backtest, name='backtest'),
    #url(r'^new_algo/$', views.new_algo, name='new_algo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # uploaded media
    urlpatterns += static(settings.TEMPLATES_URL, document_root=settings.TEMPLATES_ROOT)
