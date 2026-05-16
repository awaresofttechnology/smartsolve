import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Contact

logger = logging.getLogger(__name__)


SERVICES = [
    {
        "slug": "web-design",
        "title": "Web Design",
        "icon_color": "#1a6fd4",
        "icon_bg": "#e8f0fb",
        "desc": "Pixel-perfect, brand-consistent UI/UX design that converts visitors into loyal customers across every device.",
        "tags": ["UI/UX", "Responsive", "Branding"],
    },
    {
        "slug": "web-development",
        "title": "Web Development",
        "icon_color": "#7c3aed",
        "icon_bg": "#f0ebff",
        "desc": "Robust, scalable full-stack web applications built with modern frameworks and best-practice architecture.",
        "tags": ["React", "Node.js", "APIs"],
    },
    {
        "slug": "seo-ranking",
        "title": "SEO Ranking",
        "icon_color": "#f59e0b",
        "icon_bg": "#fff7e6",
        "desc": "Data-backed on-page and off-page SEO strategies that propel your site to Google's first page and keep it there.",
        "tags": ["On-Page", "Technical", "Analytics"],
    },
    {
        "slug": "link-building",
        "title": "Link Building",
        "icon_color": "#ef4444",
        "icon_bg": "#fef2f2",
        "desc": "High-authority backlink acquisition through ethical outreach, guest posting, and strategic digital PR.",
        "tags": ["Backlinks", "Outreach", "DA/PA"],
    },
    {
        "slug": "traffic-growth",
        "title": "Traffic Growth",
        "icon_color": "#06b6d4",
        "icon_bg": "#e0f9ff",
        "desc": "Multi-channel organic and paid traffic strategies that funnel qualified visitors to your conversion pages.",
        "tags": ["PPC", "Social", "Content"],
    },
    {
        "slug": "software-development",
        "title": "Software Development",
        "icon_color": "#10b981",
        "icon_bg": "#e6faf3",
        "desc": "Custom enterprise software — from SaaS platforms to mobile apps — engineered for performance and longevity.",
        "tags": ["SaaS", "Mobile", "Cloud"],
    },
    {
        "slug": "keyword-research",
        "title": "Keyword Research",
        "icon_color": "#f97316",
        "icon_bg": "#fff4ed",
        "desc": "Uncover high-intent, low-competition keywords that your audience actually searches — and build content around them.",
        "tags": ["Long-tail", "Intent", "Gaps"],
    },
    {
        "slug": "sitemap-optimization",
        "title": "Sitemap Optimization",
        "icon_color": "#8b5cf6",
        "icon_bg": "#f3eeff",
        "desc": "Structured XML and HTML sitemaps that help search engines crawl, index, and understand every page you publish.",
        "tags": ["XML", "Crawl", "Indexing"],
    },
]

STATS = [
    {"number": 500, "suffix": "+", "label": "Projects Completed"},
    {"number": 98,  "suffix": "%", "label": "Client Satisfaction"},
    {"number": 30,  "suffix": "+", "label": "Industries Served"},
    {"number": 12,  "suffix": "+", "label": "Years in Business"},
    {"number": 40,  "suffix": "+", "label": "Expert Professionals"},
]

TESTIMONIALS = [
    {
        "stars": 5,
        "quote": "SmartSync tripled our organic traffic in 6 months. Their SEO and link-building team genuinely understands our market.",
        "name": "Rahul Kumar",
        "role": "CEO, FinEdge Solutions",
        "initials": "RK",
        "color": "#1a6fd4",
        "featured": False,
    },
    {
        "stars": 5,
        "quote": "The web development pod delivered a complex SaaS dashboard two weeks ahead of schedule. Best agency we've worked with in a decade.",
        "name": "Sophia Martel",
        "role": "CTO, CloudFlow Inc.",
        "initials": "SM",
        "color": "#7c3aed",
        "featured": True,
    },
    {
        "stars": 5,
        "quote": "Keyword research + sitemap optimization brought us to position #1 for 14 high-value search terms. ROI exceeded 400%.",
        "name": "James Patel",
        "role": "Marketing Head, RetailPro",
        "initials": "JP",
        "color": "#10b981",
        "featured": False,
    },
]

INDUSTRIES = [
    {"icon": "🏦", "label": "Finance & Banking"},
    {"icon": "🏥", "label": "Healthcare"},
    {"icon": "🛒", "label": "E-Commerce"},
    {"icon": "🎓", "label": "Education"},
    {"icon": "🏭", "label": "Manufacturing"},
    {"icon": "🚗", "label": "Automotive"},
    {"icon": "✈️", "label": "Travel & Tourism"},
    {"icon": "🏗️", "label": "Real Estate"},
]


def home(request):
    context = {
        "services": SERVICES,
        "stats": STATS,
        "testimonials": TESTIMONIALS,
        "industries": INDUSTRIES,
    }
    return render(request, "core/index.html", context)


@require_POST
def contact_submit(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

    form = ContactForm(data)
    if not form.is_valid():
        errors = {field: errs[0] for field, errs in form.errors.items()}
        return JsonResponse({"status": "error", "errors": errors}, status=422)

    Contact.objects.create(**form.cleaned_data)
    logger.info("Contact form submission saved from %s", form.cleaned_data["email"])
    return JsonResponse({"status": "ok", "message": "Thanks! We'll be in touch soon."})
