$(document).ready(() => {
    let func = $("#function");

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
            success: function (data) {
                console.log(data);
            }
        });
    });
    $("#clear").click(() => {
        func.val("");
    });
    $("#calbutton button")
        .not("#calculate")
        .not("#clear")
        .click(ev => {
            func.val(func.val() + ev.currentTarget.innerText);
        });
    func.keypress(e => {
        return e.keyCode === 8 || e.keyCode === 46 || e.keyCode === 37 || e.keyCode === 39
    });
});