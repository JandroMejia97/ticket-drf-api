from rest_framework.serializers import ModelSerializer


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    This class takes the additional argument 'fields'
    which tells you which fields are to be displayed
    """

    def __init__(self, *args, **kwargs):
        # Taking 'fields' argument.
        context = kwargs.get('context', None)
        fields = None
        if context:
            fields = context.get('fields')
        else:
            # Don't pass the 'fields' arg up to the superclass
            fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)