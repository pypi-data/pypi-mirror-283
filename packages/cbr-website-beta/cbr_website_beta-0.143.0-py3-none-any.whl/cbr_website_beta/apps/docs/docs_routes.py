from flask import render_template

from cbr_website_beta.apps.docs                                 import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous
from cbr_website_beta.content.CBR__Content__Static              import cbr_content_static

EXPECTED_ROUTES__MINERVA = [ '/docs']

@blueprint.route('')
#@blueprint.route('/')                  # this is not working with the route ''
@blueprint.route('/<path:path>')
@allow_anonymous
def minerva_root(path='/'):
    content_view    = 'docs/index.html'
    template_name = '/pages/page_with_view.html'
    title         = 'Documentation'
    if path == '' or path == '/':
        path = 'index'
    content       = cbr_content_static.file_contents__for__web_page(path)
    folders       = cbr_content_static.folders(path)
    files         = cbr_content_static.files  (path)
    base_folder   = 'docs'
    return render_template(template_name_or_list = template_name,
                           title                 =  title       ,
                           content_view          = content_view ,
                           path                  = path         ,
                           content               = content      ,
                           files                 = files        ,
                           folders               = folders      ,
                           base_folder           = base_folder  )

