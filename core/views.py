from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

from .utils import Utils, Operator


def print_result(data, result):
    n = len(data[0])
    headers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:n]
    print(headers + "|RESULT")
    print('-' * len(headers) + '+------')
    for row, result_cell in zip(data, result):
        print(''.join({True: 'T', False:'F'}[cell] for cell in row) + '|' + '  ' + {True: 'T', False:'F'}[result_cell])


class IndexView(View):

    template_name = "index.html"

    def get(self, request):
        data = Utils.get_truth_table(4)
        A, B, C, D = Utils.unpack(data)
        result = Operator.imp_(Operator.xor_(A, D), Operator.or_(B, C))
        print_result(data, result)
        print(Utils.get_truth_table(4))
        return render(request, self.template_name, {})


class TruthTableView(View):

    template_name = "truth_table.html"

    def post(self, request):
        logic_func = request.POST.get("logic_func", "")

        if not logic_func or not Utils.is_balanced_brackets(logic_func):
            return HttpResponse(render_to_string(self.template_name, context={"error": True}, request=request))
        print(Utils.OP_AND in logic_func)
        a = Utils.infix2postfix(logic_func)
        print(a)
        print(Utils.get_used_letters(logic_func))
        print(Utils.calc_postfix(a))
        content = render_to_string(self.template_name, context={}, request=request)
        return HttpResponse(content)
