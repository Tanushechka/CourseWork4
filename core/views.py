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


class BaseView(View):
    template_name = "base.html"

    TEMPLATES = {
        "table": "base_truth.html"
    }

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        count = int(request.POST.get("count", 1)) or 1
        data = Utils.get_truth_table(count)
        columns = list(range(1, count + 1))
        columns += ["F(" + "".join("x<sub>{}</sub>{}".format(x, ")" if i == len(columns) - 1 else ",")
                                   for i, x in enumerate(columns))]
        truth_table = render_to_string(self.TEMPLATES["table"],
                                       context={"columns": columns, "data": data}, request=request)
        response = {'truthTable': truth_table}
        return HttpResponse(json.dumps(response), content_type="application/json")


class PolarizeFunctionView(View):

    @classmethod
    def post(cls, request):
        func = json.loads(request.POST.get("function", "[]"))
        vector = json.loads(request.POST.get("vector", "[]"))

        count = len(vector)
        data = Utils.get_truth_table(count)
        columns = [Utils.COLUMN_PREFIX + str(x) for x in range(1, count + 1)]

        reverse_function = Utils.build_reverse_function(func, vector, data)
        pascal_triangle = Utils.pascal_triangle(reverse_function)
        polinom_answer = [x[0] for x in pascal_triangle]
        polinom_answer = Utils.generate_reed_polinom(polinom_answer, data, columns, vector) or '0'
        polinom_answer = "P(F) = {}".format(polinom_answer)

        return HttpResponse(json.dumps({"polinom": polinom_answer}), content_type="application/json")


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
