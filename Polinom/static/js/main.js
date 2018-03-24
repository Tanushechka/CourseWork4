$(document).ready(() => {
    let func = $("#function"),
        truthTable = $('#truth-table'),
        pascalTriangle = $("#pascal-triangle"),
        polinomInfo = $("#main-info");

    $("#calculate").click(() => {
        let value = func.val();
        if (!value) return;
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/truth-table/',
            data: {
                'logic_func': value,
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
                console.log(data);
                truthTable.html(data['truthTable']);
                pascalTriangle.html(data['pascalTriangle']);
                polinomInfo.html(data["polinomAnswer"])
            },
            error: (data) => {
                truthTable.html(data.responseText);
                pascalTriangle.html("");
                polinomInfo.html("");
            }
        });
    });
    $("#clear").click(() => {
        func.val("");
        truthTable.html("");
        pascalTriangle.html("");
    });
    $("#calbutton").find("button")
        .not("#calculate")
        .not("#clear")
        .click(ev => {
            func.val(func.val() + ev.currentTarget.innerText);
        });
    func.keypress(e => {
        return e.keyCode === 8 || e.keyCode === 46 || e.keyCode === 37 || e.keyCode === 39
    });
});