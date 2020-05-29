from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from .models import *
# Register your models here.
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

class MoviesAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movies
        fields = '__all__'

    def clean_trailer(self):
        val = self.cleaned_data['trailer']
        if '=' in val:
            sp = val.split('=')
            val = 'https://www.youtube.com/embed/' + sp[-1]
            return val
        return val



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url' )
    list_display_links = ('name', 'id')


class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image} width="110"')

    get_image.short_description = 'Изображение'


@admin.register(Movies)
class MoviesAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'category', 'tagline', 'draft')
    list_display_links = ('title', 'id')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('title', 'description', 'category__name')
    inlines = [MovieShotsInline, ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    form = MoviesAdminForm
    readonly_fields = ['get_image']
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
            }),
        (None, {
            'fields': (('description', 'poster', 'trailer'), )
            }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'), )
            }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'genre', 'directors', 'category'), )
            }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'), )
            }),
        ('Options', {
            'fields': (('url', 'draft'), )
            }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image} width="110"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('name', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image} width="50"')

    get_image.short_description = 'Изображение'


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image} width="50"')

    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star','ip', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)


admin.site.site_title = 'Фильмы 228'
admin.site.site_header = 'Фильмы 228'
