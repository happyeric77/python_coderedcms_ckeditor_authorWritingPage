# User Draft Writing Page

## Preview

![preview#1](https://lh3.googleusercontent.com/pw/ACtC-3fVQs59cqanUatzkogo-XUhXNR6BK2U2T_Oxr8i2yJUU85Ey2Eml4WGaesKJXvCV-GJjQ85SwA5sCKecFhTPG7N6DL776td2Muk3AbL2XzXjeq0er4wxxQ5SwPE4deZY-09ETrGKnzyjwKBEILQlKibkA=w1762-h944-no?authuser=0)


### Dependencies of this feature:

coderedcms==0.20.*
django-ckeditor==6.1.0

### model.py

- A new draft field and add it into content_panel
```
class ArticlePage(CoderedArticlePage):
    ...
    # New field for user's pre submitting 
    draft = CkRichTextField(blank=True)
    
    content_panels = CoderedWebPage.content_panels + [
        ...
        # Add draft field into content_panel
        FieldPanel('draft'),
        ...
    ]
    ...
```

- A new model for Writing draft's landing page

The model play the key role to route users' request to certain view (explained in views.py section)

```
class WriteLandingPage(RoutablePageMixin, CoderedArticlePage):
    """
    Landing Page of Write draft
    """
    class Meta:
        verbose_name = 'Write Landing Page'

    template = 'coderedcms/pages/write_landing_page.html'    

    @route('')
    def submit(self, request):
        from .views import submit_topic
        return submit_topic(request, self)

```

** Note1: the argument of route() is changeable according to what url you want users to put in to access Writing Draft Page. In this case, we want users to directly go into Writing Draft Page when they input the WritingLandingPage's url.


### forms.py

Create a model form which is accessable from template.

```
from django.forms import ModelForm
from .models import ArticlePage

class EditForm(ModelForm):
    class Meta:
        model = ArticlePage
        fields = ['draft', 'title']
```
** note: "fields" property is adjustable according which fields would like users to access. In this case, user can only manipulate draft and title field of article page.



### views.py

The submit_topic view determines the logic when users click the sumbit button on writing draft page.

```
from django.shortcuts import render
from .forms import EditForm
from django.utils.text import slugify

def submit_topic(request, article_index):
    # check whether or not the author is logged in
    if request.user.is_authenticated:
        # If yes, instantiate EditForm
        form = EditForm(data=request.POST or None, label_suffix='')
        # If the request from author is a POST, check if all fields are valid.
        if request.method == 'POST' and form.is_valid():
            # If all fields in post form are valid, create a new article under article_index and render submit_topic_success.html
            submit_page = form.save(commit=False)
            submit_page.slug = slugify(submit_page.title)
            topic = article_index.add_child(instance=submit_page)
            if topic:
                topic.unpublish()
                topic.save_revision(submitted_for_moderation=True)
                return render(request, 'coderedcms/pages/submit_topic_success.html', {"user": request.user})
        context = {
            'form': form,
            'edit_index': article_index,
        }
        # If the request is not a POST or the posted form fields are not valid, render submit_topic.html html.
        return render(request, 'coderedcms/pages/submit_topic.html', context)
        # If the request is not from a logged in user, render request_login.html page.
    return render(request, 'coderedcms/pages/request_login.html')

```

### Newly created teamplated rendered from the view above.

- website/templates/coderedcms/pages/submit_topic_success.html
- website/templates/coderedcms/pages/submit_topic.html
- website/templates/coderedcms/pages/request_login.html


