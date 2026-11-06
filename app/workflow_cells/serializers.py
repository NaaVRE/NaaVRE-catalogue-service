import hashlib

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from base_assets.serializers import (
    BaseAssetSerializer,
    VersioningSerializerMixin,
    )
from . import models


class BaseImageSerializer(serializers.ModelSerializer):
    """ Base image of a cell, in one of two shapes:

    - flavor image: {"build": str, "runtime": str}
    - binder environment image: {"binder_environment": str}

    On write, exactly one shape must be provided, with non-empty values.
    On read, only the keys of the shape in use are returned (existing rows
    with empty build and runtime are returned as a flavor image).
    """
    FLAVOR_FIELDS = ('build', 'runtime')
    BINDER_FIELDS = ('binder_environment',)

    class Meta:
        model = models.BaseImage
        fields = ['build', 'runtime', 'binder_environment']

    def to_internal_value(self, data):
        if isinstance(data, dict):
            unknown_keys = sorted(set(data) - set(self.fields))
            if unknown_keys:
                raise serializers.ValidationError(
                    {key: ['Unknown field.'] for key in unknown_keys}
                    )
        return super().to_internal_value(data)

    def validate(self, attrs):
        is_flavor = (
            all(attrs.get(f) for f in self.FLAVOR_FIELDS)
            and not any(attrs.get(f) for f in self.BINDER_FIELDS)
            )
        is_binder_environment = (
            all(attrs.get(f) for f in self.BINDER_FIELDS)
            and not any(attrs.get(f) for f in self.FLAVOR_FIELDS)
            )
        if not (is_flavor or is_binder_environment):
            raise serializers.ValidationError(
                'base_container_image must be either {"build": str, '
                '"runtime": str} or {"binder_environment": str}, with '
                'non-empty values.'
                )
        # Specify all fields to avoid leaving stale values set when switching format on an update.
        return {f: attrs.get(f, '') for f in self.Meta.fields}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.binder_environment:
            keys = self.BINDER_FIELDS
        else:
            keys = self.FLAVOR_FIELDS
        return {key: data[key] for key in keys}


class CellContainerizationJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CellContainerizationJob
        fields = ["html_url", "status", "conclusion"]


class CellNestedFieldSerializer(serializers.ListSerializer):
    def _data_hash(self, data):
        json = JSONRenderer().render(data)
        return hashlib.sha1(json).hexdigest()

    def _instance_hash(self, instance):
        serializer_class = self.child.__class__
        data = serializer_class(instance).data
        return self._data_hash(data)

    def update(self, instance, validated_data):
        # use hash of the serialized instances and data as deterministic ids
        instance_mapping = {self._instance_hash(inst): inst for inst in instance}
        data_mapping = {self._data_hash(dat): dat for dat in validated_data}

        # Perform creations and updates
        ret = []
        for item_hash, data in data_mapping.items():
            instance = instance_mapping.get(item_hash)
            if instance is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(instance, data))

        # Perform deletions
        for item_hash, item in instance_mapping.items():
            if item_hash not in data_mapping:
                item.delete()

        return ret


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ['name', 'module', 'asname']
        list_serializer_class = CellNestedFieldSerializer


class BaseVariableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'type']
        list_serializer_class = CellNestedFieldSerializer


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
        list_serializer_class = CellNestedFieldSerializer


class ParamSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Param
        fields = BaseVariableSerializer.Meta.fields + ['default_value']


class SecretSerializer(BaseVariableSerializer):
    class Meta(BaseVariableSerializer.Meta):
        model = models.Secret


class CellSerializer(BaseAssetSerializer, VersioningSerializerMixin):
    base_container_image = BaseImageSerializer(required=False)
    containerization_job = CellContainerizationJobSerializer(required=False)
    dependencies = DependencySerializer(many=True, required=False)
    inputs = InputSerializer(many=True, required=False)
    outputs = OutputSerializer(many=True, required=False)
    confs = ConfSerializer(many=True, required=False)
    params = ParamSerializer(many=True, required=False)
    secrets = SecretSerializer(many=True, required=False)

    nested_serializer_classes = {
        'base_container_image': BaseImageSerializer,
        'containerization_job': CellContainerizationJobSerializer,
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
        versions_collection_model = models.CellVersionsCollection
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
            instance = parent_instance.__getattribute__(name).all()
        else:
            instance = parent_instance.__getattribute__(name)
        if data is not None:
            if instance is None:
                serializer = serializer_class(data=data, many=many)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
            else:
                serializer = serializer_class(instance, many=many)
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

    def validate(self, attrs):
        # Enforce that either all or none of the containerization fields be set
        keys = ['containerization_job', 'containerization_workflow_id']
        # attrs contains the data being serialized; self.instance is the existing instance (None on create)
        # A field is None when:
        keys_are_null = [
            # it is explicitly None in attrs
            (key in attrs and attrs[key] is None)
            # it is absent from, or null in, both attrs and self.instance
            or ((attrs.get(key) is None) and (getattr(self.instance, key, None) is None))
            for key in keys]
        if not (all(keys_are_null) or not any(keys_are_null)):
            raise serializers.ValidationError(
                'containerization_job and containerization_workflow_id must all be set or all be null.'
                )
        return attrs

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
        validated_data.update(nested_instances)
        instance = super().create(validated_data)
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
        validated_data.update(nested_instances)
        instance = super().update(instance, validated_data)
        for name, nested_instance in nested_instances_many.items():
            instance.__getattribute__(name).set(nested_instance)
        return instance
