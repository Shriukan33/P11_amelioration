from django.views.generic import TemplateView


class LegalMentionsView(TemplateView):
    """
    Class-based view for legal_mentions.html.
    """
    template_name = 'legal_mentions/legal_mentions.html'
