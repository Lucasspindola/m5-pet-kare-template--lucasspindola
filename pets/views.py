from django.shortcuts import render
from .models import Pet
from django.db.models import Q
from traits.models import Trait
from groups.models import Group
from .serializers import PetSerializer
from traits.serializers import TraitSerializer
import ipdb
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.views import APIView, Request, Response, status


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, req)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, req: Request):
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")

        try:
            group = Group.objects.get(scientific_name=group_data["scientific_name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)
        pet_data_obj = Pet.objects.create(**serializer.validated_data, group=group)
        for trait_loop in traits_data:
            trait = Trait.objects.filter(Q(name__iexact=trait_loop["name"])).first()
            if trait:
                pet_data_obj.traits.add(trait)
            else:
                trait = Trait.objects.create(**trait_loop)
                pet_data_obj.traits.add(trait)
        serializer = PetSerializer(pet_data_obj)
        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def patch(self, req: Request, pet_id: int):
        pet_update_exists = get_object_or_404(Pet, id=pet_id)
        data = req.data
        if "name" in data:
            pet_update_exists.name = data["name"]
        if "age" in data:
            pet_update_exists.age = data["age"]
        if "weight" in data:
            pet_update_exists.weight = data["weight"]
        pet_update_exists.save()
        serializer = PetSerializer(pet_update_exists, req.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            traits_data = serializer.validated_data.get("traits", [])
            group_data = serializer.validated_data.get("group", {})
        except KeyError:
            return Response({"error": "Invalid request data"}, status.HTTP_400_BAD_REQUEST)
        if group_data:
            try:
                group = Group.objects.get(scientific_name=group_data["scientific_name"])
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
            pet_update_exists.group = group
            pet_update_exists.save()
        if traits_data:
            list = []
            for trait_loop in traits_data:
                trait_dict = dict(trait_loop)
                trait, _ = Trait.objects.get_or_create(**trait_dict)
                list.append(trait)
                # pet_update_exists.traits.add(trait)
            pet_update_exists.traits.set(list)
        pet_update_exists.save()
        serializer = PetSerializer(pet_update_exists)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, pet_id: int):
        pet_delete_exists = get_object_or_404(Pet, id=pet_id)
        pet_delete_exists.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, req: Request, pet_id: int):
        pet_exists = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet_exists)

        return Response(serializer.data, status.HTTP_200_OK)
