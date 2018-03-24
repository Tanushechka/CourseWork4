import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

from .utils import Utils


class IndexView(View):

    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name, {})


class TruthTableView(View):

    TEMPLATES = {
        "table": "truth_table.html",
        "pascal": "pascal_triangle.html",
        "polinom": "polinom.html"
    }

    def post(self, request):
        logic_func = request.POST.get("logic_func", "")
        error_response = HttpResponse(render_to_string(self.TEMPLATES["table"], context={"error": True},
                                                       request=request))

        if not logic_func or not Utils.is_balanced_brackets(logic_func):
            return error_response

        postfix_notation = Utils.infix2postfix(logic_func)
        used_letters = Utils.get_used_letters(logic_func)
        letters_count = len(used_letters)
        data = Utils.get_truth_table(letters_count)
        operands = dict(zip(used_letters, Utils.unpack(data)))
        operands.update({'1': [True] * 2 ** letters_count, '0': [False] * 2 ** letters_count})

        try:
            result = Utils.calc_postfix(postfix_notation, operands)
        except Exception as e:
            print(e)
            return error_response

        columns = used_letters + list(result.keys())
        table = list(map(list, zip(*data))) + list(result.values())

        if not table:
            return error_response

        triangle_base = table[-1][:]
        pascal_triangle = Utils.pascal_triangle(triangle_base)
        polinom_answer = [x[0] for x in pascal_triangle]
        polinom_answer = Utils.generate_polinom(polinom_answer, data, used_letters)

        table = list(map(list, zip(*table)))

        truth_table = render_to_string(self.TEMPLATES["table"],
                                       context={"columns": columns, "data": table}, request=request)
        pascal_triangle = render_to_string(self.TEMPLATES["pascal"],
                                           context={"triangle": pascal_triangle}, request=request)
        polinom_answer = render_to_string(self.TEMPLATES["polinom"],
                                          context={"polinom": polinom_answer}, request=request)

        response = {
            'truthTable': truth_table,
            'pascalTriangle': pascal_triangle,
            'polinomAnswer': polinom_answer
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
