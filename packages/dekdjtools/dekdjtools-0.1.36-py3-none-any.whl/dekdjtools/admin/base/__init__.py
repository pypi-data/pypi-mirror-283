import sys
import functools
from django.db.models.fields.files import FieldFile
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.main import ChangeList
from ...utils.model import ModelFields


class MetaClass(admin.ModelAdmin.__class__):
    def __new__(mcs, name, bases, attrs):
        new_class = super(MetaClass, mcs).__new__(mcs, name, bases, attrs)
        if new_class._model_cls:
            admin.site.register(new_class._model_cls, new_class)
        return new_class


class ModelAdminAbstract(admin.ModelAdmin, metaclass=MetaClass):
    _model_cls = None


class ModelAdminBase(ModelAdminAbstract):
    _img_width = 50

    @property
    @functools.lru_cache(None)
    def _cl(self) -> ChangeList:
        count = 3  # only be used in custom field function, search for: lookup_field(field_name, result, cl.model_admin)
        while True:
            frame = sys._getframe(count)
            if 'cl' in frame.f_locals:
                return frame.f_locals['cl']
            count += 1

    @property
    @functools.lru_cache(None)
    def _results_index(self) -> dict:
        return {obj.pk: index for index, obj in enumerate(self._cl.result_list)}

    def _get_obj_index(self, obj):
        return (self._cl.page_num - 1) * self._cl.list_per_page + self._results_index[obj.pk]

    def row_index_(self, obj):
        return self._get_obj_index(obj) + 1

    row_index_.short_description = _("序号")

    @staticmethod
    def get_url(obj):
        if isinstance(obj, FieldFile):
            return obj.url
        return obj

    @classmethod
    def format_img(cls, img):
        if img:
            img = cls.get_url(img)
            return format_html('<img src="{0}" width="{1}" height="{1}"/>'.format(img, cls._img_width))
        else:
            return ""

    @classmethod
    def format_aimg(cls, img):
        if img:
            img = cls.get_url(img)
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" width="{1}" height="{1}"/></a>'.
                format(img, cls._img_width))
        else:
            return ""

    @classmethod
    def format_imgs(cls, img_list):
        return format_html("".join([cls.format_img(x) for x in img_list]))

    @classmethod
    def format_aimgs(cls, img_list):
        return format_html("".join([cls.format_aimg(x) for x in img_list]))

    @staticmethod
    def format_tags(tags, ml=None, sep=' '):
        if ml is not None:
            tags = sorted(tags, key=lambda x: len(x))
            r = ""
            for tag in tags:
                temp = ""
                if r:
                    temp += sep
                temp += tag
                if len(r) + len(temp) > ml:
                    return r
                r += temp
            return r
        return sep.join(tags)

    @classmethod
    def format_a(cls, url, text=None, target=None):
        if url:
            url = cls.get_url(url)
            target = target or '_blank'
            if callable(text):
                text = text(url)
            elif text == 0:
                text = url
            elif text is None:
                text = url.rsplit('/', 1)[-1]
            return format_html("<a href='{url}' target='{target}'>{text}</a>", url=url, text=text, target=target)
        return ""


def calc_list_display(_model_cls, rewrite_set=None, disable_set=None, rewrite_suffix='_'):
    array = []
    mfs = ModelFields(_model_cls)
    for name in mfs.sort_fields(mfs.auto.keys(), mfs.common.keys(), mfs.o2o.keys(), mfs.o2m.keys()):
        if disable_set and name in disable_set:
            continue
        if rewrite_set and name in rewrite_set:
            name += rewrite_suffix
        array.append(name)
    return tuple(array)


def calc_search_fields(_model_cls, list_display=None, disable_set=None):
    array = []
    mfs = ModelFields(_model_cls)
    for name in mfs.sort_fields(mfs.auto.keys(), mfs.common.keys(), mfs.o2o.keys(), mfs.o2m.keys()):
        if disable_set and name in disable_set:
            continue
        array.append(name)
    return tuple(item for item in array if item in list_display) if list_display else tuple(array)


def admin_register(_model_cls, list_display=None):
    list_display = list_display or calc_list_display(_model_cls)
    type(
        'admin',
        (ModelAdminBase,),
        {
            '_model_cls': _model_cls,
            'list_display': list_display,
            'search_fields': calc_search_fields(_model_cls, list_display)
        }
    )


def admin_register_batch(_model_cls_list):
    for _model_cls in _model_cls_list:
        admin_register(_model_cls)
