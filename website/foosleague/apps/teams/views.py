from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages import error, success
from django.http.response import HttpResponseRedirect

from mixins.views import LoginRequiredMixin

from .models import Team
from .forms import TeamForm


class TeamListView(ListView):
    model = Team
    template_name = "teams/list.html"


class TeamDetailView(DetailView):
    model = Team
    template_name = "teams/detail.html"


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "teams/update.html"
    form_class = TeamForm

    def dispatch(self, *args, **kwargs):
        team = self.get_object()
        if team.player_1.user != self.request.user and team.player_2.user != self.request.user:
            error(self.request, "You must be apart of this team to edit")
            return HttpResponseRedirect(reverse_lazy("team-detail", kwargs={'pk': team.id}))

        return super(TeamUpdateView, self).dispatch(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = self.form_class(
            self.request.POST or None, self.request.FILES or None, instance=self.get_object())
        return form

    def form_valid(self, form):
        c = form.save()
        success(self.request, "%s successfully updated" % (c.name,))
        return HttpResponseRedirect(reverse_lazy('team-detail', kwargs={'pk': c.id}))