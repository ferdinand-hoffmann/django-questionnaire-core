from django.conf.urls import url
from django.urls import reverse

from questionnaire_core.models import Questionnaire, QuestionnaireResult
from questionnaire_core.views.generic import QuestionnaireFormView


class TestQuestionnaireView(QuestionnaireFormView):
    template_name = 'test_base.html'

    def get_questionnaire(self):
        return Questionnaire.objects.get(title='test1')  # questionnaire from fixture

    def get_questionnaire_result_set(self):
        return QuestionnaireResult(questionnaire=self.get_questionnaire())

    def get_success_url(self):
        return reverse('test_view')


urlpatterns = (
    url(r'^questionnaire/$', TestQuestionnaireView.as_view(), name='test_view'),
)
