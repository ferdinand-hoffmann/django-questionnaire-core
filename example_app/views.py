from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

from questionnaire_core.models import Questionnaire, QuestionnaireResult
from questionnaire_core.views.generic import QuestionnaireFormView


class BasicQuestionnaireView(QuestionnaireFormView):
    template_name = 'questionnaire_form.html'

    def get_questionnaire(self):
        return Questionnaire.objects.get(pk=self.kwargs.get('pk'))

    def get_questionnaire_result_set(self):
        if self.request.GET.get('result_set'):
            return QuestionnaireResult.objects.get(pk=self.request.GET.get('result_set'))
        return QuestionnaireResult(questionnaire=self.get_questionnaire())

    def get_success_url(self):
        return reverse('basic_questionnaire_form', args=(self.kwargs.get('pk'),))

    def form_valid(self, form):
        # Add current result set to the url (allows editing of the result)
        redirect = super(BasicQuestionnaireView, self).form_valid(form)
        url_params = urlencode({'result_set': form.current_result_set.pk})
        return HttpResponseRedirect('{url}?{params}'.format(url=redirect.url, params=url_params))
