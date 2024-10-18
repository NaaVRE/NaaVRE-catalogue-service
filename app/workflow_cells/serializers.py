from rest_framework import serializers

from base_assets.serializers import BaseAssetSerializer
from . import models


class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseImage
        fields = ['build', 'runtime']


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ['name', 'module', 'asname']


class BaseVariableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'type']


class InputSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Input


class OutputSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Output


class ConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conf
        fields = ['name', 'assignation']


class ParamSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Param
        fields = BaseVariableSerializer.Meta.fields + ['default_value']


class SecretSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Secret


class CellSerializer(BaseAssetSerializer):
    base_container_image = BaseImageSerializer(required=False)
    dependencies = DependencySerializer(many=True, required=False)
    inputs = InputSerializer(many=True, required=False)
    outputs = OutputSerializer(many=True, required=False)
    confs = ConfSerializer(many=True, required=False)
    params = ParamSerializer(many=True, required=False)
    secrets = SecretSerializer(many=True, required=False)

    nested_serializer_classes = {
        'base_container_image': BaseImageSerializer,
        }
    nested_serializer_classes_many = {
        'dependencies': DependencySerializer,
        'inputs': InputSerializer,
        'outputs': OutputSerializer,
        'confs': ConfSerializer,
        'params': ParamSerializer,
        'secrets': SecretSerializer,
        }

    class Meta(BaseAssetSerializer.Meta):
        model = models.Cell
        fields = '__all__'

    @staticmethod
    def create_nested_instance(
            name, serializer_class, data, parent_instance=None, many=False,
            ):
        if data is None:
            if many:
                return []
            else:
                return None
        serializer = serializer_class(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update_nested_instance(
            name, serializer_class, data, parent_instance=None, many=False,
            ):
        if many:
            # FIXME: it's unclear how to deal with this. DRF message states:
            # "Serializers with many=True do not support multiple update by
            # default, only multiple create. For updates it is unclear how to
            # deal with insertions and deletions. If you need to support
            # multiple update, use a `ListSerializer` class and override
            # `.update()` so you can specify the behavior exactly."
            # Could try
            # https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
            # But how to chose which objects to update vs remove or recreate,
            # because the serialized data intentionally doesn't have PKs
            instances = parent_instance.__getattribute__(name).all()
            serializer = serializer_class(instances, many=True)
            # if data is not None:
            #     instances = serializer.update(instances, data)
            # FIXME: for now return [], which results in no data updates
            return []
        else:
            instance = parent_instance.__getattribute__(name)
            serializer = serializer_class(instance)
            if data is not None:
                instance = serializer.update(instance, data)
            return instance

    @staticmethod
    def extract_nested_instances(
            serializer_classes, get_instance, data, instance=None, many=False,
            ):
        """ Extract nested field entries from validated data and convert them
        to model instances

        :param serializer_classes: dict where keys are names of nested fields,
            and values are their respective serializer classes
        :param get_instance: a function that converts a nested field's data
            into a model instance, or None. Depending on the context, this
            function may create a new instance, or retrieve an existing one.
            If many=true, the function expects a list of validated data and
            returns a list of instances.
        :param data: the main serializer's validated data
        :param instance: the main serializer's instance, or None
        :param many: boolean
        :return: a dictionary where keys are names of nested fields, and
            values are model instances (or lists thereof if many=True)
        """
        instances = {
            name: get_instance(
                name,
                serializer_class,
                data.pop(name, None),
                parent_instance=instance,
                many=many,
                )
            for name, serializer_class in serializer_classes.items()
            }
        return instances

    def create(self, validated_data):
        nested_instances = self.extract_nested_instances(
            self.nested_serializer_classes,
            self.create_nested_instance,
            validated_data,
            )
        nested_instances_many = self.extract_nested_instances(
            self.nested_serializer_classes_many,
            self.create_nested_instance,
            validated_data,
            many=True,
            )
        instance = models.Cell.objects.create(
            **nested_instances,
            **validated_data,
            )
        for name, nested_instance in nested_instances_many.items():
            instance.__getattribute__(name).set(nested_instance)
        return instance

    def update(self, instance, validated_data):
        nested_instances = self.extract_nested_instances(
            self.nested_serializer_classes,
            self.update_nested_instance,
            validated_data,
            instance=instance,
            )
        nested_instances_many = self.extract_nested_instances(
            self.nested_serializer_classes_many,
            self.update_nested_instance,
            validated_data,
            instance=instance,
            many=True,
            )
        return super().update(instance, validated_data)
