var IMAGE_URL = '';

function Check() {

}


Check.prototype.listenCheckEvent = function () {
    var changeBtn = $('#news-change');
    changeBtn.click(function (event) {
        event.preventDefault();
        var check_news = $('#news-data').val();
        $.ajax({
            'type': 'POST',
            'url': '/news_check/',
            'data': {
                check_news,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var pred_name = result['data']['pred_name'];
                    myalert.alertInfoWithTitle(pred_name, '识别成功!');
                } else {
                    myalert.alertInfoWithTitle(result['message'], '错误信息')
                }
            }
        })
    })
};


Check.prototype.run = function () {
    var self = this;
    self.listenCheckEvent();
};


$(function () {
    var check = new Check();
    check.run()
});


