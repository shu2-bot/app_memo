from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from matplotlib.pyplot import get
from memo.models import Memo
from django.contrib.auth.decorators import login_required
from memo.forms import MemoForm
from django.views.decorators.http import require_GET, require_POST

# Create your views here.
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
            return redirect(memo_detail, memo_id = memo.pk)
    else:
        form = MemoForm()
    return render(request, "memo_new.html", {"form":form})

@require_GET
@login_required
def memo_edit(request, memo_id):
    memo = get_object_or_404(Memo, pk=memo_id)
    if memo.created_by_id != request.user.id:
        return HttpResponseForbidden("このメモの編集は許可されていません")

    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memo_detail', memo_id = memo_id)
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memo_edit.html', {"form":form})

def memo_detail(request, memo_id):
    """
    memo = get_object_or_404(Memo, pk=memo_id)
    context = {"memo":memo}
    """
    try:
        memo = Memo.objects.get(id=memo_id)
        context = {"memo":memo}
    except Memo.DoesNotExist:
        return HttpResponseNotFound("Memo is not found!!")

    return render(request, "memo_detail.html", context)