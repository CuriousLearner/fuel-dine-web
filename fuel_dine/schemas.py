# Third Party Stuff
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator, SchemaView
from rest_framework_swagger.views import get_swagger_view


class MySchemaView(SchemaView):
    permission_classes = (AllowAny,)


def get_schema_view(title=None, url=None, description=None, urlconf=None, renderer_classes=None, public=False):
    """Return a schema view.
    """
    generator = SchemaGenerator(title=title, url=url, description=description, urlconf=urlconf)
    return MySchemaView.as_view(
        renderer_classes=renderer_classes,
        schema_generator=generator,
        public=public,
    )


schema_view = get_schema_view(
    title='fuel_dine API',
    description='Decide whether team should dine in a restaurant',
    public=True
)

swagger_schema_view = get_swagger_view(title='fuel_dine API Playground')
