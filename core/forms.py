from django import forms


SERVICE_CHOICES = [
    ("web-design", "Web Design"),
    ("web-development", "Web Development"),
    ("seo-ranking", "SEO Ranking"),
    ("link-building", "Link Building"),
    ("traffic-growth", "Traffic Growth"),
    ("software-development", "Software Development"),
    ("keyword-research", "Keyword Research"),
    ("sitemap-optimization", "Sitemap Optimization"),
    ("full-package", "Full-Service Package"),
]


class ContactForm(forms.Form):
    fname = forms.CharField(max_length=50, strip=True)
    lname = forms.CharField(max_length=50, strip=True)
    email = forms.EmailField(max_length=254)
    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    message = forms.CharField(max_length=2000, strip=True)
