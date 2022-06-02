"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import (IndexView,
                            Home,
                            RecipeList,
                            Main,
                            Plans,
                            RecipeAdd,
                            PlanAdd,
                            PlanAddRecipe,
                            RecipeDetails,
                            RecipeModify,
                            PlanDetails,
                            SlugViewContactAndAbout,
                            PlanModify,
                            DeleteReceipe,
                            DeletePlan
                            )


urlpatterns = [

    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', Home.as_view()),
    path('main/', Main.as_view(), name='main'),
    path('recipe/list', RecipeList.as_view(), name='recipe'),
    path('recipe/<int:id>', RecipeDetails.as_view(), name='recipe_id'),
    path('recipe/modify/<int:id>', RecipeModify.as_view()),
    path('recipe/add', RecipeAdd.as_view(), name='recipe-add'),
    path('recipe/modify/<int:id>', RecipeModify.as_view(),name='recipe-modify'),
    path('plan/list', Plans.as_view(), name='plans'),
    path('plan/<int:id>', PlanDetails.as_view(), name='plan-details'),
    path('plan/add', PlanAdd.as_view(), name='plan-add'),
    path('plan/add-recipe', PlanAddRecipe.as_view(), name='plan-add-recipe'),
    path('<slug:slug>/', SlugViewContactAndAbout.as_view()),
    path('plan/modify/<int:id>', PlanModify.as_view(), name='plan-modify'),
    path('recipe/delete/<int:id>', DeleteReceipe.as_view(), name='delete-recipe'),
    path('plan/delete/<int:id>', DeletePlan.as_view(), name='delete-plan'),

]
