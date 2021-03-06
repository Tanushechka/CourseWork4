$(document).ready(() => {
    let func = $("#function"),
        truthTable = $('#truth-table'),
        pascalTriangle = $("#pascal-triangle"),
        polinomInfo = $("#main-info");

    const MIN_VALUE = 1,
        MAX_VALUE = 20;

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
    let countVal = $(".index-container").find("#counter");
    countVal.on("keyup keydown change", () => {
        let val = countVal.val();
        if (val <= MIN_VALUE) val = MIN_VALUE;
        if (val >= MAX_VALUE) val = MAX_VALUE;
        countVal.val(val);
        changeCounter(val)
    });
    changeCounter(1);

    function changeCounter(v) {
        // countVal.attr("disabled", true);
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                'count': v,
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
                $("#baseTruthTable").html(data["truthTable"]);
                // countVal.attr("disabled", false);
            },
            error: (data) => {
            }
        });
        let vector = "";
        const event = 'this.innerText = +(!parseInt(this.innerText)); clearResult();';
        for(let i=0; i < v; i++) {
            vector += `<button onclick="${event}">0</button>`
        }
        $("#vectorPolarized").html(vector);
        clearResult();
/*
        let main = $("#mainContainer"),
            tableContainer = $("#truthTableContainer"),
            settingsContainer = $("#settingsContainer");
        if (v > 5) {
            main.removeClass("col-8").addClass("col-10");
            main.removeClass("offset-2").addClass("offset-1");
            tableContainer.removeClass("col-5").addClass("col-7");
            settingsContainer.removeClass("col-7").addClass("col-5");
        } else {
            main.removeClass("col-10").addClass("col-8");
            main.removeClass("offset-1").addClass("offset-2");
            tableContainer.removeClass("col-7").addClass("col-5");
            settingsContainer.removeClass("col-5").addClass("col-7");
        }*/
    }

    function replaceAllTableButton(val=1) {
        $.each($("table .functionValue"), (i, x) => x.innerText=val);
        clearResult();
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
                'csrfmiddlewaretoken': csrf_token
            },
            dataType: 'json',
            success: (data) => {
                $("p#polarizedResult").html(data["polinom"]);
            },
            error: (data) => {
            }
        });
    });

    function clearResult() {
        $("p#polarizedResult").html("");
        $("h3#resultTitle").html("");
    }

    window.clearResult = clearResult;

});
