# app_uploads/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UploadsDocs
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from django.core.files.storage import default_storage



@receiver(post_save, sender=UploadsDocs)
def comprimir_arquivo_apos_upload(sender, instance, created, **kwargs):
    if not created:
        return

    path = instance.arquivo.path
    ext = path.lower().split('.')[-1]

    try:
        if ext in ['jpg', 'jpeg', 'png']:
            imagem = Image.open(path)
            imagem = imagem.convert('RGB')
            imagem.save(path, optimize=True, quality=65)

        elif ext == 'pdf':
            reader = PdfReader(path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            with open(path, "wb") as f:
                writer.write(f)

    except Exception as e:
        print(f"Erro ao comprimir: {e}")
