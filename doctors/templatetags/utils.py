from django import template
register = template.Library()


@register.inclusion_tag("template_tags/field_layout.html")
def field_layout(field, horizontal=False):
    return dict(
        field=field,
        horizontal=horizontal
    )


def verbose_name(instance, field_name):
    model = instance.__class__
    return model._meta.get_field(field_name).verbose_name


@register.inclusion_tag(
    "template_tags/nav_link_collapsed.html", takes_context=True
)
def nav_link_collapsed(context, url_name, title):
    context["url_name"] = url_name
    context["title"] = title
    return context


@register.inclusion_tag(
    "template_tags/display_subdeclaration_display.html"
)
def display_subdeclaration_display(
    declaration,
    title_field,
    band_field,
    details_field,
    boolean_fields=None
):
    """
    Displays a subsection of a delcaration

    We only show it if the title field is True.
    We then show the verbose name of the title.

    Boolean fields are also return to the template
    as their verbose names but only if they are true.
    """

    if not getattr(declaration, title_field):
        return {
            "hide": True
        }

    title = verbose_name(declaration, title_field)
    boolean_titles = []
    if boolean_fields:
        boolean_fields = boolean_fields.split(",")
        for boolean_field in boolean_fields:
            if getattr(declaration, boolean_field):
                boolean_titles.append(
                    verbose_name(declaration, boolean_field)
                )

    return {
        "title": title,
        "details_value": getattr(declaration, details_field),
        "band_value": getattr(declaration, band_field),
        "boolean_titles": boolean_titles
    }
