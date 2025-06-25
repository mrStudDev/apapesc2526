# core/base_imports.py
from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

from django.contrib import messages

from app_accounts.models import CustomUser

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import get_user_model

from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
    )