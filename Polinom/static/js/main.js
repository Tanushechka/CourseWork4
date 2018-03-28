$(document).ready(() => {
    let func = $("#function"),
        truthTable = $('#truth-table'),
        pascalTriangle = $("#pascal-triangle"),
        polinomInfo = $("#main-info");

    const MIN_VALUE = 1,
        MAX_VALUE = 5;

    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $("#calculate").click(() => {
        let value = func.val();
        if (!value) return;

        $.ajax({
            type: 'POST',
            url: '/truth-table/',
            data: {
                'logic_func': value,
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
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
    let countVal = $(".index-container .variables").find("#counter"),
        countChange = $(".index-container .count-change");

    countChange.find("#inc").click(() => changeCounter());
    countChange.find("#dec").click(() => changeCounter("dec"));
    changeCounter("inc", 2);

    function changeCounter(action = "inc", v = null) {
        v = v || parseInt(countVal[0].innerHTML);
        if ((v <= MIN_VALUE && action === "dec") || (v >= MAX_VALUE && action === "inc")) return;
        v += (action === "inc") ? 1 : -1;
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                'count': v,
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
                countVal[0].innerHTML = v;
                $("#baseTruthTable").html(data["truthTable"]);
            },
            error: (data) => {
            }
        });
        let vector = "";
        const event = 'this.innerText = +(!parseInt(this.innerText))';
        for(let i=0; i < v; i++) {
            vector += `<button onclick="${event}">0</button>`
        }
        $("#vectorPolarized").html(vector);
    }

    function replaceAllTableButton(val=1) {
        $.each($("table .functionValue"), (i, x) => x.innerText=val);
    }

    $("#all_zero").click(() => replaceAllTableButton(0));
    $("#all_one").click(() => replaceAllTableButton());

    $("#calculatePolarized").click(() => {
        let _function = [], vector = [];
        $.each($("table .functionValue"), (i, x) => _function.push(parseInt(x.innerText)));
        $.each($("#vectorPolarized").find("button"), (i, x) => vector.push(parseInt(x.innerText)));
        $.ajax({
            type: 'POST',
            url: '/polarize/',
            data: {
                'function': JSON.stringify(_function),
                "vector": JSON.stringify(vector),
                'count': parseInt(countVal[0].innerHTML),
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
                console.log(data);
            },
            error: (data) => {
            }
        });
    });
});
