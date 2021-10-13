from django import forms

from .models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeForm(forms.ModelForm):
    error_css_class = "error-field"
    required_css_class = "required-field"
    name = forms.CharField(help_text="Texto de ajuda!")

    class Meta:
        model = Recipe
        fields = ["name", "description", "directions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "placeholder": f"Receita {str(field)}",
                "class": "form-contol",
            }
            self.fields[str(field)].widget.attrs.update(new_data)
            self.fields[str(field)].label = ""

        self.fields["description"].widget.attrs.update({"rows": "2"})
        self.fields["directions"].widget.attrs.update({"rows": "4"})


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["name", "quantity", "unit"]


class RecipeIngredientImageForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredientImage
        fields = ["image"]
