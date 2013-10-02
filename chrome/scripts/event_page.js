// Listen for any changes to the URL of any tab.
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    var douban_read_url_regex  = /http:\/\/read.douban.com\/reader\/ebook\//;
    if (changeInfo.status == 'complete') {
        if (douban_read_url_regex.test(tab.url)) {
            chrome.pageAction.show(tabId);
        }
    }
});

function open_option_page() {
    chrome.tabs.create({ url: 'options.html' });
}

// when clicked
chrome.pageAction.onClicked.addListener(function(tab) {
    // config if haven't
    if (!localStorage.to_email || !localStorage.server) {
        open_option_page();
        return;
    }

	chrome.tabs.sendMessage(tab.id, {'call': 'get_current_book_data'}, function(response) {
	    send(response.book_id, response.book_data, function(){
        });
  	});
});

function send(book_id, book_data, callback) {
    var to_email = localStorage.to_email,
        server = localStorage.server;

    if (!to_email || !server) {
        open_option_page();
        return;
    }

    var post_data = {
        book_id: book_id,
        book_data: book_data,
        to_email: to_email
    };

    console.log(post_data);
    return;

	$.post(server, post_data, function(data){
    });
}
