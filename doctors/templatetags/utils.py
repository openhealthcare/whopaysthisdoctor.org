from django import template
register = template.Library()


@register.inclusion_tag("template_tags/field_layout.html")
def field_layout(field, horizontal=False):
    return dict(
        field=field,
        horizontal=horizontal
    )


def verbose_name(model, field_name):
    return getattr(model.__class__, field_name).verbose_name


@register.inclusion_tag("template_tags/declaration_display.html")
def field_display(
    model, field_name
):
    return {
        "title": verbose_name(model, field_name),
        "value": getattr(model, field_name)
}

