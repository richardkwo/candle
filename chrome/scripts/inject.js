chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.call == "get_current_book_data") {
        get_current_book_data(function(book_id, book_data){
            sendResponse({
                book_id: book_id,
                book_data: book_data
            });
        });
    } else if (request.call == 'show_result_tip') {
        show_result_tip(request.success);
    }
    return true;
});

function get_book_id() {
    var matches = location.href.match(/ebook\/(\d+)\//);
    return matches[1];
}

function fetch_book_data(book_id, callback) {
    var post_data = {
        ck: $.cookie('ck'),
        aid: book_id,
        reader_data_version: 'v3'
    };
    var url = 'http://read.douban.com/j/article_v2/get_reader_data';
    $.post(url, post_data, function(data){
        var book_data = [
            data.title,
            data.data,
            data.purchase_time,
            data.is_sample,
            data.is_gift,
            data.has_formula,
            data.has_added,
            data.price
        ];
        callback(book_data.join(':'));
    }, 'json');
}

function get_current_book_data(callback) {
    var book_id = get_book_id();
    if (('e' + book_id) in localStorage) {
        callback(book_id, localStorage['e' + book_id]); 
    } else {
        fetch_book_data(book_id, function(book_data) {
            callback(book_id, book_data);
        });
    }
}

function show_result_tip(success) {
    var html = '<div id="send-to-kindle-result">' +
        (success ? '<p>发送成功！</p><p class="content">请等待它出现在你的Kindle中</p>' :
                   '<p>发送失败。</p><p class="content">请稍后重试</p>') +
        '</div>';

    var el = $(html).hide().appendTo('body').fadeIn(1000);
    setTimeout(function(){
        el.fadeOut(2000, function(){
            el.remove();
        });
    }, 3000);
}
