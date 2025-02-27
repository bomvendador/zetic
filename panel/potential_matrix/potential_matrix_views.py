from pdf.models import PotentialMatrix, Category, Project, ConditionGroup, \
    ConditionGroupOfGroups, ConditionGroupPotentialMatrix, ConditionGroupCategoryPotentialMatrix
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from ..constants import CONSTANT_POTENTIAL_MATRIX
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe

from ..views import info_common
from django.db.models import Sum, Q, Max


@login_required(redirect_field_name=None, login_url='/login/')
def potential_matrix_list(request):
    context = info_common(request)
    potential_matrices = PotentialMatrix.objects.filter(project=None)
    context.update(
        {
            'potential_matrices': potential_matrices,
            # 'potential_matrix_categories': potential_matrix_categories
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
        context.update(
            {
                'potential_matrices': potential_matrices,
                # 'potential_matrix_categories': potential_matrix_categories,
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
        context.update(
            {
                'potential_matrices': potential_matrices,
                # 'potential_matrix_categories': potential_matrix_categories,
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
        # print(json_data)
        # return
        groups_data = json_data['groups_data']
        square_code = json_data['square_code']
        matrix_id = json_data['matrix_id']
        project_id = json_data['project_id']
        if matrix_id != '':
            matrix_inst = PotentialMatrix.objects.get(id=matrix_id)
        else:
            matrix_inst = PotentialMatrix()
        if project_id != '':
            matrix_inst.project = Project.objects.get(id=project_id)
        matrix_inst.created_by = request.user
        matrix_inst.name = CONSTANT_POTENTIAL_MATRIX[square_code]['name']
        matrix_inst.code = square_code
        matrix_inst.save()
        condition_groups_potential_matrix = ConditionGroupPotentialMatrix.objects.filter(matrix=matrix_inst)
        if condition_groups_potential_matrix:
            for condition_group in condition_groups_potential_matrix:
                condition_group.group.delete()

        groups_arr = []
        for group in groups_data:
            new_group_inst = ConditionGroup()
            new_group_inst.created_by = request.user
            new_group_inst.type = group['group_type']
            new_group_inst.save()
            groups_arr.append({
                'id': new_group_inst.id,
                'name': group['group_id']
            })
            new_condition_groups_potential_matrix = ConditionGroupPotentialMatrix()
            new_condition_groups_potential_matrix.created_by = request.user
            new_condition_groups_potential_matrix.group = new_group_inst
            new_condition_groups_potential_matrix.matrix = matrix_inst
            new_condition_groups_potential_matrix.level = group['level']
            new_condition_groups_potential_matrix.save()
            if group['group_categories_arr']:
                group_categories = group['group_categories_arr']
                for category in group_categories:
                    new_condition_group_category_potential_matrix = ConditionGroupCategoryPotentialMatrix()
                    new_condition_group_category_potential_matrix.created_by = request.user
                    new_condition_group_category_potential_matrix.group = new_group_inst
                    new_condition_group_category_potential_matrix.matrix = matrix_inst
                    new_condition_group_category_potential_matrix.category = Category.objects.get(id=category['category_id'])
                    new_condition_group_category_potential_matrix.points_from = category['points_from']
                    new_condition_group_category_potential_matrix.points_to = category['points_to']
                    new_condition_group_category_potential_matrix.save()
                    # new_condition_groups_potential_matrix.
        for group in groups_data:
            parent_group_name = group['parent_group_id']
            group_name = group['group_id']
            if parent_group_name != '':
                parent_group_inst_id = 0
                group_inst_id = 0
                for groups_arr_item in groups_arr:
                    if groups_arr_item['name'] == parent_group_name:
                        parent_group_inst_id = groups_arr_item['id']
                    if groups_arr_item['name'] == group_name:
                        group_inst_id = groups_arr_item['id']
                new_condition_group_of_groups = ConditionGroupOfGroups()
                new_condition_group_of_groups.group = ConditionGroup.objects.get(id=group_inst_id)
                new_condition_group_of_groups.parent_group = ConditionGroup.objects.get(id=parent_group_inst_id)
                new_condition_group_of_groups.created_by = request.user
                new_condition_group_of_groups.matrix = matrix_inst
                new_condition_group_of_groups.save()
        return HttpResponse(200)


@login_required(redirect_field_name=None, login_url='/login/')
def edit_potential_matrix(request, matrix_id):
    context = info_common(request)
    categories = Category.objects.all()
    potential_matrix = PotentialMatrix.objects.get(id=matrix_id)
    if potential_matrix.project:
        matrices_not_defined = get_matrices_not_defined_for_project(matrix_id, potential_matrix.project_id)
        context.update({
            'project': potential_matrix.project
        })
    else:
        matrices_not_defined = get_matrices_not_defined(matrix_id)
    groups_of_matrix = ConditionGroupPotentialMatrix.objects.filter(matrix=potential_matrix)
    max_level = groups_of_matrix.aggregate(Max('level'))['level__max']
    # print(f'max lrvrl = {max_level}')
    groups_of_groups_matrix = ConditionGroupOfGroups.objects.filter(matrix=potential_matrix)
    groups_by_levels = []
    for level in range(max_level + 1):
        # print(f'level = {level}')
        groups_of_matrix_level = ConditionGroupPotentialMatrix.objects.filter(Q(matrix=potential_matrix) &
                                                                              Q(level=level))
        level_data = []
        for group_level in groups_of_matrix_level:
            data = {
                'group_id': group_level.group.id,
                'group_type': group_level.group.type,
                'level': group_level.level
            }
            parent_group_inst = ConditionGroupOfGroups.objects.filter(group=group_level.group)
            if parent_group_inst:
                data.update({
                    # 'parent_group_id': 'group_' + str(ConditionGroupOfGroups.objects.get(group=group_level.group).parent_group.id)
                    'parent_group_id': ConditionGroupOfGroups.objects.get(group=group_level.group).parent_group.id
                })
            matrix_group_categories = ConditionGroupCategoryPotentialMatrix.objects.filter(group=group_level.group)
            group_data_categories = []
            category_rows_html = ''
            if matrix_group_categories:
                for category in matrix_group_categories:
                    category_html_context = {
                        'matrix_category_data': category,
                        'categories': Category.objects.all()
                    }
                    category_html = render_to_string('potential_matrix/potential_matrix_category_tr.html', category_html_context)

                    # print(category_html)
                    group_data_categories.append({
                        'group_id': category.group.id,
                        'id': category.category.id,
                        'name': category.category.name,
                        'points_from': category.points_from,
                        'points_to': category.points_to,
                        'code': category.category.code,
                        'category_html': category_html,
                    })
                    # normalized_text_rows_html = normalize_newlines(category_html).replace('[', '')
                    # category_rows_html.append(mark_safe(normalized_text_rows_html.replace('\n', '')))
                    category_rows_html += category_html

            if len(group_data_categories) > 0:
                categories_table_html_context = {
                    'category_rows_html': category_rows_html,
                    'group_level_id': group_level.group.id,

                }
                categories_table_html = render_to_string('potential_matrix/potential_matrix_category_table_with_rows.html', categories_table_html_context)
                normalized_text = normalize_newlines(categories_table_html)
                # print(normalized_text)
                data.update({
                    'group_data_categories': group_data_categories,
                    'categories_table_html': mark_safe(normalized_text.replace('\n', ''))
                })

            level_data.append(data)
        groups_by_levels.append({
            level: level_data
        })
    # print(groups_by_levels)

    # matrix_groups_data = []

    context.update({
        'matrices_not_defined': matrices_not_defined,
        'categories': categories,
        'potential_matrix': potential_matrix,
        'groups_by_levels': groups_by_levels
        # 'potential_matrix_categories': potential_matrix_categories
    })
    return render(request, 'potential_matrix/add_potential_matrix_page.html', context)


@login_required(redirect_field_name=None, login_url='/login/')
def delete_potential_matrix(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        matrix_id = json_data['matrix_id']
        PotentialMatrix.objects.get(id=matrix_id).delete()
    return HttpResponse(200)

