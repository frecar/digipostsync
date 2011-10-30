
/*
 * DS, short for DigipostSync, is our global, fun fun fun namespace!
 */

var DS = {
	url_backend: 'http://127.0.0.1:8000/api',
	
	user: { 
		username: localStorage.getItem('ds_username'),
		password: localStorage.getItem('ds_password')
	},
	
	/*
	 * Ajax functions, basically just wrappers that add the backend url 
	 * to jQuery's standard calls
	 */ 
	ajax: function (type, url, data) {
		return $.ajax({
		  type: type,
		  url: DS.url_backend + url,
		  data: data
		});
	},
	
	get: function (url, data) {
		return DS.ajax('get', url, data);
	},
	
	post: function (url, data) {
		return DS.ajax('post', url, data);
	},
	
	put: function (url, data) {
		return DS.ajax('put', url, data);
	},
	
	delete: function (url, data) {
		return DS.ajax('delete', url, data);
	},
	
	afterPageLoad: function (func, selector) {
		
		if ($(selector).length > 0) {
			func();
		}
		else {
			$('#content').bind('DOMNodeInserted', function (event) {
				if (event.target.id == 'content-container') {
					func();
					$(this).unbind('DOMNodeInserted');
				}
			});
		}
	}
	
}