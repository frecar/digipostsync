
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
	DS.loadSync();
	DS.loadDirs();
}	
	
DS.loadSync = function () {
	$(window).bind('hashchange', function (data) {
		if (location.hash.indexOf('#/innstillinger') == 0) {
			DS.afterPageLoad(DS.loadSyncTab, '#innstillingerFrame');
		}
		
		// Load our sync tab after going to dropbox
		if (location.search.indexOf('oauth_token=') != -1) {
			if (location.hash.indexOf('#/innstillinger') == -1) {
				window.location = "https://www.digipost.no/post/privat/index.html?uid=823393&oauth_token=83rlbebitf45itg#/innstillinger/varsling";
			}
			else {
				DS.get('/user/' + DS.user.id + '/tell_server_dropbox_token_is_ready_for_user/').success(function () {
					DS.user.can_connect_to_dropbox = true;
					DS.afterPageLoad(DS.loadSyncPage, '#innstillingerFrame');
				});
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
	
	// Make it look active
	$('#innstillingerFrame ul.tabs .active').removeClass("active");
	$(this).addClass("active");
	
	// Load the page content
	$('#content .tabContent').load(chrome.extension.getURL("pages/sync.html"), function () {
		
		if (DS.user.can_connect_to_dropbox) {
			$('.dropbox').hide();
			$('.dropbox.synced').show();
		}

		// Add some hooks to those buttons
		$('#dropboxButton').click(function () {
			DS.get('/user/' + DS.user.id + '/get_url_for_auth_dropbox/').success(function (data) {
				window.location = $.parseJSON(data).url + "&oauth_callback=https://www.digipost.no/post/privat/index.html#/innstillinger/varsling";
			});
		});

		$('#dropboxButtonDelete').click(function () {
			DS.get('/user/' + DS.user.id + '/delete_dropbox_token/').success(function (data) {
				DS.user.can_connect_to_dropbox = false;
				$('.dropbox').show();
				$('.dropbox.synced').hide();
			});
		});
	});
	
	return false;
}

DS.loadDirs = function () {
	var mock = ['Regninger', 'Forsikring', 'Helse'];
	
	$('#main-nav li').last()
}
