var LoginHandler = function () {
};

LoginHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click", function (event) {
        event.preventDefault();
        var username = $("#username").val();
        var password = $("#password").val();
        console.log('sss')
        $.ajax({
            url: "/login/",
            type: 'POST',
            data: {
                username,
                password,
            },
            success: function (result) {
                if (result['code'] == 200) {
                    alert('登录成功');
                    window.location = "/"
                } else {
                    alert(result['message']);
                }
            }
        })
    });
};

LoginHandler.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var handler = new LoginHandler();
    handler.run();
});