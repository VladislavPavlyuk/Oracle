import re

from django import forms

from team.models import TeamMember


class TeamMemberCreateForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "salary", "note", "photo"]
        labels = {
            'name': "Name",
            'salary': "Salary",
            'note': "Note",
            'photo': "Photo",
        }
        help_texts = {
            "name": "Enter a name, please",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter a name",
                    "class": "form-control",
                }
            ),
            "salary": forms.NumberInput(
                attrs={
                    "min": "0",
                    "class": "form-control",
                    "step": "1",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "placeholder": "Enter a note",
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control-file",
                'accept': "image/*",
            })
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        words = name.split()

        if len(words) != 2:
            raise forms.ValidationError("Name have to be two words.")

        for word in words:
            if any(ch.isdigit() for ch in word):
                raise forms.ValidationError("Name field should contain only digits.")
            if len(word) < 3:
                raise forms.ValidationError("Every word should have at least 3 digits.")
            if not re.fullmatch(r"[A-Za-z]+", word):
                raise forms.ValidationError("Letters are allowed only.")

        return name


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        label="Enter a name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter a name",
                "class": "form-control",
            }
        ),
    )
    min_salary = forms.IntegerField(
        label="Minimum salary",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Enter a minimum salary",
                "class": "form-control",
                "min": "0",
            }
        ),
    )
    max_salary = forms.IntegerField(
        label="Maximum salary",
        required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Enter a maximum salary",
                "class": "form-control",
                "min": "0",
            }
        ),
    )
