
/*
 * Login sends stuff to our backend, so our backend can communicate with digipost
 */


DS.post('/users/', { username: DS.username, password: DS.password })
	.success(function (data) {
		console.log('User synced to DigipostSync, hooking up GUI changes...');
		//DS.load();
	})
	.error(function () {
		console.error('Aiiii, Could not connect to DigipostSync!')
	});
	
DS.load = function () {
	$(window).bind('hashchange', function (data) {
		if (location.hash.indexOf('#/innstillinger') == 0) {
			$('#content').bind('DOMNodeInserted', function (event) {
				if (event.target.id == 'content-container') {
					DS.loadSyncTab();
					$(this).unbind('DOMNodeInserted');
				}
			});
		}
	});
	
	$(window).trigger('hashchange');
}

DS.loadSyncTab = function () {
	$('#innstillingerFrame ul.tabs li').last().removeClass("last");
	$('#innstillingerFrame ul.tabs').append('<li class="last"><a href="#">Synkronisering</a></li>');
	$('#innstillingerFrame ul.tabs li').last().click(DS.loadSyncPage);
}

DS.loadSyncPage = function () {
	$('#innstillingerFrame ul.tabs .active').removeClass("active");
	$(this).addClass("active");
	$('#content .tabContent').load(chrome.extension.getURL("pages/sync.html"), function () {
		$('#dropboxButton').click(function () {
			DS.get('/').success(function (url) {
				window.location(url);
			})
		})
	});
	
	return false;
}

DS.load();
