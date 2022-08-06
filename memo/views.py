from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from matplotlib.pyplot import get
from numpy import quantile
from memo.models import Memo
from django.contrib.auth.decorators import login_required
from memo.forms import MemoForm
from django.views.decorators.http import require_GET, require_POST
from urllib.parse import quote

# Create your views here.
@login_required
def top(request):
    memos = Memo.objects.all()
    context = {"memos": memos}
    return render(request, "top.html", context)

@login_required
def memo_new(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.created_by = request.user
            memo.save()
            return redirect(memo_detail, memo_id = memo.id)
    else:
        form = MemoForm()
    return render(request, "memo_new.html", {"form":form})

@login_required
def memo_edit(request, memo_id):
    memo = get_object_or_404(Memo, pk=memo_id)
    """
    if memo.created_by_id != request.user.id:
        return HttpResponseForbidden("このメモの編集は許可されていません")
    """

    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memo_detail', memo_id = memo_id)
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memo_edit.html', {"form":form})

@require_GET
@login_required
def memo_detail(request, memo_id):
    """
    memo = get_object_or_404(Memo, pk=memo_id)
    context = {"memo":memo}
    """
    try:
        memo = Memo.objects.get(id=memo_id)
        context = {"memo":memo}
    except Memo.DoesNotExist:
        #raise Http404("Memo is not found!!")
        return handlar404(request, Http404)
    return render(request, "memo_detail.html", context)

def handlar404(request, exception):
    context = {"request_path":quote(request.path)}
    return render(request, 'error/404.html', context, status = 404)