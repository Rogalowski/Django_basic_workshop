from datetime import datetime
import random
from difflib import get_close_matches


from django.http import Http404



from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from datetime import datetime

from jedzonko.models import Recipe, Plan, RecipePlan, DayName, Page
from django.contrib import messages
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Home(View):
    HTML_TEMPLATE = 'index.html'

    def get(self, request):
        # SLUG
        try:
            pageslug = Page.objects.get(slug='contact').slug
        except Page.DoesNotExist:
            pageslug = '#contact'

        try:
            aboutslug = Page.objects.get(slug='about').slug
        except Page.DoesNotExist:
            aboutslug = '#about'



        recipes = Recipe.objects.all()
        three_recipes = random.sample(list(recipes), 3)

        last_plan = Plan.objects.all().order_by('-created')[0]
        last_plan_id = Plan.objects.all().order_by('-created')[0].id

        recipes_in_last_plan = RecipePlan.objects.filter(plan=last_plan_id)

        return render(
            request,
            self.HTML_TEMPLATE,
            context={
                'recipes': three_recipes,
                'last_plan': last_plan,
                'recipes_in_last_plan': recipes_in_last_plan,
                'pageslug': pageslug,
                'aboutslug': aboutslug,
            },
        )



class Main(View):
    HTML_TEMPLATE = 'dashboard.html'

    def get(self, request):
        recipes_count = Recipe.objects.all().count()
        plans_count = Plan.objects.all().count()

        last_plan = Plan.objects.all().order_by('-created')[0]
        last_plan_id = Plan.objects.all().order_by('-created')[0].id

        recipes_in_last_plan = RecipePlan.objects.filter(plan=last_plan_id)

        return render(
            request,
            self.HTML_TEMPLATE,
            context={
                'recipes_count': recipes_count,
                'plans_count': plans_count,
                'last_plan': last_plan,
                'recipes_in_last_plan': recipes_in_last_plan,
            },
        )


class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)

        buttons_like_unlike = f"""
                <input type="hidden" name="pk" value="{ recipe.pk }">
                <input type="submit" name="like" value="Polub przepis" class="btn btn-color rounded-0 pt-0 pb-0 pr-4 pl-4">
                <input type="submit" name="dislike" value="Nie lubię przepisu" class="btn btn-color rounded-0 pt-0 pb-0 pr-4 pl-4">
        """


        if request.session.get(f'recipe{id}'):
            print('GET ' + request.session[f'recipe{id}'])

            return render(
                request,
                'app-recipe-details.html',
                {'recipe': recipe},

            )

        return render(
            request,
            'app-recipe-details.html',
            {'buttons_like_unlike': buttons_like_unlike, 'recipe': recipe},
        )

    def post(self, request, id):
        id_from_input = request.POST.get('pk')
        recipe = Recipe.objects.get(pk=id_from_input)
        likes = recipe.votes

        if 'like' in request.POST:
            request.session[f'recipe{id_from_input}'] = id_from_input
            print('POST ' + request.session[f'recipe{id_from_input}'])
            likes += 1

        elif 'dislike' in request.POST:
            request.session[f'recipe{id_from_input}'] = id_from_input
            likes -= 1

        recipe.votes = likes
        recipe.save()
        return redirect('recipe_id', id=id_from_input)

class DeleteReceipe(View):
    def get(self, request, id):
        recipe_del_id = Recipe.objects.get(pk=id)
        recipe_del_id.delete()
        return redirect('/recipe/list')

class DeletePlan(View):
    def get(self, request, id):
        plan_del_id = Plan.objects.get(pk=id)
        plan_del_id.delete()
        return redirect('/plan/list')


class RecipeAdd(View):
    HTML_TEMPLATE = 'app-add-recipe.html'

    def get(self, request):
        return render(request, self.HTML_TEMPLATE)

    def post(self, request):
        name = request.POST.get('name')

        try:
            preparation_time = int(request.POST.get('preparation_time'))
        except:
            return self.error(request)

        description = request.POST.get('description')
        method_of_preparing = request.POST.get('method_of_preparing')
        ingredients = request.POST.get('ingredients')

        if name == '' or description == '' or ingredients == '' or preparation_time == '':
            return self.error(request)

        Recipe.objects.create(
            name=name,
            ingredients=ingredients,
            description=description,
            preparation_time=preparation_time,
            method_of_preparing=method_of_preparing,
        )


        return redirect('recipe')

    def error(self, request):
        error = 'Wypełnij poprawnie wszystkie pola'

        return render(
            request,
            self.HTML_TEMPLATE,
            context={'error': error},
        )


class RecipeList(View):
    HTML_TEMPLATE = 'app-recipes.html'

    def get(self, request):
        # recipes = Recipe.objects.all()
        recipes = Recipe.objects.all().order_by('-votes', '-created')

        paginator = Paginator(recipes, 5)  # wysw. liczbe wierszy na stronie
        page = request.GET.get('page')
        recipes_page = paginator.get_page(page)

        return render(
            request,
            self.HTML_TEMPLATE,
            context={'recipe_pages': recipes_page})

    def post(self, request):
        search_phrase = request.POST.get('search_phrase')
        phrases = self.variants_of_search(search_phrase)

        recipes = Recipe.objects.filter(name__in=phrases)

        paginator = Paginator(recipes, 5)  # wysw. liczbe wierszy na stronie
        page = request.GET.get('page')
        recipes_page = paginator.get_page(page)

        if recipes:
            return render(
                request,
                self.HTML_TEMPLATE,
                context={'recipe_pages': recipes_page})
        else:
            return render(
                request,
                self.HTML_TEMPLATE,
                context={
                    'recipe_pages': recipes_page,
                    'no_results': 'Nie znaleziono przepisu',
                },
            )

    def variants_of_search(self, word):
        recipe_objects = Recipe.objects.all()
        recipe_names = [recipe.name.lower() for recipe in recipe_objects]
        names_splited_to_lists = [word.split() for word in recipe_names]
        names_splited_to_single_word = []
        for lista in names_splited_to_lists:
            for n in lista:
                if len(n) > 2:
                    names_splited_to_single_word.append(n)

        variant_lower = get_close_matches(
            word, names_splited_to_single_word, n=3, cutoff=0.6)
        variant_capitalize = get_close_matches(
            word.capitalize(), names_splited_to_single_word, n=3, cutoff=0.6)
        variant_upper = get_close_matches(
            word.upper(), names_splited_to_single_word, n=3, cutoff=0.6)
        variants = variant_lower+variant_capitalize+variant_upper
        variants = set(variants)

        return list(variants)


class RecipeModify(View):

    def get(self, request, id):
        try:
            recipe = Recipe.objects.get(pk=id)
        except:
            raise Http404

        return render(
            request,
            'app-edit-recipe.html',
            {'recipe': recipe}
        )

    def post(self, request, id):
        name = request.POST.get('name')
        time = request.POST.get('time')
        description = request.POST.get('description')
        method_of_preparing = request.POST.get('method_of_preparing')
        ingredients = request.POST.get('ingredients')
        if name != '' and time != '' and description != '' and ingredients != '':
            Recipe.objects.create(
                name=name,
                preparation_time=time,
                description=description,
                ingredients=ingredients,
                method_of_preparing=method_of_preparing
            )
            return redirect('recipe')
        else:
            return render(
                request, 'app-edit-recipe.html',
                {
                    'recipe': Recipe.objects.get(pk=id),
                    'error': 'Wypełnij poprawnie wszystkie pola'
                },
            )


class Plans(View):

    def get(self, request):
        plans = Plan.objects.all().order_by('name')

        paginator = Paginator(plans, 2)
        page_num = request.GET.get('page')
        plans_pages = paginator.get_page(page_num)

        return render(
            request,
            'app-schedules.html',
            {'plans_pages': plans_pages})


class PlanAdd(View):
    HTML_TEMPLATE = 'app-plan-add.html'

    def get(self, request):
        return render(
            request,
            self.HTML_TEMPLATE,
        )

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')

        if plan_name == '':
            return render(
                request,
                self.HTML_TEMPLATE,
                context={
                    'name_error': 'Nazwij nowy plan, żebyś potem go odnalazł/a.'},
            )

        if plan_description == '':
            return render(
                request,
                self.HTML_TEMPLATE,
                context={'description_error': 'Dodaj opis.'}
            )

        new_plan = Plan.objects.create(
            name=plan_name,
            description=plan_description,
        )
        new_plan.save()
        plan_id = new_plan.pk

        messages.success(request, 'Plan dodany do bazy danych')
        return redirect(
            'plan-details',
            id=plan_id,
        )


class PlanDetails(View):
    HTML_TEMPLATE = 'app-details-schedules.html'

    def get(self, request, id):
        plan = Plan.objects.get(pk=id)

        recipes_in_plan = RecipePlan.objects.filter(plan=plan.id)
        time_weekday = datetime.today().weekday()
        time_time_now = datetime.today().hour
        list_day = DayName.objects.all()

        return render(
            request,
            self.HTML_TEMPLATE,
            context={
                'plan': plan,
                'list_day': list_day,
                'time_weekday': time_weekday,
                'time_time_now': time_time_now,
                'recipes_in_plan': recipes_in_plan,
            },
        )

    def post(self, request, id):

        recipe_plan_id = request.POST.get('recipe_plan_id')

        RecipePlan.objects.get(pk=recipe_plan_id).delete()
       
        plan = Plan.objects.get(pk=id)
        recipes_in_plan = RecipePlan.objects.filter(plan=plan.id)
        time_weekday = datetime.today().weekday()
        time_time_now = datetime.today().hour

        # TODO: redirect nie działał...
        return render(
            request,
            self.HTML_TEMPLATE,
            context={
                'plan': plan,
                'time_weekday': time_weekday,
                'time_time_now': time_time_now,
                'recipes_in_plan': recipes_in_plan,
            }
        )


class PlanAddRecipe(View):

    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        return render(
            request,
            'app-schedules-meal-recipe.html',
            {
                'plans': plans,
                'recipes': recipes,
                'days': days
            },
        )

    def post(self, request):
        plan = request.POST.get('plan')
        meal_name = request.POST.get('meal_name')
        meal_number = request.POST.get('meal_number')
        recipe = request.POST.get('recipe')
        day = request.POST.get('day')

        RecipePlan.objects.create(
            meal_name=meal_name,
            order=meal_number,
            recipe=Recipe.objects.get(pk=recipe),
            plan=Plan.objects.get(pk=plan),
            day_name=DayName.objects.get(pk=day))

        return redirect('plan-details', id=plan)



class SlugViewContactAndAbout(View):
    def get(self, request, slug):
        if slug == 'about':
            aboutslug = get_object_or_404(Page, slug=slug)
            return render(request, "about.html", {"aboutslug": aboutslug})
        if slug == 'contact':
            contactslug = get_object_or_404(Page, slug=slug)
            return render(request, "contact.html", {"contactslug": contactslug})


class PlanModify(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        return render(request, 'app-edit-schedules.html',
                      {'plan': plan})

    def post(self, request, id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        plan = Plan.objects.get(pk=id)
        if name == '' or description == '':
            return render(request, 'app-edit-schedules.html',
                          {'plan': plan,
                           'error': "Uzupełnij pola"})
        else:
            plan.name = name
            plan.description = description
            plan.save()
            return redirect('plans')
