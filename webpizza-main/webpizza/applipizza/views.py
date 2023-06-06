from django.shortcuts import render

# Create your views here.

from applipizza.models import Pizza, Ingredient, Composition
from applipizza.forms import IngredientForm,PizzaForm,CompositionForm

def pizzas(request) :

    lesPizzas = Pizza.objects.all()

    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas" : lesPizzas}
    )

def pizza(request, pizza_id) :

    laPizza = Pizza.objects.get(idPizza = pizza_id)
    laCompo = Composition.objects.filter(pizza = pizza_id)
    formulaire = CompositionForm()
    listeIngredients = []
    
    for c in laCompo:
        ing = Ingredient.objects.get(idIngredient = c.ingredient.idIngredient)
        listeIngredients.append({"nom" : ing.nomIngredient,"qte" : c.quantite})

    return render(
        request,
        "applipizza/pizza.html",
        {"pizza" : laPizza,
        "composition" : laCompo,
        "liste" : listeIngredients,
        "form" : formulaire}
    )


def ingredients(request) :

    lesIngredients = Ingredient.objects.all()

    return render(
        request,
        "applipizza/ingredients.html",
        {"ingredients": lesIngredients}
    )

def formulaireCreationIngredient(request) :
    formulaire = IngredientForm()
    return render(
        request,
        "applipizza/formulaireCreationIngredient.html",
        {"form" : formulaire}
    )

def creerIngredient(request) :
    form = IngredientForm(request.POST)
    if form.is_valid() :
        nomIng = form.cleaned_data['nomIngredient']
        ing = Ingredient()
        ing.nomIngredient = nomIng
        ing.save()
        return render(
            request,
            "applipizza/traitementFormulaireCreationIngredient.html",
            {"nom" : nomIng}
        )

def formulaireCreationPizza(request) :
    formulaire = PizzaForm()
    return render(
        request,
        "applipizza/formulaireCreationPizza.html",
        {"form" : formulaire}
    )

def creerPizza(request) :
    form = PizzaForm(request.POST)
    if form.is_valid() :
        nomPiz = form.cleaned_data['nomPizza']
        prixPiz = form.cleaned_data['prix']
        piz = Pizza()
        piz.nomPizza = nomPiz
        piz.prix = prixPiz
        piz.save()
        return render(
            request,
            "applipizza/traitementFormulaireCreationPizza.html",
            {"nom" : nomPiz ,
            "prix" : prixPiz}
        )

def ajouterIngredientDansPizza(request, pizza_id) :
    
    formulaire = CompositionForm(request.POST)

    if formulaire.is_valid() :

        idIng = formulaire.cleaned_data['ingredient']
        qte = formulaire.cleaned_data['quantite']

        compo = Composition()
        compo.ingredient = Ingredient.objects.get(idIngredient = idIng.idIngredient)
        compo.pizza = Pizza.objects.get(idPizza = pizza_id)
        compo.quantite = qte

        compo.save()

    formulaire = CompositionForm()
    laPizza = Pizza.objects.get(idPizza = pizza_id)
    compo = Composition.objects.filter(pizza = pizza_id)
    listeIngredients = []

    for c in compo :
        ing = Ingredient.objects.get(idIngredient = c.ingredient.idIngredient)
        listeIngredients.append({"nom" : ing.nomIngredient, "qte" : c.quantite})

    return render(
        request,
        "applipizza/pizza.html",
        {"pizza" : laPizza,
        'composition' : compo,
        "liste" : listeIngredients,
        "form" : formulaire}
    )