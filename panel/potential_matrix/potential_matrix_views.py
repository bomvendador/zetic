from pdf.models import PotentialMatrix, PotentialMatrixCategory, Category, Project
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from ..constants import CONSTANT_POTENTIAL_MATRIX

from ..views import info_common


@login_required(redirect_field_name=None, login_url='/login/')
def potential_matrix_list(request):
    context = info_common(request)
    potential_matrices = PotentialMatrix.objects.filter(project=None)
    potential_matrix_categories = PotentialMatrixCategory.objects.all()
    context.update(
        {
            'potential_matrices': potential_matrices,
            'potential_matrix_categories': potential_matrix_categories
        }
    )
    return render(request, 'potential_matrix/potential_matrix_list.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def add_potential_matrix(request):
    context = info_common(request)
    categories = Category.objects.all()
    matrices_not_defined = get_matrices_not_defined('')
    if len(matrices_not_defined) > 0:
        context.update({
            'matrices_not_defined': matrices_not_defined,
            'categories': categories
        })
        return render(request, 'potential_matrix/add_potential_matrix_page.html', context)
    else:
        potential_matrices = PotentialMatrix.objects.all()
        potential_matrix_categories = PotentialMatrixCategory.objects.all()
        context.update(
            {
                'potential_matrices': potential_matrices,
                'potential_matrix_categories': potential_matrix_categories,
                'no_free_matrices': True
            }
        )
        return render(request, 'potential_matrix/potential_matrix_list.html', context)


def add_potential_matrix_for_project(request, project_id):
    context = info_common(request)
    categories = Category.objects.all()
    matrices_not_defined = get_matrices_not_defined_for_project('', project_id)
    project = Project.objects.get(id=project_id)
    context.update({
        'project': project
    })
    if len(matrices_not_defined) > 0:
        context.update({
            'matrices_not_defined': matrices_not_defined,
            'categories': categories
        })
        return render(request, 'potential_matrix/add_potential_matrix_page.html', context)
    else:
        potential_matrices = PotentialMatrix.objects.all()
        potential_matrix_categories = PotentialMatrixCategory.objects.all()
        context.update(
            {
                'potential_matrices': potential_matrices,
                'potential_matrix_categories': potential_matrix_categories,
                'no_free_matrices': True
            }
        )
        return render(request, 'potential_matrix/potential_matrix_list.html', context)


def get_matrices_not_defined(matrix_id):
    if matrix_id == '':
        potential_matrices = PotentialMatrix.objects.filter(project=None)
    else:
        potential_matrices = PotentialMatrix.objects.filter(project=None).exclude(id=matrix_id)
    matrices_not_defined = []
    for code, matrix_data in CONSTANT_POTENTIAL_MATRIX.items():
        matrix_defined = False
        if potential_matrices.exists():
            for potential_matrix in potential_matrices:
                if potential_matrix.code == code:
                    matrix_defined = True
        if not matrix_defined:
            matrices_not_defined.append({
                'code': code,
                'name': matrix_data['name'],
                })
    return matrices_not_defined


def get_matrices_not_defined_for_project(matrix_id, project_id):
    if matrix_id == '':
        potential_matrices = PotentialMatrix.objects.filter(project_id=project_id)
    else:
        potential_matrices = PotentialMatrix.objects.filter(project_id=project_id).exclude(id=matrix_id)
    matrices_not_defined = []
    for code, matrix_data in CONSTANT_POTENTIAL_MATRIX.items():
        matrix_defined = False
        if potential_matrices.exists():
            for potential_matrix in potential_matrices:
                if potential_matrix.code == code:
                    matrix_defined = True
        if not matrix_defined:
            matrices_not_defined.append({
                'code': code,
                'name': matrix_data['name'],
                })
    return matrices_not_defined


@login_required(redirect_field_name=None, login_url='/login/')
def save_potential_matrix(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        categories = json_data['categories']
        square_code = json_data['square_code']
        matrix_id = json_data['matrix_id']
        project_id = json_data['project_id']
        if matrix_id != '':
            matrix_inst = PotentialMatrix.objects.get(id=matrix_id)
            PotentialMatrixCategory.objects.filter(matrix=matrix_inst).delete()
        else:
            matrix_inst = PotentialMatrix()
        if project_id != '':
            matrix_inst.project = Project.objects.get(id=project_id)
        matrix_inst.created_by = request.user
        matrix_inst.name = CONSTANT_POTENTIAL_MATRIX[square_code]['name']
        matrix_inst.code = square_code
        matrix_inst.save()
        for category in categories:
            matrix_category = PotentialMatrixCategory()
            matrix_category.category = Category.objects.get(id=category['category_id'])
            matrix_category.matrix = matrix_inst
            matrix_category.points_to = category['points_to']
            matrix_category.points_from = category['points_from']
            matrix_category.created_by = request.user
            matrix_category.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_potential_matrix(request, matrix_id):
    context = info_common(request)
    categories = Category.objects.all()
    potential_matrix = PotentialMatrix.objects.get(id=matrix_id)
    potential_matrix_categories = PotentialMatrixCategory.objects.filter(matrix=potential_matrix)
    if potential_matrix.project:
        matrices_not_defined = get_matrices_not_defined_for_project(matrix_id, potential_matrix.project_id)
        context.update({
            'project': potential_matrix.project
        })
    else:
        matrices_not_defined = get_matrices_not_defined(matrix_id)

    context.update({
        'matrices_not_defined': matrices_not_defined,
        'categories': categories,
        'potential_matrix': potential_matrix,
        'potential_matrix_categories': potential_matrix_categories
    })
    return render(request, 'potential_matrix/add_potential_matrix_page.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_potential_matrix(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        matrix_id = json_data['matrix_id']
        PotentialMatrix.objects.get(id=matrix_id).delete()
    return HttpResponse(200)

