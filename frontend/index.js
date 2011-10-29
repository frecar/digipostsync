
/*
 * Login sends stuff to our backend, so our backend can communicate with digipost
 */


DS.post('/users/', { username: DS.user.username, password: DS.user.password })
	.success(function (user) {
		console.log('User synced to DigipostSync, hooking up GUI changes...');
		DS.user = user;
		DS.load();
	})
	.error(function () {
		console.error('Aiiii, Could not connect to DigipostSync!')
	});
	
DS.load = function () {
	$(window).bind('hashchange', function (data) {
		if (location.hash.indexOf('#/innstillinger') == 0) {
			DS.afterPageLoad(DS.loadSyncTab);
		
			// Load our sync tab after going to dropbox
			if (location.search.indexOf('oauth_token=') != -1) {
				DS.afterPageLoad(DS.loadSyncPage);
			}
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
	
	// Hack: Get that oauth_token away when we click another link
	if (location.search.indexOf('oauth_token=') != -1) {	
		$('a[href^="#"]').each(function () {
			$(this).attr('href', "index.html" + $(this).attr('href'));
		});
	}
	
	$('#innstillingerFrame ul.tabs .active').removeClass("active");
	$(this).addClass("active");
	$('#content .tabContent').load(chrome.extension.getURL("pages/sync.html"), function () {
		$('#dropboxButton').click(function () {
			DS.get('/user/' + DS.user.id + '/get_url_for_auth_dropbox/').success(function (data) {
				window.location = $.parseJSON(data).url + "&oauth_callback=https://www.digipost.no/post/privat/index.html#/innstillinger/varsling";
			});
		});
	});
	
	return false;
}
