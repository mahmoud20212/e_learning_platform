# from slugify import slugify

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Course, Subject


# @receiver(post_save, sender=Subject)
# def subject_title_changed(sender, instance, created, **kwargs):
#     new_slug = slugify(instance.title, to_lower=True)
#     Subject.objects.filter(id=instance.id).update(slug=new_slug)


# @receiver(post_save, sender=Course)
# def course_title_changed(sender, instance, created, **kwargs):
#     new_slug = slugify(instance.title, to_lower=True)
#     Course.objects.filter(id=instance.id).update(slug=new_slug)
