import requests
from django.db import transaction
from decouple import config
from academics.models.program import Program
from django.shortcuts import get_object_or_404





def update_program_capacity(program_id: int, capacity: int) -> Program:
    """
    Updates a program's enrollment capacity.
    Raises Http404 if program does not exist.
    """

    program = get_object_or_404(Program, id=program_id)

    program.enrollment_capacity = capacity
    program.save(update_fields=["enrollment_capacity"])

    return program


def sync_program_capacity():
    response = requests.get(config('EXTERNAL_API_URL_FOR_STUDENTS_CAPACITY'), timeout=30)
    response.raise_for_status()

    data = response.json()

    with transaction.atomic():
        for item in data:
            program_id = item.get("id")
            capacity = item.get("capacity")

            if capacity is None:
                continue

            try:
                program = Program.objects.get(id=program_id)
                program.enrollment_capacity = int(capacity)
                program.save()
            except Program.DoesNotExist:
                continue
