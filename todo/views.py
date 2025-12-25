from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import ToDo


def home(request: HttpRequest) -> HttpResponse:
    todos = ToDo.objects.all().order_by("-created_at")
    return render(request, "home.html", {"todos": todos})


def add_todo(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            ToDo.objects.create(title=title)
            messages.success(request, "Task added successfully!")
    return redirect("home")


def toggle_todo(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    todo.completed = not todo.completed
    todo.save()

    if todo.completed:
        msg = "Task marked as completed"
    else:
        msg = "Task marked as not completed"

    messages.success(request, msg)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"completed": todo.completed, "message": msg})

    return redirect("home")


def update_todo(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    if todo.completed:
        messages.error(request, "Cannot edit a completed task!")
        return redirect("home")
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            todo.title = title
            todo.save()
            messages.success(request, "Task updated successfully!")
        return redirect("home")
    return render(request, "update.html", {"todo": todo})


def delete_todo(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    todo.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect("home")
