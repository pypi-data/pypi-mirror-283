from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET


APP_TITLE = 'Django Rahavard Robots'
APP_SLUG  = 'django rahavard robots'

rules = ''

if settings.ALLOW_GOOGLE_BOTS:
    for gb in [
        'AdsBot-Google',
        'AdsBot-Google-Mobile',
        'AdsBot-Google-Mobile-Apps',
        'APIs-Google',
        'DuplexWeb-Google',
        'Feedfetcher-Google',
        'Google',
        'Google AdSense',
        'Google Feedfetcher',
        'Google Plus Share',
        'Google-Ads',
        'Google-Read-Aloud',
        'Google-Shopping',
        'Google-Structured-Data-Testing-Tool',
        'GoogleAssociationService',
        'Googlebot',
        'Googlebot-Image',
        'Googlebot-Mobile',
        'Googlebot-News',
        'Googlebot-Video',
        'GoogleBot',
        'GoogleDocs',
        'GoogleSites',
        'googleweblight',
        'iGooglePortal',
        'Mediapartners-Google',
        'Storebot-Google ',
    ]:
        rules += f'User-agent: {gb}\n'
        rules += 'Disallow: /cgi-bin*\n'
        rules += 'Disallow: /static*\n'
        rules += 'Disallow: /staticfiles*\n\n'

rules += 'User-agent: *\n'
rules += 'Disallow: *\n'


## https://adamj.eu/tech/2020/02/10/robots-txt/
@require_GET
def robots(request):
    return HttpResponse(
        rules,
        content_type='text/plain'
    )
