from django.shortcuts import render
from .forms import EditForm
from django.utils.text import slugify

def submit_topic(request, write_index):
    print(request.user.is_authenticated)
    form = EditForm(data=request.POST or None, label_suffix='')
    print(form.is_valid())
    if request.method == 'POST' and form.is_valid():
        
        submit_page = form.save(commit=False)
        submit_page.slug = slugify(submit_page.title)
        topic = write_index.add_child(instance=submit_page)
        if topic:
            topic.unpublish()
            # Submit page for moderation. This requires first saving a revision.
            topic.save_revision(submitted_for_moderation=True)
            # Then send the notification to all Wagtail moderators.
        return render(request, 'coderedcms/pages/submit_topic_success.html', {"user": request.user})
    context = {
        'form': form,
        'edit_index': write_index,
    }
    return render(request, 'coderedcms/pages/submit_topic.html', context)
